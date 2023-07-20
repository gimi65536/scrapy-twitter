from yaml import safe_load
from decouple import config
from datetime import datetime
from time import sleep

import json
import pickle
from pathlib import Path

import requests
from parsel import Selector

with open(config('GRAB_INFO')) as f:
    data = safe_load(f)

use_pickle = config('PICKLE', cast = bool, default = False)
bridge = config('BRIDGE', default = 'https://rss-bridge.org/bridge01/')

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

# Main
while True:
	print(datetime.now().strftime('%Y%m%d %H:%M'))
	for index, i in enumerate(data['instance']):
		print(f"Instance {index}")
		response = requests.get(bridge, params = {
			'action': 'display',
			'bridge': 'TwitterBridge',
			'context': 'By username',
			'u': i['username'],
			'norep': 'on',
			'nopinned': 'on',
			'nopic': 'on',
			'noimg': 'on',
			'noimgscaling': 'on',
			'format': 'Json'
		})
		result = response.json()

		if 'items' not in result:
			print('\tError when retrieving response...')
			continue

		print(f"\tReteieved {len(result['items'])} tweets")

		for tweet in reversed(result['items']):
			if tweet['id'] in history[index]:
				continue

			history[index].add(tweet['id'])
			print('\t', tweet['id'])

			# Retrieve text
			selector = Selector(tweet['content_html'])
			text = selector.xpath('//blockquote/text()').get()
			# Send to webhooks
			send_data = {
				"text": text,
				"username": i['username'],
				"link": tweet['url'],
				"created_at": tweet['date_modified']
			}
			for webhook in i['webhook']:
				method = webhook['method'].strip().lower()
				if method not in ('post', 'put', 'patch'):
					method = 'post'
				r = requests.request(method, webhook['address'],
					headers = webhook.get('headers'),
					data = {k: v.format(**send_data) for k, v in webhook['data'].items()}
				)
				print('\t\t', r.status_code)

	dump_history(history)
	sleep(data['period'])
