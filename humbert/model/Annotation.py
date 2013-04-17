import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn


"""
Annotation is the user's copy of a text. It includes his comments.

"""


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
    def make_annotation(klass, text_info, user_id):
        #main method for creating annotations
        doc = {
            'text_info': text_info,
            'user_id':user_id,
            'text_id':text_info.get('_id')
            }

        return klass._add_annotation(doc)

    @classmethod
    def add_comment_to_annotation(klass, annotation_id, comment):
        if comment.__class__.__name__ != 'Comment':
            raise Exception('you stupid shit you didn not pass in a comment obj')
        
        doc = { 'comment':comment }
        return klass.update(annotation_id, doc)
        
    @classmethod
    def _add_annotation(klass, doc):
        return klass.mdbc().insert(doc) 

    @classmethod
    def find_by_user_id(klass, user_id):
        spec = {'user_id':user_id}
        return klass.mdbc().find(spec)

    @classmethod 
    def get_stored_text_by_url(klass, url):
        annotation = klass.mdbc().find_one({ 'url': url})
        return annotation.get('text')

class Comment():
    def __init__(self, start_span, end_span, text):
        self.start_span = start_span
        self.end_span = end_span
        self.text = text
