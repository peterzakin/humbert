import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import MongoClient, Connection
from bson.objectid import ObjectId


class mongoMixIn(object):

    DB_NAME = "heroku_app10941623"
 
    @classmethod 
    def connect(klass):
        if constants.ENVIRONMENT == 'test':
            return klass._connect_on_dev()
        else:
            return klass._connect_on_prod()

    @classmethod
    def _connect_on_prod(klass):
        mongo_uri = constants.mongo_uri
        connection = Connection(mongo_uri)
        return connection 
    
    @classmethod
    def _connect_on_dev(klass):
        connection = MongoClient()
        return connection 

    @classmethod
    def mdbc(klass):
        connection = klass.connect()
        db = connection[klass.DB_NAME]
        collection = db[klass.COLLECTION]
        return collection
    
    """ functional """

    @classmethod
    def update(klass, obj_id, doc):
        if hasattr(klass, klass.COLLECTION, None):
            spec = { "_id": obj_id }
            return klass.mdbc().update(spec, doc, upsert=True, safe=True)
        else:
            raise Exception("no collection, asshole")

    @classmethod
    def find_by_id(klass, obj_id):
        spec = { "_id":obj_id }
        return klass.mdbc().find_one(spec)

    #to be used when we want to save the instance to db
    def save(self):
        mongoMixIn.update(self.id, self.__dict__)
        
    #helpers
    @classmethod
    def _create(klass, **kwargs):
        doc = kwargs
        model_id = klass.mdbc().insert(doc)
        return model_id
