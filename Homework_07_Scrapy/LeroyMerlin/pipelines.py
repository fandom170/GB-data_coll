# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from scrapy.utils.python import to_bytes


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["LeroyMerlin"]

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        goods_data = {}
        goods_data['_id'] = self.hash_calc(item['item_link'])
        goods_data['name'] = item['item_name']
        goods_data['price'] = item['item_price']
        goods_data['link'] = item['item_link']
        goods_data['params'] = self.get_item_params(item['item_data_keys'], item['item_data_vals'])
        query = {'_id': goods_data['_id']}
        collection.update_one(query, {'$set': goods_data}, upsert=True)
        return item

    def get_item_params(self, definitions, params):
        item_params = {}
        for i in range(len(definitions)):
            item_params[definitions[i]] = params[i] if not params[i].isdigit() else float(params[i])
        return item_params

    def hash_calc(self, item):
        return str((hashlib.md5(item.encode())).hexdigest())


class LeroymerlinPhotosPipeline (ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['item_photos']:
            for img in item['item_photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        """take links"""
        if results:
            item['item_photos'] = [it[1] for it in results if it[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        """Generates hash and return file name and path to it."""
        folder_name = item['item_name']\
            .replace('/', '')\
            .replace(',', '')\
            .replace('.', '')

        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        path_to_saved_file = f'full/{folder_name}/{image_guid}.jpg'
        return path_to_saved_file

    def thumb_path(self, request, thumb_id, response=None, info=None):
        line = response.url.split('/')[-1]
        goods_id = line.split('.')[0]
        thumb_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'thumbs/{thumb_id}/{goods_id}/{thumb_guid}.jpg'
