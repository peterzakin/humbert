import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn

class Annotation(mongoMixIn):
    COLLECTION = 'Annotations'

    """
    Annotation:
    { 
    author,
    user_id,
    url,
    text
    }
    """
    
    @classmethod
    def add_annotation(klass, doc):
        return klass.mdbc().insert(doc)

    @classmethod
    def find_by_author(klass, author):
        spec = {'author':author}
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_user_id(klass, user_id):
        spec = {'user_id':user_id}
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_url(klass, url):
        spec = {'url':url}
        return klass.mdbc().find(spec)

    @classmethod 
    def get_stored_text_by_url(klass, url):
        annotation = klass.mdbc().find_one({ 'url': url})
        return annotation.get('text')

#Maybe we should use another model for each text
