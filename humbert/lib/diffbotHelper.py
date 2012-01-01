import sys
sys.path.append('humbert/')
import constants
import requests
import simplejson
from django.utils.html import escape

class DiffBot():

    @classmethod 
    def get_article_info(klass, article_url):
        url = "http://www.diffbot.com/api/article?"
        url += "token=" + constants.diffbot_key
        url += "&url=" + article_url
        url += "&html=true"
        response = requests.get(url)
        text_info = simplejson.loads(response.text)
        return text_info
