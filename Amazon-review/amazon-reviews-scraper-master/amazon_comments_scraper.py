import argparse
import pickle
from core_extract_comments import *
from core_utils import *
from pymongo import MongoClient
import pickle

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

detect_list={}
def run(search, input_product_ids_filename,db):
    if input_product_ids_filename is not None:
        f=open(input_product_ids_filename,'rb')  
        product_ids=pickle.load(f) 
        f.close() 
        logging.info('{} product ids were found.'.format(len(product_ids)))
        i=0
        for product_id,count in product_ids[99:]:
            reviews = get_comments_with_product_id(product_id,count)
            logging.info('no.{},{} reviews found so far.'.format(i,len(reviews)))

            if len(reviews) !=0:
                db.Amazon_Eyeshadow_review.insert_many(reviews)
            if len(reviews)!= count:
                detect_list[product_id]=(count,len(reviews))

            i+=1
            # persist_comment_to_disk(reviews)
        f=open('detect.pickle','wb')  
        pickle.dump(detect_list,f,0)  
        f.close() 

    else:
        DEFAULT_SEARCH = 'BOTANIST ボタニカルシャンプー 490ml ＆ トリートメント 490g　モイストセット'
        search = DEFAULT_SEARCH if search is None else search
        reviews = get_comments_based_on_keyword(search=search)
        persist_comment_to_disk(reviews)


def get_script_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    input_product_ids_filename = args.input
    search = args.search
    return search, input_product_ids_filename

def mongodb():
    MONGO_HOST= "mongodb://user:0000@ec2-52-87-161-70.compute-1.amazonaws.com/Amazondb" 
    client = MongoClient(MONGO_HOST)
    db = client.Amazondb
    return db


def main():
    db=mongodb()
    search, input_product_ids_filename = get_script_arguments()
    run(search, input_product_ids_filename,db)


if __name__ == '__main__':
    main()
