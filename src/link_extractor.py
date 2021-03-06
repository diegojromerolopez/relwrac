import argparse
import asyncio
import logging
import os
import re
from typing import Optional

import validators

from crawler.crawl.crawl import Crawl
from crawler.crawler import Crawler
from crawler.delay import Delay
from crawler.stop_condition import StopCondition
from crawler.url_filter import UrlFilter
from crawler.user_agent import UserAgent
from crawler.crawl.output.csv import CSVWriter
from crawler.crawl.output.pickle import PickleWriter


def make_logger():
    current_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(
        current_file_path, '..', 'log', f'link_extractor-depth.log'
    )
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(filename=log_file_path, filemode='w+', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.Logger(name='link_extractor')
    return logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Start URL that will be the first step of crawling", type=str,
                        required=True)
    parser.add_argument("-d", "--max_depth", help="Max depth of crawling", type=int, default=2, required=False)
    parser.add_argument("-ureg", "--url_regex", help="URL regex of the URLs you want to crawl", type=str,
                        default=None, required=False)
    parser.add_argument("-ua", "--user_agent", help="Max depth of crawling", type=str, required=False)
    parser.add_argument("-op", "--pickle_path",
                        help="The path of a pickle object that stores a dict where each key is an URL and the values"
                             "are a list of URLs found there.", type=str, required=False)
    parser.add_argument("-csv", "--csv_path",
                        help="The path of a csv file that the URLs found in each page.", type=str, required=False)

    args = parser.parse_args()

    if not validators.url(args.url):
        raise ValueError(f"The first argument must be an URL. It is {args.url} instead")

    if args.max_depth < 1:
        raise ValueError(f"Max depth argument must be greater or equal than 1. It is {args.max_depth} instead")

    url_filter: Optional[UrlFilter] = None
    if args.url_regex:
        try:
            url_filter = UrlFilter(args.url_regex)
        except re.error:
            raise ValueError(f"URL regex argument is not a valid regex. It is {args.url_regex} instead")

    if not args.pickle_path and not args.csv_path:
        raise ValueError(f"An output file path (pickle or CSV) is required.")

    crawl_delay = (1, 2)

    logger = make_logger()

    crawler = Crawler(
        start_url=args.url,
        stop_condition=StopCondition.depth_is_reached(args.max_depth),
        url_filters=[url_filter],
        user_agent=UserAgent.none(),
        timeout=None,
        logger=logger,
        delay=Delay.uniform(*crawl_delay)
    )

    crawl: Crawl = asyncio.run(crawler.crawl())

    if args.pickle_path:
        PickleWriter(crawl).write(args.pickle_path)

    if args.csv_path:
        CSVWriter(crawl).write(args.csv_path)


if __name__ == '__main__':
    main()
