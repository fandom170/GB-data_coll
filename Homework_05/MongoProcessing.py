from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib


class MongoProcessing():
    def __init__(self,):
        self.client = MongoClient('localhost', 27017)
        self.db = None
        self.collection = None

    def db_init(self, db_name):
        self.db = self.client[db_name]

    def collection_init(self, site):
        """Init Mongo DB collection. Duplicate check is not performed as Mongo DB does not create duplicates"""
        self.collection = self.db[site]

    def add_new_entries_mvideo(self, data):
        """Function adds elements from data to mongo database. Duplicate check is performed by link to job which
        should be unique for each job"""
        counter = 0
        id_list = []
        for item in self.collection.find():
            id_list.append(item['_id'])

        for elem in data:
            hash_total = self.hash_calculation_mvideo(elem)
            elem['_id'] = hash_total
            try:

                self.collection.insert_one(elem)
            except DuplicateKeyError:
                filter = {'_id': elem['_id']}
                update = {'$set': {'Price': elem['Price']}}
                self.collection.update(filter, update)
                continue
            counter += 1
        return counter

    def hash_calculation_mvideo(self, elem):
        line = elem['Name'] + elem['VendorName'] + elem['Category']
        hash_total = str((hashlib.md5(line.encode())).hexdigest())
        return hash_total


