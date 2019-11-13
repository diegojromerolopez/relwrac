from crawler.crawl import Crawl
import numpy as np

# See https://www.cs.ubc.ca/~nando/540b-2011/lectures/book540.pdf
# for more information about this implementation
class PageRank(object):
    def __init__(self, crawl: Crawl):
        self.crawl = crawl
        self.size = len(crawl)

    def __transition_matrix(self, epsilon=0.0) -> np.array:
        trans = self.crawl.adjacency_matrix
        #
        E = np.ones(trans.shape) / self.size
        L = trans + epsilon * E
        m_c_trans_matrix = np.array(np.zeros(L.shape))
        for i in range(self.size):
            m_c_trans_matrix[i, :] = L[i, :] / np.sum(L[i, :])
        return m_c_trans_matrix

    def compute(self, epsilon=0.001, iterations=1000):
        self.G = self.__transition_matrix(epsilon=epsilon)
        self.pi = np.random.rand(self.size)
        self.pi /= np.sum(self.pi)
        self.R = self.pi
        for _ in range(iterations):
            self.R = np.dot(self.R, self.G)
        return self.R

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

