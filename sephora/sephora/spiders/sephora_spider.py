from scrapy import Spider, Request
from sephora.items import SephoraItem
import re
import pandas as pd
import json
import math
import time

n_count_tot = 0

class SephoraSpider(Spider):

	name = "sephora_spider"
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
			yield Request(url, callback=self.parse_product,meta={'brand_index':i})

	def parse_product(self, response):
		#time.sleep(0.5)	

		brand_index = response.meta['brand_index']
		print("Current brand_index is:",brand_index)
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

		product_df = pd.DataFrame({'links2': links2,'product_names': product_names,'p_id': product_ids, 
			'ratings': ratings,'brand_names': brand_names})

		print (product_df.head())
		print (list(product_df.index))
		print("total num of product:",len(product_df))

		for n in list(product_df.index):
			product = product_df.loc[n, 'product_names']
			p_id = product_df.loc[n, 'p_id']
			p_star = product_df.loc[n, 'ratings']
			brand_name = product_df.loc[n, 'brand_names']

			print (product_df.loc[n,'links2'])

			#if n>0:
				#time.sleep(20)

			yield Request(product_df.loc[n,'links2'], callback=self.parse_detail,
				meta={'n':n,'product': product, 'p_id':p_id, 'p_star':p_star, 'brand_name':brand_name,})

	def parse_detail(self, response):
		#time.sleep(0.5)
		print ('parse_detail: current index is',response.meta['n'])

		product = response.meta['product']
		p_id = response.meta['p_id']
		p_star = response.meta['p_star']
		brand_name = response.meta['brand_name']

		p_category = response.xpath('//a[@class="css-1i9riiu"]/text()').extract_first()

		try:
			p_price = response.xpath('//div[@class="css-18suhml"]/text()').extract()
			p_price = p_price[0]
		except:
			p_price = None

		p_num_reviews = response.xpath('//span[@class="css-1dz7b4e"]/text()').extract()
		p_num_reviews = p_num_reviews[0]
		p_num_reviews = p_num_reviews.replace('s', '')
		p_num_reviews = p_num_reviews.replace(' review', '')
		p_num_reviews = int(p_num_reviews)

		print ('Number of reviews: {}'.format(p_num_reviews))

		n_count = 0
		global n_count_tot

		item = SephoraItem()
		item['product'] = product
		item['p_id'] = p_id
		item['p_star'] = p_star
		item['brand_name'] = brand_name
		item['p_price'] = p_price
		item['p_category'] = p_category
		item['p_num_reviews'] = p_num_reviews 


		yield item

		n_count += 1
		n_count_tot += 1

		print ('='*50)
		print ('TOTAL NUMBER OF REVIEWS: {}'.format(int(p_num_reviews)))
		print ('ACTUAL NUMBER PULLED {}'.format(n_count))
		print ('TOTAL NUMBER PULLED {}'.format(n_count_tot))
		print ('='*50)




