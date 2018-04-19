import logging
import re

import validators

from core_utils import get_soup, extract_product_id


# https://www.amazon.co.jp/product-reviews/B00Z16VF3E/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1

def get_product_reviews_url(item_id, page_number):
    return 'https://www.amazon.com/product-reviews/{}/ref=' \
           'cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews' \
           '&showViewpoints=1&sortBy=helpful&pageNumber={}'.format(
        item_id, page_number)


def get_comments_based_on_keyword(search):
    logging.info('SEARCH = {}'.format(search))
    url = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + \
          search + '&rh=i%3Aaps%2Ck%3A' + search
    soup = get_soup(url)
    items = []
    for a in soup.find_all('a', class_='s-access-detail-page'):
        if a.find('h2') is not None and validators.url(a.get('href')):
            name = str(a.find('h2').string)
            link = a.get('href')
            items.append((link, name))
    logging.info('Found {} items.'.format(len(items)))
    for (link, name) in items:
        logging.debug('link = {}, name = {}'.format(link, name))
        product_id = extract_product_id(link)
        count=1000
        get_comments_with_product_id(product_id,count)


def get_comments_with_product_id(product_id,count):
    reviews = list()
    if product_id is None:
        return reviews
    if not re.match('^[A-Z0-9]{10}$', product_id):
        return reviews
    page_range=int(count/10)
    if not count%10 == 0:
        page_range+=1

    k=0
    for page_number in range(1,page_range+1):
        product_reviews_link = get_product_reviews_url(product_id, page_number)
        so = get_soup(product_reviews_link)

        cr_review_list_so = so.find(id='cm_cr-review_list')

        if cr_review_list_so is None:
            logging.info('No reviews for this item.')
            break

        reviews_list = cr_review_list_so.find_all(attrs={'class': 'a-section review'})

        if len(reviews_list) == 0:
            logging.info('No more reviews to unstack.')
            break

        for review in reviews_list:
            rating = review.find(attrs={'data-hook': 'review-star-rating'}).attrs['class'][2].split('-')[-1]
            body = review.find(attrs={'data-hook': 'review-body'}).text
            title = review.find(attrs={'data-hook': 'review-title'}).text
            date = review.find(attrs={'data-hook': 'review-date'}).text

            logging.info('***********************************************')
            logging.info('no.review = ' + str(k)+ " /"+str(count))
            logging.info('TITLE    = ' + title)
            logging.info('RATING   = ' + rating)
            logging.info('CONTENT  = ' + body)
            logging.info('DATE  = ' + date)
            logging.info('***********************************************\n')
            reviews.append({'p_id': product_id,
                            'title': title,
                            'rating': rating,
                            'ReviewText': body,
                            'LastModificationTime': date
                            })
            k+=1
    return reviews
