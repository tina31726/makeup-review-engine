from flask import Flask, request, render_template
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import pandas as pd
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import numpy as np
from dateutil.parser import parse
from urllib.parse import quote 
import requests
import json
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os
import base64
import matplotlib.pyplot as plt
import pickle
from nltk.stem.porter import PorterStemmer
import nltk

stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tknzr = nltk.tokenize.TweetTokenizer()
    tokens = tknzr.tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

app = Flask(__name__)

MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/Amazondb" 
client = MongoClient(MONGO_HOST)
db = client.Amazondb

MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/twitterdb" 
client = MongoClient(MONGO_HOST)
db_t = client.twitterdb

Collection=['twitterdb','Amazondb']
Database=['Sephora_Eyeshadow','Amazon_Eyeshadow']
Database_review=['sephora_review','Amazon_Eyeshadow_review']

params = {
'spider_name': 'TweetScraper',
'start_requests': True,
'query':''
}


@app.route('/')
def index():

    return render_template('home.html')

@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
    msg=''

    pipeline = [{"$sort":{"p_num_reviews":-1}},{"$match":{"p_num_reviews":{"$gte": 1000 }} }]
    a=db.Sephora_Eyeshadow.aggregate(pipeline)


    #Duo Eyeshadow
    if request.method == 'POST':
        name = request.form['name'] # Get Form Fields
        if len(name.split('\"'))>2:
            sephora_review=review_search(0,name.split('\"')[1],db)
            amazon_review=review_search(1,name.split('\"')[1],db)
            params['query']=name
            response = requests.get('http://localhost:9080/crawl.json', params)
            data = json.loads(response.text)
            if response.status_code==200 and len( data['items'])!=0:
                twitter_review = db_t.tweet_collect.find({"keyword":name},{"text":1,"datetime":1,"_id":0})
                score=predict_score(twitter_review.clone())
                s_len,t_len,url=line_plot(twitter_review.clone(),sephora_review[1].clone())
                return render_template('twitter_submit.html',t_len=t_len,s_len=s_len, url=url,s_info=sephora_review[0],score=score)
            else:
                msg="Please enter complete product name"
                
        else:
            msg="Please include \"\" with your product like \"Kitten Eye Shadow\""       

             
       


    return render_template('twitter.html',msg=msg,products=a)


def line_plot(t_review,s_review):
    sephora =  pd.DataFrame(list(s_review))
    sephora.index = pd.DatetimeIndex(sephora['LastModificationTime'], inplace=True)
    sephora = sephora.sort_index()
    sephora.drop(['LastModificationTime'],axis=1,inplace=True)
    sephora.drop(['ReviewText'],axis=1,inplace=True)
    sephora['Sephora']=1 

    twitter =  pd.DataFrame(list(t_review))
    twitter.drop_duplicates(subset='text', keep='first', inplace=True)
    twitter.index = pd.DatetimeIndex(twitter['datetime'], inplace=True)
    twitter = twitter.sort_index()
    twitter.drop(['datetime'],axis=1,inplace=True)
    twitter.drop(['text'],axis=1,inplace=True)
    twitter['Twitter']=1 

    result = pd.concat([sephora.resample('M').count(), twitter.resample('M').count()], axis=1, join='inner')
    plot=result.plot()
    fig = plot.get_figure()
    tem=BytesIO()
    fig.savefig(tem, format='png')
    tem.seek(0) 
    plot_data = quote(base64.b64encode(tem.read()).decode())

    return len(sephora),len(twitter),plot_data


def review_search(no,name,db):
    
    pd = db[Database[no]].find_one({"product":name},{"p_id":1,"brand_name": 1, "product": 1,"p_star":1,'_id':0})
    if pd!=None:
        review=db[Database_review[no]].find({"p_id":pd['p_id']},{"ReviewText":1,"LastModificationTime": 1,'_id':0})
        if review!=None:
            return pd,review
        else:
            print(Database[no],"review is none")
    else:
        print(Database[no],"pd is none")
        
    return None

def predict_score(Review):
    twitter =  pd.DataFrame(list(Review))
    twitter.drop_duplicates(subset='text', keep='first', inplace=True)
    tfidf = pickle.load(open('tfidf.pkl','rb'))
    lr_regression = pickle.load(open('lr_regression.pkl','rb'))
    tfidf_train = tfidf.transform(twitter.text)
    pred = lr_regression.predict(tfidf_train)
    pred_rounded = np.round(pred)
    score=np.average(pred_rounded)
    return score



# hottest
@app.route('/hottest')
def hottest():
    pipeline = [{"$group": {"_id": "$p_category", "count": {"$sum": 1 } } },{"$sort":{"count":-1}},{"$match":{"count":{"$gte": 40 }} }]

    hottest = db.sephora.aggregate(pipeline)
    # hottest =  pd.DataFrame(list(cursor))
    if hottest.alive:
        return render_template('hottest.html', hottest=hottest)
    else:
        msg = 'No Category  Found'
        return render_template('hottest.html', msg=msg)

#Single Article
@app.route('/hottest/<string:_id>/')
def hottest_info(_id):
    current_top5_product_id = pickle.load(open(_id+'.pickle','rb'))
    url = plot_gradient(current_top5_product_id)
    
    return render_template('product_sort.html', product_info=url)


def plot_gradient(current_top5_product_id):
    url=[]
    print(current_top5_product_id)
    for test_id,value in current_top5_product_id:

        cursor = db.sephora.find({"p_id":test_id},{"brand_name": 1, "product": 1,"p_star":1,'_id':0})
        df_product =  pd.DataFrame(list(cursor))

        cursor = db.sephora_review_all.find({"p_id":test_id},{"LastModificationTime": 1,'_id':0})
        df_time =  pd.DataFrame(list(cursor))

        df_time.index = pd.DatetimeIndex(df_time['LastModificationTime'], inplace=True)
        df_time = df_time.sort_index()
        df_time.drop(['LastModificationTime'],axis=1,inplace=True)
        df_time['Count']=1 
        fig = plt.figure(figsize=(50, 50))
        plt.title(str(list(df_product.iloc[0]))+ 'total review: '+str(len(df_time)))
        print('increasing rate:{0} increasing period:{1} period:{2}'.format(value[0], value[1], value[2]))
        plt.plot(df_time['2017':'2018'].resample('M').count(), color='blue', label='resample count')
        tem=BytesIO()
        fig.savefig(tem, format='png')
        tem.seek(0) 
        plot_data = quote(base64.b64encode(tem.read()).decode())
        url.append(plot_data)
    return url


# Register Form Class
class SearchForm(Form):
    name = StringField('Eyeshadow name', [validators.Length(min=3, max=100)])



if __name__ == '__main__':
    app.run(debug=True)