import argparse

from crawler.crawl import Crawl
import pickle

from output.page_rank import PageRank


class PageRanker(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None
        self.crawl = None

    def __enter__(self):
        self.file = open(self.file_path, 'rb')
        self.crawl = Crawl()
        links_by_url = pickle.load(self.file)
        for url, page_links in links_by_url.items():
            self.crawl.add_url_links(url, page_links)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def compute(self):
        page_rank = PageRank(crawl=self.crawl)
        R = page_rank.compute()
        print(R)

    def plot_to_file(self, file_path):
        page_rank = PageRank(crawl=self.crawl)
        R = page_rank.compute()
        print(R)
        #page_rank.save_plot(file_path=file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pickle_path",
                        help="The path of a pickle file that stores the crawled URLs", type=str, required=True)
    #parser.add_argument("-o", "--output-file", help="Output file were the graph will be drawn", type=str, required=True)

    args = parser.parse_args()

    with PageRanker(args.pickle_path) as page_ranker:
        page_ranker.compute()


if __name__ == '__main__':
    main()
