from scrapy.crawler import CrawlerProcess

from yaml import safe_load
from decouple import config
from datetime import datetime
from time import sleep

from spider import TweetSpider
from pipeline import TweetPipeline

with open(config('GRAB_INFO')) as f:
    data = safe_load(f)

process = CrawlerProcess(
    settings={
        "DOWNLOAD_HANDLERS": {
			"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
			"https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
		},
		"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
		"ITEM_PIPELINES": {
			TweetPipeline: 100,
		},
    }
)

# Main
while True:
	sleep(data['period'])
	print(datetime.now().strftime('%Y%m%d %H:%M'))
	for index, i in enumerate(data['instance']):
		process.crawl(TweetSpider, instance = i)

	process.start(stop_after_crawl = False)
