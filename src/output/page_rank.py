from crawler.crawl import Crawl
import numpy as np

# See https://www.cs.ubc.ca/~nando/540b-2011/lectures/book540.pdf
# for more information about this implementation
class PageRank(object):
    def __init__(self, crawl: Crawl):
        self.crawl = crawl
        self.size = len(crawl)

    def __transition_matrix(self, epsilon=0.0) -> np.array:
        # Adjacency matrix, i.e T[i][j] is the number of links from URL_i to URL_j
        T = self.crawl.adjacency_matrix
        # E[i][j] = 1/size
        E = np.ones(T.shape) / self.size
        # L[i][j] = T[i][j] + e*(1/size)
        L = T + epsilon * E
        # Normalization
        G = np.zeros(L.shape)
        for i in range(self.size):
            G[i, :] = L[i, :] / np.sum(L[i, :])
        return G

    def compute(self, epsilon=0.001, iterations=1000):
        G = self.__transition_matrix(epsilon=epsilon)
        pi = np.random.rand(self.size)
        pi /= np.sum(pi)
        R = pi
        for _ in range(iterations):
            R = np.dot(R, G)
        return R

    def save_plot(self, file_path: str):
        import matplotlib.pyplot as plt
        evolution = [np.dot(self.pi, self.G ** i) for i in range(1, 20)]
        plt.figure()
        for i in range(self.size):
            plt.plot([step[0, i] for step in evolution], label=fnames[i], lw=2)
        plt.draw()
        plt.title('rank vs iterations')
        plt.xlabel('iterations')
        plt.ylabel('rank')
        plt.legend()
        plt.draw()

