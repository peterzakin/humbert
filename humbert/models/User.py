import sys
sys.path.append('humbert/')
import os
import constants
from lib.mongoHelper import mongoHelper
from pymongo import ASCENDING, DESCENDING

class User():
    connection = mongoHelper.connect()
    db = connection.core_humbert_data
    collection = db.Users
    
    @classmethod
    def add_user(klass, doc):
        user_id = klass.collection.insert(doc)
        return user_id

    @classmethod
    def get_user(klass, user_id):
        pass
