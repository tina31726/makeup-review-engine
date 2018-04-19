from bazaarvoice_api import BazaarvoiceAPI
from pymongo import MongoClient
import pandas as pd


    

MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/Amazondb" 
client = MongoClient(MONGO_HOST)
db = client.Amazondb


cursor = db.sephora.aggregate( [ {"$project" : { "p_id" : 1 , "_id" : 0 } } ] )
df =  pd.DataFrame(list(cursor))



# cursor = db.sephora.find({'p_category':'Eyeshadow'}, {"p_id": 1, "_id": 0})
# df =  pd.DataFrame(list(cursor))




i=0
data_container = []
data_dic={}
for n in range(len(df)):
    bazzarvoice = BazaarvoiceAPI('rwbw526r2e7spptqd2qzbkp7', str(df['p_id'].iloc[n]))
    for prod in bazzarvoice.get_product():
    	i+=1
    	print(n,i)
        data_dic['p_id']=df['p_id'].iloc[n]
        data_dic['Rating']=prod.Rating
        data_dic['ReviewText']=prod.ReviewText
        data_dic['UserNickname']=prod.UserNickname
        data_dic['LastModificationTime']=prod.LastModificationTime
        data_container.append(data_dic)
        data_dic={}
    if len(data_container)!=0:
        db.sephora_review_all.insert_many(data_container)
        print("successfully save in mongodb!")
        data_container = []
