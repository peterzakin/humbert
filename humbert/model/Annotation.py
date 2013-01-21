import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn

class Annotation(mongoMixIn):
    DB_NAME = 'core_humbert_data'
    COLLECTION = 'Annotations'
    
    @classmethod
    def add_annotation(klass, doc):
        return klass.mdbc().insert(doc)

    @classmethod
    def find_by_src(klass, src):
        spec = {'src':src }
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_author(klass, author):
        spec = {'author':author}
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_user_id(klass, user_id):
        spec = {'user_id':ObjectId(user_id)}
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_url(klass, url):
        spec = {'url':url}
        return klass.mdbc().find(spec)



#Maybe we should use another model for each text
