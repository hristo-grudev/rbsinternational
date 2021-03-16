import scrapy

from scrapy.loader import ItemLoader

from ..items import RbsinternationalItem
from itemloaders.processors import TakeFirst


class RbsinternationalSpider(scrapy.Spider):
	name = 'rbsinternational'
	start_urls = ['https://www.rbsinternational.com/institutional-banking/news.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="singlearticle"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//span[@class="title1"]/text()').get()
		description = response.xpath('//div[@class="singlearticle"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="apr-text legal-copy"]/span[@class="text-comp"]/text()').get()

		item = ItemLoader(item=RbsinternationalItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
