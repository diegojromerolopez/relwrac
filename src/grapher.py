import argparse
import pickle

from crawler.crawl.crawl import Crawl
from crawler.crawl.output.graph import Graph


class Grapher(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None
        self.crawl = None

    def __enter__(self):
        self.file = open(self.file_path, 'rb')

        links_by_url = pickle.load(self.file)
        self.crawl = Crawl.create_from_links_by_url(links_by_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def plot_to_file(self, file_path):
        graph = Graph(crawl=self.crawl)
        graph.build()
        print(graph)
        graph.save_plot(file_path=file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pickle_path",
                        help="The path of a pickle file that stores the crawled URLs", type=str, required=True)
    parser.add_argument("-o", "--output-file", help="Output file were the graph will be drawn", type=str, required=True)

    args = parser.parse_args()

    with Grapher(args.pickle_path) as grapher:
        grapher.plot_to_file(args.output_file)


if __name__ == '__main__':
    main()
