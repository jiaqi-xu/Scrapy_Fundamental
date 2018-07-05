# -*- coding: utf-8 -*-
from pymongo import MongoClient

'''
Database Operation Class
contains basic CRUD operation
'''


class DB_Helper(object):

    def __init__(self):
        '''
        initialize the mongodb connection in constructor
        '''

        client = MongoClient() # connect to default host and port mongodb://localhost:27017/
        self.db_xici_proxy = client.xici_proxy
        self.collection_proxy = self.db_xici_proxy.ips_collection

    def return_xici_proxy(self):
        return self.db_xici_proxy

    def update(self, *condition):
        '''
        :param condition:
        :return:
        '''
        result = self.collection_proxy.update(*condition)
        if result:
            return True
        else:
            return False

    def find(self, *condition):
        '''
        :param condition: find query
        :return:
        '''
        result = self.collection_proxy.find_one(*condition)
        print result
        if result:
            return True
        else:
            return False

    def delete(self, *condition):
        '''
        :param condition:
        :return:
        '''
        result = self.collection_proxy.remove(*condition)
        print result
        if result:
            return True
        else:
            return False

    def insert(self, *condition):
        '''
        :param condition:
        :return:
        '''
        result = self.collection_proxy.insert(*condition)
        print result
        if result:
            return True
        else:
            return False



