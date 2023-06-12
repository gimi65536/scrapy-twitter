# Standalone spider (without a scrapy project)
import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod

class TweetSpider(scrapy.Spider):
	name = "twitter"

	def start_requests(self):
		# GET request
		yield scrapy.Request(f"https://twitter.com/{self.instance['username']}", meta = {
			"playwright": True,
			"playwright_include_page": True,
			"playwright_page_methods": [
				PageMethod("wait_for_timeout", 20000)
			]
		})

	def parse(self, response):
		# print(response.text)
		for article in reversed(response.xpath('//article')):
			href = article.xpath('.//a[time]/@href').get()
			created_at = datetime.fromisoformat(article.xpath('.//time/@datetime').get())
			text = ''.join(article.xpath('.//div[@data-testid="tweetText"]//text()').getall())
			yield {
				"text": text,
				"username": self.instance['username'],
				"link": f"https://twitter.com{href}",
				"created_at": created_at,
				"href": href, # This field is used as an identifier (like "id of the tweet")
			}
