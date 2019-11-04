# relwrac

A basic crawler developed with Python 3.7+
and [asyncio](https://docs.python.org/3/library/asyncio.html).

**WARNING: this project is in alpha stage and you should not be using it in production.**

## Crawler

[link_extractor.py](/src/link_extractor.py) is a Python program that allows to extract
all links included in pages from a start URL recursively.

### Example

Get all reddit links (starting from http://old.reddit.com).

Note there is no depth specified, hence it is 2 (default value).

Results will be saved in two files, a pickle file and a CSV file.

Pickle file will store `Crawler.link_adj` attribute and CSV file
will store a line per crawled URL and a column for each link found
in that URL.

```bash
$ pwd
/home/my_user/relcraw
$ python3 src/link_extractor.py \
    -u http://old.reddit.com  \
    -ureg '^https:\/\/(\w+\.)?reddit\.com$' \
    -op reddit_domain.pickle \
    -csv reddit_domain.csv
```

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
