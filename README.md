# relwrac

A basic crawler developed with Python 3.7+
and [asyncio](https://docs.python.org/3/library/asyncio.html).

**WARNING: this project is in alpha stage and you should not be using it in production.**

## Crawler

[link_extractor.py](/src/link_extractor.py) is a Python program that allows to extract
all links included in pages from a start URL recursively.

## TODO

- Show a graph of the crawled URLs.
- Filter URLs to crawl by regex.
- Compute page rank of the URLs.
- Limit crawling by time.
- Add multiprocessing to crawling process.
- Check if timeout works.
- Store links in database (optionally)
- Some documentation and examples.
- Measure performance.
