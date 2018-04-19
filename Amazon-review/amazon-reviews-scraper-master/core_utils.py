import errno
import json
import logging
import os
import re
from time import sleep
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import urllib
from banned_exception import BannedException

OUTPUT_DIR = 'comments'
proxy='https://api.proxycrawl.com/?token=d0hO_cRvGbNMwPPu4l1kNw&url='

def get_reviews_filename(product_id):
    filename = os.path.join(OUTPUT_DIR, '{}.json'.format(product_id))
    exist = os.path.isfile(filename)
    return filename, exist


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def persist_comment_to_disk(reviews):
    if len(reviews) == 0:
        return False
    product_id_set = set([r['product_id'] for r in reviews])
    assert len(product_id_set) == 1, 'all product ids should be the same in the reviews list.'
    product_id = next(iter(product_id_set))
    output_filename, exist = get_reviews_filename(product_id)
    if exist:
        return False
    mkdir_p(OUTPUT_DIR)
    with open(output_filename, 'w') as fp:
        json.dump(reviews, fp, sort_keys=True, indent=4, ensure_ascii=False)
    return True


def extract_product_id(link_from_main_page):
    # e.g. B01H8A7Q42
    p_id = -1
    tags = ['/dp/', '/gp/product/']
    for tag in tags:
        try:
            p_id = link_from_main_page[link_from_main_page.index(tag) + len(tag):].split('/')[0]
        except:
            pass
    m = re.match('[A-Z0-9]{10}', p_id)
    if m:
        return m.group()
    else:
        return None


def get_soup(url):
    if 'amazon.com' not in url:
        url = 'https://www.amazon.com' + url
    nap_time_sec = 1
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
    ua = UserAgent()

    test = urllib.parse.quote(url)
    url_proxy=proxy+test

    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers={'user-agent':str(ua.random)})
    assert out.status_code == 200
    soup = BeautifulSoup(out.content, 'html.parser')
    if 'captcha' in str(soup):
        # logging.debug('Your bot has been detected. Please wait a while.')
        # get_soup(url)
        raise BannedException('Your bot has been detected. Please wait a while.')
    return soup
