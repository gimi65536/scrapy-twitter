from scrapy.exceptions import DropItem
import requests

class TweetPipeline:
	def process_item(self, item, spider):
		if item['href'] in spider.history:
			raise DropItem("Existing")

		print(f"\t{item['href']}")
		spider.history.add(item['href'])
		for webhook in spider.instance['webhook']:
			method = webhook['method'].strip().lower()
			if method not in ('post', 'put', 'patch'):
				method = 'post'
			r = requests.request(method, webhook['address'],
				headers = webhook.get('headers'),
				data = {k: v.format(**item) for k, v in webhook['data'].items()}
			)
			# print(r.status_code)

		return item
