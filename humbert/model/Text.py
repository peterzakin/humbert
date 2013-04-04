import sys
sys.path.append('humbert/')
import os
import constants
from pymongo import ASCENDING, DESCENDING
from mongoMixIn import mongoMixIn
from lib.diffbotHelper import DiffBot
import re

class Text(mongoMixIn):
    COLLECTION = 'Texts'

    """
    Text:
    {
    url,
    text,
    author,
    title
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
        text_info = DiffBot.get_article_info(url)
        if text_info:
            doc = {
                'text': Text.prepare_text(text_info.get('html')),
                'url':text_info.get('url'),
                'author':text_info.get('author'),
                'title':text_info.get('title')
                }
            klass.add_text(doc)
            text_info = doc
        return text_info

    @classmethod
    def prepare_text(klass, html):
        pattern ="(?<=>)(?!<).*?(?=.?<)[^<>]?"
        return re.sub(pattern, repl, html, flags=re.DOTALL)

count = 0    
def repl(matchobject):
    text = matchobject.group(0)
    return re.sub("([^\s]*?) | \s+", subrepl, text)

def subrepl(matchobject):
    match = matchobject.group(0)
    global count
    output = "<span id=a%s>%s</span>" % (count, match)
    count = count + 1
    return output
