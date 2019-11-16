import argparse
from typing import Optional

from crawler.crawl.page_rank.page_rank import PageRank


class LinkPageRank(object):
    def __init__(self, page_rank_matrix_file_path: str):
        self.page_rank_matrix_file_path = page_rank_matrix_file_path
        self.page_rank: Optional[PageRank] = None

    def load_page_rank(self):
        self.page_rank = PageRank.load(self.page_rank_matrix_file_path)

    def get(self, url):
        return self.page_rank.link_page_rank(url)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pr", "--page_rank_path",
                        help="The path of a pickle file that stores the page rank", type=str, required=True)
    parser.add_argument("-u", "--url", help="URL whose page rank will be returned", type=str, required=True)

    args = parser.parse_args()

    link_page_rank = LinkPageRank(args.page_rank_path)
    link_page_rank.load_page_rank()
    url_page_rank = link_page_rank.get(args.url)

    print(f"{args.url} has a page rank of {url_page_rank}")


if __name__ == '__main__':
    main()
