import pickle
from typing import Callable, Optional, Dict

import numpy as np


class PageRank(object):
    def __init__(self, page_rank_matrix: np.array, url_indexes: Dict[str, int]):
        self.__page_rank_matrix = page_rank_matrix
        self.__url_indexes = url_indexes

    def link_page_rank(self, url) -> Optional[float]:
        if self.__page_rank_matrix is None:
            raise ValueError("Page rank has not been computed yet!")

        url_index = self.__url_indexes.get(url)
        if url_index is None:
            return None

        return self.__page_rank_matrix[url_index]

    def save(self, file_path):
        with open(file_path, 'wb') as pickle_file:
            pickle.dump({"page_rank_matrix": self.__page_rank_matrix, "url_indexes": self.__url_indexes}, pickle_file)

    @classmethod
    def load(cls, file_path):
        with open(file_path, 'rb') as pickle_file:
            page_rank_attributes = pickle.load(pickle_file)
            return PageRank(**page_rank_attributes)
