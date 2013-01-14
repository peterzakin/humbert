import sys
sys.path.append('humbert/')
import constants
import requests
import simplejson

class DiffBot():

    @classmethod 
    def get_article(klass, article_url):
        url = "http://www.diffbot.com/api/article?"
        url += "token=" + constants.diffbot_key
        url += "&url=" + article_url
        response = requests.get(url)
        text = simplejson.loads(response.text)
        return text.get('text')
