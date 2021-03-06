import asyncio
import logging
import random
import urllib
import urllib.parse
from typing import Set, Union, List, Callable, Dict, Optional

import aiohttp
import validators
from bs4 import BeautifulSoup

from crawler.crawl.crawl import Crawl
from crawler.url_filter import UrlFilter


class Crawler(object):
    def __init__(self,
                 start_url: str,
                 stop_condition: Callable[[int, Crawl], bool],
                 logger: logging.Logger,
                 url_filters: Optional[List[UrlFilter]] = None,
                 delay: Union[int, Callable[[], int]] = 0,
                 proxies: Union[str, List, Callable] = None,
                 user_agent: Union[str, List, Callable] = None,
                 timeout: Union[int, Callable] = None,
                 ):
        self.start_url = start_url
        self.stop_condition = stop_condition
        self.logger = logger
        self.url_filters = url_filters

        self.delay = delay
        self.proxies = proxies
        self.user_agent = user_agent
        self.timeout = timeout

    async def crawl(self) -> Crawl:
        current_crawl: Crawl = Crawl(crawler=self)
        await self.__crawl(current_crawl, [self.start_url], 0)
        return current_crawl

    async def __crawl(self, current_crawl: Crawl, urls: List[str], depth):
        if self.stop_condition(depth, current_crawl):
            return

        page_links = await asyncio.gather(*(self.__page_links(url) for url in urls))

        unvisited_urls = set()
        for url_index, links_found in enumerate(page_links):
            url_i = urls[url_index]
            current_crawl.add_url_links(url_i, links_found)
            unvisited_urls |= links_found

        unvisited_urls -= set(current_crawl.visited_urls)

        return await self.__crawl(current_crawl=current_crawl, urls=list(unvisited_urls), depth=depth + 1)

    async def __page_links(self, url: str) -> Set[str]:
        await self.__sleep()

        proxy_url = self.__proxy_url()

        headers = self.__request_headers()

        timeout = self.__timeout()

        async with aiohttp.ClientSession(timeout=timeout) as session:
            response = await session.get(url=url, headers=headers, proxy=proxy_url)
            page_links = set()
            html = await response.text(errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            for html_a in soup.find_all('a'):
                page_link = html_a.get('href')
                page_url = urllib.parse.urljoin(url, page_link)
                if self.__url_must_be_crawled(page_url):
                    page_links.add(page_url)
            return page_links

    async def __sleep(self):
        if self.delay:
            if callable(self.delay):
                delay = self.delay()

            elif isinstance(self.delay, int):
                delay = self.delay

            else:
                raise ValueError('Invalid delay value, expected an integer or callable')

            await asyncio.sleep(delay)

    def __proxy_url(self) -> Optional[str]:
        if isinstance(self.proxies, str):
            return self.proxies

        if isinstance(self.proxies, list):
            return random.choice(self.proxies)

        if callable(self.proxies):
            return self.proxies()

        return None

    def __request_headers(self) -> Dict[str, str]:
        headers = dict()

        if self.user_agent:
            if isinstance(self.user_agent, str):
                headers['User-Agent'] = self.user_agent

            if isinstance(self.user_agent, list):
                headers['User-Agent'] = random.choice(self.user_agent)

            if callable(self.user_agent):
                headers['User-Agent'] = self.user_agent()

        return headers

    def __timeout(self) -> aiohttp.ClientTimeout:
        if isinstance(self.timeout, int):
            return aiohttp.ClientTimeout(total=self.timeout)

        if callable(self.timeout):
            return aiohttp.ClientTimeout(total=self.timeout())

        return aiohttp.helpers.sentinel

    def __url_must_be_crawled(self, url) -> bool:
        if not validators.url(url):
            return False

        if not self.url_filters:
            return True

        for url_filter in self.url_filters:
            if url_filter.match(url):
                return True

        return False
