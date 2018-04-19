#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:23:10 2018

@author: YiChen
"""
from pymongo import MongoClient
import pandas as pd
from collections import defaultdict
import pickle

MONGO_HOST= "mongodb://user:0000@ec2-34-205-144-84.compute-1.amazonaws.com/Amazondb" 
client = MongoClient(MONGO_HOST)
db = client.Amazondb



pipeline = [{"$group": {"_id": "$brand_name", "count": {"$sum": 1 } } }]
cursor = db.sephora.aggregate(pipeline)
df =  pd.DataFrame(list(cursor))

cursor = db.sephora_check.find({})
df_check =  pd.DataFrame(list(cursor))
del df_check['_id']

check_set=set(df_check['brand_name'])
test_set=set(df['_id'])
miss_set = check_set-test_set

df_dic = df.set_index('_id').T.to_dict('records')[0]
df_check_dic = df_check.set_index('brand_name').T.to_dict('records')[0]

#wrong_num_product= defaultdict(list)
wrong_num_product = list(miss_set)

for k,v in df_dic.items():
    if v!= df_check_dic[k]:
        wrong_num_product.append(k)
#        wrong_num_product[k].append(v)
#        wrong_num_product[k].append(df_check_dic[k])
        
pickle.dump(wrong_num_product, open( "wrong_num_product.p", "wb" ) )