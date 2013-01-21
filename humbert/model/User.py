import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn

class User(mongoMixIn):
    DB_NAME = 'core_humbert_data'
    COLLECTION = 'Users'
    
    #def __init__(self, doc):
     #   self.__dict__.update(doc)

    @classmethod
    def add_user(klass, doc): 
        return klass.mdbc().insert(doc)
