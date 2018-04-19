from flask import Flask, request, render_template
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import pandas as pd


app = Flask(__name__)
# app.config.update(
#     MONGO_HOST='ec2-52-87-161-70.compute-1.amazonaws.com',
#     MONGO_PORT=27017,
#     MONGO_USERNAME='user',
#     MONGO_PASSWORD='0000',
#     MONGO_DBNAME='Amazondb'
# )
# mongo = PyMongo(app)

MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/Amazondb" 
client = MongoClient(MONGO_HOST)
db = client.Amazondb

@app.route('/')
def home_page():
	pipeline = [{"$group": {"_id": "$p_category", "count": {"$sum": 1 } } }]
	cursor = db.sephora.aggregate(pipeline)
	df =  pd.DataFrame(list(cursor))
	return render_template('index.html', name='test', data=df.to_html())

    # online_users = db.sephora.find({'brand_name': 'Yves Saint Laurent'})
    # df =  pd.DataFrame(list(online_users))



# @app.route('/query', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['category id']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # 如果请求访求是 GET 或验证未通过就会执行下面的代码
#     return render_template('login.html', error=error)
