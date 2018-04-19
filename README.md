# CS579_Project
## Descrption
Here's the reputation Eningee,
Which provide user to search partucular product catogory.
It will return the popular prodcuts candidate. Also return the tweets talked about the items.


## Data Collection
### Sephora
We use sephora dictionary and sephora_review dictionary to get all product and reviews, that sephora is used Scrapy, sephora_review is used bazaarvoice_api.
### Twitter
We use Twitter_Spider dictionary as scrapy framework to collect twitter data, this is real-time scrapy, please enter scrapyrt not scrapy
### Amazon
We use Amazon-review dictionary to collect all eyeshadow product name and reviews. Inside the dictionary, there is Amazon_Test, which used AmazonAPI to collect top 100 eyeshadow product name, the other dictionary, amazon-reviews-scraper-master, which used beautiful soap to collect all reviews in each product.

## Data Collection
Flask dictionary is used to implement data deployment, enter python app.py to activate flask web application. There are two features you can use. One is Twitter tab, which can enter interesting product name first and get review time series and Twitter predicted rating. The other one is checking hottest product which got more and more reviews recently.
Notice:Categories you can check are only in .pickle in dictionary



???-Good catogory

Amazon, Sephora-All item catogory
reference scraper on git
https://github.com/adamlwgriffiths/amazon_scraper
https://github.com/jernchr11/Sephora/tree/master/tutorial
### Claning Data
### Scrape youtube descrption
### User follower and user network


## Modeling
### Find items set
### Analysis quantify reputation for user
### Sentment Analysis for tweets


## Visualize Deploy
### Show related tweets
### Graph
### Web application
