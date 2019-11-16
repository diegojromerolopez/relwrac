import numpy as np
from typing import Callable
from crawler.crawl.crawl import Crawl
from crawler.crawl.page_rank.page_rank import PageRank


# See https://www.cs.ubc.ca/~nando/540b-2011/lectures/book540.pdf
# for more information about this implementation
class PageRankComputer(object):
    def __init__(self, crawl: Crawl, epsilon: float = 0.001,
                 stop_condition: Callable[[int, np.array, np.array], bool] =
                 lambda iterations, pi_t, pi_t_1: iterations == 1000):
        self.__crawl = crawl
        self.__size = len(crawl)
        self.__urls = crawl.urls
        self.__url_indexes = crawl.url_indexes

        self.__epsilon = epsilon
        self.__stop_condition = stop_condition

        self.transition_matrix = None
        self.page_rank_matrix = None

    def __compute_transition_matrix(self) -> np.array:
        # Adjacency matrix, i.e T[i][j] is the number of links from URL_i to URL_j
        T = self.__crawl.adjacency_matrix
        # Matrix of uniform probability
        # E[i][j] = 1/size
        E = np.ones(T.shape) / self.__size
        # L[i][j] = T[i][j] + e*(1/size), this avoids falling in link cycles
        L = T + self.__epsilon * E
        # Normalization
        G = np.zeros(L.shape)
        for i in range(self.__size):
            G[i, :] = L[i, :] / np.sum(L[i, :])
        # G is a stochastic
        # matrix, matrix where G[i][j] stores the probability
        # of the web surfer of going from link i to link j
        return G

    def __compute_page_rank(self) -> np.array:
        self.transition_matrix = self.__compute_transition_matrix()
        pi = np.random.rand(self.__size)
        pi /= np.sum(pi)
        pi_t = pi
        iterations = 0
        while True:
            pi_t_1 = np.dot(pi_t, self.transition_matrix)
            self.__stop_condition(iterations, pi_t_1, pi_t)
            if self.__stop_condition(iterations, pi_t, pi_t_1):
                pi_t = pi_t_1
                break
            pi_t = pi_t_1
            iterations += 1
        return pi_t

    def compute(self) -> np.array:
        self.page_rank_matrix = self.__compute_page_rank()
        return PageRank(self.page_rank_matrix, self.__url_indexes)
