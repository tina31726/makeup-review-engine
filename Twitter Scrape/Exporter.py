# -*- coding: utf-8 -*-

import sys,getopt,got3,datetime,codecs
import pymongo
import json
from pymongo import MongoClient
import regex as re
import pprint
import csv
import pandas as pd

#For secert key or login info
#PATH = '/home/chester/Desktop/CS579_Proj/Twitter Scrape/private_key.txt'
PATH = './private_key.txt'



def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print("""\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n""")
		return




		
	
	try:

		opts, args = getopt.getopt(argv, "", ["username=", "since=", "until=", "querysearch=", "toptweets=", "maxtweets=","f=","DB"])
		tweetCriteria = got3.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			elif opt == '--f':
				tweetCriteria.setFileName = arg
			elif opt == '--DB':
				tweetCriteria.DB = True
	
		def get_setting(config_file):
		    """ Read the config_file and construct an instance of TwitterAPI.
		    Args:
		      config_file ... A config file in ConfigParser format with Twitter credentials
		    Returns:
		      An instance of TwitterAPI.
		    """
		    ls_lines = list()
		    dict_info = dict()
		    pat = r"[\d|\w|\W]+\s="
		    pat_content = r"'[\d|\w|\W]+'"
		    with open(config_file,'r') as text_handler:
		        ls_lines = text_handler.readlines()
		        for line in ls_lines:
		            dict_info[re.findall(pat,line)[0][:-2]] = re.findall(pat_content,line)[0][1:-1]
		    return dict_info
		def receiveBuffer(tweets):
			for t in tweets:
				outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
			outputFile.flush();
			print('More %d saved on file...\n' % len(tweets))
	
		def receiveBuffer_DB(tweets):
			for t in tweets:
				t.product_name = tweetCriteria.querySearch
				db.eyeshadow_tw.insert_one(vars(t))
			print('More %d saved on file...\n' % len(tweets))
			
		if hasattr(tweetCriteria,'FileName'):
			outputFile = codecs.open((tweetCriteria.setFileName+".csv"), "w+", "utf-8")
			print(outputFile)
			outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
		else:
			print("DB conecting....")
			dict_key =  get_setting(PATH)
			MONGO_HOST= "mongodb://{0}:{1}@ec2-52-87-161-70.compute-1.amazonaws.com/twitterdb".format(dict_key['mongo_db_user'],dict_key['mongo_db_password']) # assuming you have mongoDB installed locally
			client = MongoClient(MONGO_HOST)
			db = client.twitterdb
			
		print('Searching...\n')
		
	
		if hasattr(tweetCriteria,'DB'):
			got3.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer_DB)
		else:
			got3.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		if hasattr(tweetCriteria,'FileName'):
			outputFile.close()
			print('Done. Output file generated '+tweetCriteria.setFileName+'.csv')
		else:
			print("Upload End")
			client.close()
		
		

			
if __name__ == '__main__':
#    main(['--querysearch', 'beautyblender', '--since', '2017-12-12','--until','2018-02-16', '--f', 'hello'])
    main(['--querysearch', 'beautyblender', '--since', '2017-12-12','--until','2018-02-16', '--DB','--maxtweets','50'])
