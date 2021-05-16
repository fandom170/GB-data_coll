# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.utils.python import to_bytes


class InstagramPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["instagramm_data"]

    def process_item(self, item, spider):
        collection_name = f"{spider.name}_{item['data_type']}_{item['user_id']}"
        collection = self.db[collection_name]
        inst_data = {}
        inst_data['_id'] = item['linked_acc_id']
        inst_data['user_id'] = item['user_id']
        inst_data['user_name'] = item['user_name']
        inst_data['linked_acc_name'] = item['linked_acc_name']
        inst_data['full_name'] = item['full_name']
        inst_data['profile_pic_url'] = item['profile_pic_url']
        inst_data['user_data'] = item['user_data']
        query = {'_id': inst_data['_id']}
        collection.update_one(query, {'$set': inst_data}, upsert=True)
        return item
