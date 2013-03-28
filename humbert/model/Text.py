import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn
from lib.diffbotHelper import DiffBot
class Text(mongoMixIn):
    COLLECTION = 'Texts'

    """
    Text:
    {
    url,
    text,
    author,

    }


    """
    @classmethod
    def add_text(klass, doc):
        return klass.mdbc().insert(doc)

    @classmethod
    def find_by_author(klass, author):
        spec = {'author':author}
        return klass.mdbc().find(spec)

    @classmethod
    def find_by_url(klass, url):
        spec = {'url':url}
        return klass.mdbc().find(spec)

    @classmethod
    def get_or_create_text_by_url(klass, url):
        spec = {'url':url}
        texts = klass.mdbc().find(spec)
        if texts.count() > 0:
            return texts[0]

        #get from diffbot. the text isnt stored here.
        #need to add error handling here.
        text = DiffBot.get_article(url)
        if text:
            doc = {
                'text': text,
                'url':url,
                }
            klass.add_text(doc)

        return text
