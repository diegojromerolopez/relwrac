import pickle

from crawler.crawl.output.abstract_writer import AbstractWriter


class PickleWriter(AbstractWriter):
    def write(self, file_path):
        with open(file_path, 'wb') as pickle_file:
            pickle.dump(self.links_by_url, pickle_file)
