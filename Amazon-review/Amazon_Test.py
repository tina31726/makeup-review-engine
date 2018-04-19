#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 12:46:22 2018

@author: YiChen
"""
from amazon.api import AmazonAPI
from collections import Counter, defaultdict, deque
from pymongo import MongoClient
import pandas as pd
import pickle
import errno
import json
import logging
import os
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

from banned_exception import BannedException




MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/Amazondb"  # assuming you have mongoDB installed locally                                             # and a database called 'twitterdb'
client = MongoClient(MONGO_HOST)
db = client.Amazondb

AMAZON_ACCESS_KEY = 'AKIAJNNFMSX5V3HLZB6Q'
AMAZON_SECRET_KEY='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'
AMAZON_ASSOC_TAG = 'tina31726-20'


amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

browse_id = amazon.browse_node_lookup(BrowseNodeId=11058281) ##Makeup_node = 11058281
#Browse_node_mining(browse_id)


#parent = [a for a in browse_id[0].ancestors]
Makeup_dir = defaultdict(int)
child = [a for a in browse_id[0].children]
len(child)
for n in child:
    print(n.name,n.id)
    if n.name != 'Body':
        Makeup_dir[n.name] = n.id


def Browse_node_mining(i):
    browse_id = amazon.browse_node_lookup(BrowseNodeId=i)
    try :
        child = [a for a in browse_id[0].children]
        print(browse_id[0].name,' has child',browse_id[0].id)
        Makeup_parents.append(browse_id[0].id)
        for n in child:
            if n.id not in Makeup_parents:
                Makeup_subdir[n.name] = n.id
    except:
        print(browse_id[0].name,'doesnt have child',browse_id[0].id)
        if browse_id[0].id not in Makeup_parents:           
            Makeup_subdir[browse_id[0].name] = browse_id[0].id
    

Makeup_subdir= dict()
Makeup_parents=[]
for k,v in Makeup_dir.items():
    Browse_node_mining(v)

    





products = amazon.search(SearchIndex='Beauty',BrowseNode=11058361) # eyeshadow node= 11058361
product = [r for r in products]



def get_soup(url):
    if 'amazon.com' not in url:
        url = 'https://www.amazon.com' + url
    nap_time_sec = 1
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
    }
    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers=header)
    assert out.status_code == 200
    soup = BeautifulSoup(out.content, 'html.parser')
    if 'captcha' in str(soup):
        raise BannedException('Your bot has been detected. Please wait a while.')
    return soup


def get_product_reviews_url(item_id):
    return 'https://www.amazon.com/product-reviews/{}/ref=' \
           'cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews' \
           '&showViewpoints=1&sortBy=helpful'.format(item_id)
           

product_dir={}
i=0
for n in product:
    product_reviews_link = get_product_reviews_url(n.asin)
    so = get_soup(product_reviews_link)
    
    cr_review_list_so = so.find(id='cm_cr-product_info')
    
    if cr_review_list_so is None:
        logging.info('No info for this item.')
        break
    
    info_list = cr_review_list_so.find_all(attrs={'class': 'a-text-left a-fixed-left-grid-col reviewNumericalSummary celwidget a-col-left'})
    
    if len(info_list) == 0:
        logging.info('No more info to unstack.')
        break
    

    p_num_reviews = info_list[0].find(attrs={'data-hook': 'total-review-count'}).text
    p_star = info_list[0].find(attrs={'data-hook': 'rating-out-of-text'}).text.split(" ")[0]
        
   
    product_dir['p_id']=n.asin
    product_dir['p_price']=float(n.price_and_currency[0])
    product_dir['product']=n.title
    product_dir['brand_name']=n.brand
    product_dir['p_num_reviews']=int(p_num_reviews.replace(',', ''))
    product_dir['p_star']=float(p_star)
    
    
    db.Amazon_Eyeshadow.insert_one(product_dir)
    product_dir={}
    print(i)
    i+=1
    
p_id_collection=[]
    
for doc in db.Amazon_Eyeshadow.find({},{"p_id": 1,"p_num_reviews":1, "_id": 0}):
    p_id_collection.append(tuple(doc.values()))

f=open('p_id.pickle','wb')  
pickle.dump(p_id_collection,f,0)  
f.close() 



cursor = db.Amazon_Eyeshadow.find({},{"p_id": 1,"p_num_reviews":1, "_id": 0})

#
#f=open('p_id.pickle','rb')  
#bb=pickle.load(f)  
#f.close() 
#
#page_range=int(count/10)
#if not count%10 == 0:
#    page_range+=1