# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import scrapy

class SephoraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_name = scrapy.Field()
    # n_product = scrapy.Field() //use when collecting brand_list to check and comment below
    product = scrapy.Field()
    p_id = scrapy.Field()
    p_star = scrapy.Field()
    p_category = scrapy.Field()
    p_price = scrapy.Field()
    p_num_reviews = scrapy.Field()