from scrapy.exceptions import DropItem

class TweetPipeline:
	def process_item(self, item, spider):
		if item['href'] in spider.history:
			raise DropItem("Existing")

		spider.add(item['href'])
		NotImplemented
