# Standalone spider (without a scrapy project)
import scrapy

class TweetSpider(scrapy.Spider):
	name = "twitter"

	def start_requests(self):
		# GET request
		yield scrapy.Request(f"https://twitter.com/{self.instance['username']}", meta = {"playwright": True})

	def parse(self, response):
		# yield from response.xpath('//article//a@href').getall()
		print(response.xpath('//article//a@href').getall())