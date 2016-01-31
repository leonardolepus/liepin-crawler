# liepin-crawler
A scrapy-based crawler that retrieves all relevant job postings from liepin.com that match a list of queries

Scrapy is required.

In the app folder, run:

scrapy crawl liepin -o output.csv

This will automatically retrieve all relevant jobs that match a list of queries, and store them in the output.csv file, which can be further analyzed using excel.

The queries are incorporated in the liepin/spider/liepin_spider.py file as a list of urls. Modify this part to run your own queries.
