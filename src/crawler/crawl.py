import datetime
from typing import List, Set, Dict, KeysView


class Crawl(object):
    def __init__(self, links_by_url: Dict[str, Set[str]] = None, crawler=None):
        self.crawler = crawler
        if links_by_url is None:
            links_by_url = {}
        self.links_by_url: Dict[str, Set[str]] = links_by_url
        self.created_at = datetime.datetime.utcnow()

    def add_url_links(self, url: str, page_links: List[str]):
        if url not in self.links_by_url:
            self.links_by_url[url] = set()
        self.links_by_url[url] |= page_links

    @property
    def visited_urls(self) -> KeysView[str]:
        return self.links_by_url.keys()
