# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookCollectPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["bookCollect"]

    def process_item(self, item, spider):
        collection = self.db[spider.name]

        book_data = {}
        book_data['_id'] = self.hash_calc(str(item['book_name']) +
                                          str(item['book_link']) +
                                          str(self.authors_to_string(item['authors'])))
        book_data['book_name'] = item['book_name'].strip()
        book_data['authors'] = item['authors']
        book_data['main_price'] = self.price_extract(item['main_price'])
        book_data['bargain_price'] = self.price_extract(item['bargain_price'])
        book_data['currency'] = item['currency']
        book_data['book_rate'] = item['book_rate']
        book_data['book_link'] = item['book_link']

        query = {'_id': book_data['_id']}
        collection.update_one(query, {'$set': book_data}, upsert=True)

        return item

    def hash_calc(self, item):
        return str((hashlib.md5(item.encode())).hexdigest())

    def authors_to_string(self, authors):
        line = ""
        for author in authors:
            line += author + ' '

    def price_extract(self, value):
        if value:
            line = [int(s) for s in value.split() if s.isdigit()]
            return line[0]
        return None

