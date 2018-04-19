# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy import log 
from scrapy.conf import settings
from pymongo import MongoClient

class MongoDBPipeline(object):

    def __init__(self):
    	client = MongoClient(settings['MONGO_HOST'])
    	db = client.Amazondb
    	self.collection = db.sephora_check # mongo db collection name 

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
