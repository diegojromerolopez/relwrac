import csv

from output.abstract_writer import AbstractWriter


class CSVWriter(AbstractWriter):
    def write(self, file_path):
        with open(file_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
            for page_url, page_links in self.links_by_url.items():
                csv_writer.writerow([page_url] + list(page_links))
