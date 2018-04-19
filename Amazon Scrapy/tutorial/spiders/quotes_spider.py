import scrapy
import urllib
from collections import defaultdict
import re
import json
from pymongo import MongoClient
MONGO_HOST= "mongodb://USERNAME:PASSWORD@ec2-34-205-144-84.compute-1.amazonaws.com/Amazondb"  

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    urls_list = ['https://www.amazon.com/gp/search/other/ref=sr_in_1_-2?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=%23&ie=UTF8&qid=1519434978'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_a_1?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=a&ie=UTF8&qid=1519442908'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_b_A?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=b&ie=UTF8&qid=1519442948'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_c_B?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1519442974'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_d_C?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=d&ie=UTF8&qid=1519442988'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_e_D?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=e&ie=UTF8&qid=1519443033'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_f_E?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=f&ie=UTF8&qid=1519443070'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_g_F?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=g&ie=UTF8&qid=1519443080'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_h_G?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=h&ie=UTF8&qid=1519443100'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_i_H?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=i&ie=UTF8&qid=1519443112'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_j_I?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=j&ie=UTF8&qid=1519443124'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_k_J?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=k&ie=UTF8&qid=1519443136'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_l_K?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=l&ie=UTF8&qid=1519443156'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_m_L?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=m&ie=UTF8&qid=1519443171'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_n_M?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=n&ie=UTF8&qid=1519443182'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_o_N?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=o&ie=UTF8&qid=1519443192'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_p_O?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=p&ie=UTF8&qid=1519443202'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_q_R?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=q&ie=UTF8&qid=1519443306'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_r_Q?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=r&ie=UTF8&qid=1519443222'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_s_R?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=s&ie=UTF8&qid=1519443306'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_t_S?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=t&ie=UTF8&qid=1519443346'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_u_T?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=u&ie=UTF8&qid=1519443357'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_v_U?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=v&ie=UTF8&qid=1519443368'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_w_V?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=w&ie=UTF8&qid=1519443378'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_x_W?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=x&ie=UTF8&qid=1519443389'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_y_X?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=y&ie=UTF8&qid=1519443401'
                  ,'https://www.amazon.com/gp/search/other/ref=sr_in_z_Y?rh=i%3Abeauty%2Cn%3A3760911%2Cn%3A%2111055981%2Cn%3A11058281&bbn=11058281&pickerToList=lbr_brands_browse-bin&indexField=z&ie=UTF8&qid=1519443523']
    
    proxy='https://api.proxycrawl.com/?token=YOURTOKEN&url='
    for i,url in enumerate(urls_list):
        test = urllib.parse.quote(url)
        urls_list[i]=proxy+test
        
    start_urls = urls_list
    
    def parse(self, response):
#         print('start!')
#         brand_link = response.xpath('//div[@class="a-row a-spacing-base"]/a').extract()
#         for i in brand_link:
#             print(i)

        brand = response.xpath('//a[@class="a-link-normal"]//@title').extract()
        num_list = response.xpath('//span[@class="narrowValue"]/text()').extract()
        outer = re.compile("(?!\()\d{1},\d{3}|\d{1,3}(?<!\))")
        brand_num = outer.findall(str(num_list))
                
        client = MongoClient(MONGO_HOST)
        db = client.Amazondb
        if len(brand_num)== len(brand):
            for i, num in enumerate(brand_num):
                brand_dir={}
                numm = int(num.replace(',', ''))
                brand_dir['brand']=brand[i]
                brand_dir['number']=numm
                if numm>3:
                    print(brand_dir)
                    db.brand_list.insert_one(brand_dir)
                else:
#                    print(brand[i])
                    db.brand_remove_list.insert_one(brand_dir)

        else:
            print('brand_num and brand not match')
            print(num_list)
            print(brand_num)
            
