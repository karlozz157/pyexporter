#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

class MongoDataSource(object):
    def __init__(self):
        self.__connect()

    def __del__(self):
        self.__disconnect()

    def __connect(self):
        self.client = pymongo.MongoClient('localhost')

    def __disconnect(self):
        self.client.logout()

    def get_database_names(self):
        """ get database names """
        return self.client.database_names()

    def get_collections(self, database):
        """ get collections """
        if database not in self.get_database_names():
            raise Exception('The database %s doesn\'t exist!' % database)
        return self.client[database].collection_names()

    def get_data_from_collection(self, database, collection):
        """ get data from collection """
        if collection not in self.get_collections(database):
             raise Exception('The collection %s doesn\'t exist!' % collection)
        results = self.client[database][collection].find()
        return [result for result in results]

