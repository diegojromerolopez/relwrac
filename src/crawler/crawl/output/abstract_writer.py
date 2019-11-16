from crawler.crawl.crawl import Crawl


class AbstractWriter(object):
    def __init__(self, crawl: Crawl):
        self.links_by_url = crawl.links_by_url
