import datetime
import numpy as np
from typing import List, Set, Dict, KeysView


class Crawl(object):
    def __init__(self, crawler=None):
        self.crawler = crawler
        self.links_by_url: Dict[str, Set[str]] = dict()
        self.visited_urls = []
        self.__urls = None
        self.created_at = datetime.datetime.utcnow()

    def add_url_links(self, url: str, page_links: List[str]):
        if url not in self.links_by_url:
            self.links_by_url[url] = set()
            self.visited_urls.append(url)
        self.links_by_url[url] |= page_links

    def __len__(self) -> int:
        return len(self.urls)

    @property
    def urls(self) -> List[str]:
        if self.__urls:
            return self.__urls
        urls_set = set(self.visited_urls)
        for url, page_links in self.links_by_url.items():
            urls_set |= set(page_links)
        self.__urls = list(urls_set)
        return self.__urls

    @property
    def adjacency_matrix(self) -> np.array:
        size = len(self)
        url_index = {url_i: index for index, url_i in enumerate(self.urls)}
        adj_matrix = np.zeros(shape=(size, size))
        # Weighted adjacency matrix
        for url_i, page_links in self.links_by_url.items():
            url_i_index = url_index[url_i]
            for url_i_page_link_j in page_links:
                url_i_page_link_j_index = url_index[url_i_page_link_j]
                adj_matrix[url_i_index, url_i_page_link_j_index] += 1.0
        return adj_matrix
