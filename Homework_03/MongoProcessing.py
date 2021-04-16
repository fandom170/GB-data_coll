from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib


class MongoProcessing():
    def __init__(self,):
        self.client = MongoClient('localhost', 27017)
        self.db = None
        self.collection = None
        self.usd = 75.75
        self.euro = 90.76
        self.kzt = 5.68

    def db_init(self, db_name):
        self.db = self.client[db_name]

    def collection_init(self, site):
        """Init Mongo DB collection. Duplicate check is not performed as Mongo DB does not create duplicates"""
        if site == "hh":
            collection_name = 'head_hunter'
        elif site == "sj":
            collection_name = 'super_job'
        else:
            collection_name = 'something_else'
        self.collection = self.db[collection_name]


    def add_new_entries(self, data):
        """Function adds elements from data to mongo database. Duplicate check is performed by link to job which
        should be unique for each job"""
        counter = 0
        id_list = []
        for job in self.collection.find():
            id_list.append(job['_id'])

        for elem in data:
            elem_id = elem['link'].split('/')[-1]
            if elem_id in id_list:
                continue
            new_elem = elem
            hash_total = str((hashlib.md5(elem['title'].encode())).hexdigest())
            new_elem['_id'] = elem_id + hash_total
            try:
                self.collection.insert_one(new_elem)
            except (DuplicateKeyError):
                continue
            counter += 1
        return counter

    def currency_converting(self):
        """function converts all data in database to Rubles"""
        # query = ({"$and": [{"currency": {"$ne":"руб."}}, {"$or":[{"max_salary": None}, {"min_salary": None}]}]})
        query = ({"currency": {"$ne": "руб."}})
        for elem in self.collection.find(query):
            if elem['currency'] is None or (elem['min_salary'] is None and elem['max_salary'] is None):
                continue
            else:
                elem['min_salary'] = self.currency_multiplying(elem['currency'], elem['min_salary'])
                elem['max_salary'] = self.currency_multiplying(elem['currency'], elem['max_salary'])
                elem['currency'] = "руб."

    def currency_multiplying(self, currency, value):
        """Function multiplies salary value to appropriate currency"""
        if currency == 'KZT':
            multiplier = self.kzt
        elif currency == 'USD':
            multiplier = self.usd
        elif currency == 'EUR':
            multiplier = self.euro
        else:
            multiplier = 1
        salary = None if value is None else value * multiplier
        return salary

    def find_data_by_salary(self, salary_value):
        """Search jobs in database by month salary value"""
        result = []
        query = {"$or": [{"min_salary": {"$gte": salary_value}}, {"max_salary": {"$gte": salary_value}}]}

        for elem in self.collection.find(query, {"title":1, "_id": 1}):
            result.append(elem)
        return result





