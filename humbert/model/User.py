from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth.models import User
import requests
import simplejson

class Profile(User):
    fb_id = models.IntegerField(default=0)
    access_token = models.CharField(max_length=200)

    class Meta:
        app_label = "humbert"
    
    @classmethod
    def create_new_fb_user(klass, fb_id, access_token):
        if fb_id not in [None, ''] and access_token not in [None, '']:
            fb_user = klass.get_fb_user_dict(access_token)
            last_name = fb_user.get('last_name')
            first_name = fb_user.get('first_name')
            username= fb_user.get('username')
            user = klass(fb_id=fb_id, username=username, access_token=access_token, first_name=first_name, last_name=last_name)
            user.save()
            return user

    @classmethod
    def get_fb_user_dict(klass, access_token):
        #make a server side query to fb api and get the user info
        url = 'https://graph.facebook.com/me?access_token=%s' % (access_token)
        user_dict = simplejson.loads(requests.get(url).text)
        print user_dict
        return user_dict
