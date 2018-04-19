
import json
from math import floor
from fake_useragent import UserAgent

import requests




class BazaarvoiceAPI:

    api_key = None
    productt_id = None

    reviews_list = []

    def __init__(self, api_key, productt_id):
        self.api_key = api_key
        self.productt_id = productt_id

        if not isinstance(productt_id, str):
            raise Exception('You must provide string in productt_id var, got: ' + str(type(productt_id)))

        if 'http://' in productt_id:
            raise Exception('You cant provide url')

    def make_url(self):
        productt_id = self.productt_id
        api_key = self.api_key

        base_url = 'https://api.bazaarvoice.com/data/'

        start_url = base_url + "reviews.json?apiversion=5.4&passkey=" + api_key + \
                    "&Sort=Helpfulness%3Adesc&Limit=100&Include=Products%2CComments&Stats=Reviews&Filter=ProductId:" + productt_id + '&offset=0'

        return start_url

    # Check if the response received is OK
    @staticmethod
    def _check_response(json_data):
        has_errors = bool(json_data['HasErrors'])
        if has_errors:
            errors = json_data['Errors']

            errors_str_handler = ''
            for error in errors:
                errors_str_handler += '\n' + error['Message']

            raise Exception('Bad response: ' + errors_str_handler)

    def get_product(self):
        products_url = self.make_url()
        print(products_url)

        products = self._get_reviews(products_url)
        for review_list in products:
            for rev in review_list:
                review_object = Review(rev)

                yield review_object

    def _get_reviews(self, products_url):
        ua = UserAgent()
        products_content = requests.get(products_url, headers={'user-agent':str(ua.random)}).text
        products_json = json.loads(products_content)

        self._check_response(products_json)

        product_max_offset = int(floor(int(products_json['TotalResults']) / 100.0)) * 100
        for i in range(0, product_max_offset + 100, 100):
            offset = i

            products_url = self._make_next_page_url(offset, products_url)

            yield products_json['Results']

            products_content = requests.get(products_url, headers={'user-agent':str(ua.random)}).text
            products_json = json.loads(products_content)

    @staticmethod
    def _make_next_page_url(offset, product_url):
        new_offset = offset + 100

        current_offset_str = 'offset=%d' % offset
        new_offset_str = 'offset=%d' % new_offset

        new_reviews_url = product_url.replace(current_offset_str, new_offset_str)

        return new_reviews_url

class Review(object):
    def __init__(self, review_dict):
        for k, v in review_dict.items():
            self.__setattr__(k, v)