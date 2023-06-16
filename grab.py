from scrapy.crawler import CrawlerProcess

from yaml import safe_load
from decouple import config
from datetime import datetime
from time import sleep

from spider import TweetSpider
from pipeline import TweetPipeline

import json
import pickle
from pathlib import Path

from multiprocessing import Process

with open(config('GRAB_INFO')) as f:
    data = safe_load(f)

use_pickle = config('PICKLE', cast = bool, default = False)

def load_history():
	if use_pickle:
		history_path = Path('history/history.pickle')
		if(history_path.exists()):
			with open(history_path, 'rb') as f:
				try:
					obj = pickle.load(f)
				except:
					pass
				else:
					return obj
	else:
		history_path = Path('history/history.json')
		if(history_path.exists()):
			with open(history_path, 'rt') as f:
				try:
					j = json.load(f)
				except:
					pass
				else:
					return [set(l) for l in j]

	return [set() for _ in data['instance']]

def dump_history(history):
	if use_pickle:
		history_path = Path('history/history.pickle')
		with open(history_path, 'wb') as f:
			pickle.dump(history, f)
	else:
		history_path = Path('history/history.json')
		with open(history_path, 'wt') as f:
			json.dump([list(s) for s in history], f)

history = load_history()

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
		"LOG_LEVEL": "ERROR",
		"PLAYWRIGHT_BROWSER_TYPE": "firefox",
		"USER_AGENT": None,
    }
)

def run(history):
	for index, i in enumerate(data['instance']):
		process.crawl(TweetSpider, instance = i, history = history[index])

	process.start()
	print("Done")
	# All processes are done
	dump_history(history)

# Main
while True:
	print(datetime.now().strftime('%Y%m%d %H:%M'))
	_process = Process(target = run, args = (history, )) # history will changed in the process but not here
	_process.start()
	_process.join()
	_process.close()
	history = load_history() # Update the variable changed in the process
	sleep(data['period'])
