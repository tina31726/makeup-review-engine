# -*- coding: utf-8 -*-

import re

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
PATH = './private_key.txt'
dict_key =  get_setting(PATH)



# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'TweetScraper'

# settings for spiders
BOT_NAME = 'TweetScraper'
LOG_LEVEL = 'INFO'
DOWNLOAD_HANDLERS = {'s3': None,} # from http://stackoverflow.com/a/31233576/2297751, TODO

SPIDER_MODULES = ['TweetScraper.spiders']
NEWSPIDER_MODULE = 'TweetScraper.spiders'
ITEM_PIPELINES = {
    # 'TweetScraper.pipelines.SaveToFilePipeline':100,
    'TweetScraper.pipelines.SaveToMongoPipeline':100, # replace `SaveToFilePipeline` with this to use MongoDB
}

# settings for where to save data on disk
SAVE_TWEET_PATH = './Data/tweet/'
SAVE_USER_PATH = './Data/user/'

# settings for mongodb
# MONGODB_HOST = "mongodb://{0}:{1}@ec2-52-87-161-70.compute-1.amazonaws.com".format(dict_key['mongo_db_user'],dict_key['mongo_db_password']) # assuming you have mongoDB installed locally
MONGODB_HOST = "ec2-52-87-161-70.compute-1.amazonaws.com"
MONGODB_PORT = 27017
MONGODB_USER = dict_key['mongo_db_user']
MONGODB_PASSWORD = dict_key['mongo_db_password']
MONGODB_DB = "twitterdb"        # database name to save the crawled data
MONGODB_TWEET_COLLECTION = "tweet_collect" # collection name to save tweets
MONGODB_USER_COLLECTION = "user_collect"   # collection name to save users

