import re


class UrlFilter(object):
    def __init__(self, url_regex):
        self.url_regex = url_regex
        self.compiled_url_regex = re.compile(url_regex)

    def match(self, url):
        return self.compiled_url_regex.match(url)
