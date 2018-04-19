from scrapy import Spider, Request
from sephora.items import SephoraItem
import re
import pandas as pd
import json
import math
import time

n_count_tot = 0

class SephoraSpider(Spider):

	name = "sephora_spider_check"
	allowed_urls = ["https://www.sephora.com", "https://api.bazaarvoice.com"]
	start_urls = ["https://www.sephora.com/brand/list.jsp"]
	# start_urls = ["https://www.sephora.com"]

	#first is to collect all the links for all the brands
	#but this will not be used because the data is just too much. I'll just define the links

	def parse(self, response):
		#time.sleep(0.5)
		#this scrapes all of the brands
		link = response.xpath('//a[@class="u-hoverRed u-db u-p1"]//@href').extract()
		brand_links = [x + "?products=all" for x in link]
		
		#brand_links = ["/fenty-beauty-rihanna", "/kiehls", "/lancome", "/estee-lauder", "/the-ordinary",
		#"/shiseido", "/sk-ii", "/clinique", "/benefit-cosmetics", "dr-jart", "/chanel", "/nars",
		#"/laneige", "/urban-decay", "/bobbi-brown"]
		# brand_links = ["/bobbi-brown"]
		# brand_links = [x + "?products=all" for x in brand_links]

		#this scrapes only the brands inside brand_links
		links = ["https://www.sephora.com" + link for link in brand_links]
		print("total num of brand:",len(links))
		for i,url in enumerate(links):
			#time.sleep(0.5)
			yield Request(url, callback=self.parse_product,meta={'brand_index':i,'brand_total':len(links)})

	def parse_product(self, response):
		#time.sleep(0.5)	

		brand_index = response.meta['brand_index']
		brand_total = response.meta['brand_total']
		print("Current brand_index is:",brand_index,"/",brand_total)
		dictionary = response.xpath('//script[@id="searchResult"]/text()').extract()
		dictionary = re.findall('"products":\[(.*?)\]', dictionary[0])[0]
		
		product_urls = re.findall('"product_url":"(.*?)",', dictionary)
		product_names = re.findall('"display_name":"(.*?)",', dictionary)
		product_ids = re.findall('"id":"(.*?)",', dictionary)
		ratings = re.findall('"rating":(.*?),', dictionary)
		brand_names = re.findall('"brand_name":"(.*?)",', dictionary)
		#list_prices = re.findall('"list_price":(.*?),', dictionary)

		links2 = ["https://www.sephora.com" + link for link in product_urls]

		if len(product_urls)!=len(ratings)!=len(brand_names):
			print('Number of products do not match with ratings')
		else:
			item = SephoraItem()
			item['brand_name'] = brand_names[0]
			item['n_product'] = len(brand_names)
			yield item


		