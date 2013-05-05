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
    user_id,
    text_id,
    comments[]
    }
    """
    @classmethod
    def save_annotation(klass, user_id, text_id, comments):
        doc = {
            'user_id': user_id,
            'text_id': text_id,
            'comments': comments,
            }
        response =  klass._add_annotation(doc)
        import pdb; pdb.set_trace()
        return response

    @classmethod
    def _add_annotation(klass, doc):
        return klass.mdbc().insert(doc) 

    @classmethod
    def find_by_user_id(klass, user_id):
        spec = {'user_id':user_id}
        return klass.mdbc().find(spec)
