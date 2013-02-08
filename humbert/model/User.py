from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth.models import User
import requests
import simplejson
import constants 
from django.http import QueryDict
from django.shortcuts import redirect
import logging

from lib.Errors import Errors

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
            profile = klass(fb_id=fb_id, username=username, access_token=access_token, first_name=first_name, last_name=last_name)
            profile.save()
            return profile

    @classmethod
    def get_fb_user_dict(klass, access_token):
        #make a server side query to fb api and get the user info
        url = 'https://graph.facebook.com/me?access_token=%s' % (access_token)
        response = requests.get(url).text
        user_dict = simplejson.loads(response)
        
        import pdb; pdb.set_trace()

        if user_dict.get('error') is not None:
           # klass.handle_fb_errors(user_dict.get('error'))
            return redirect('/logout')
        logging.info(user_dict)
        return user_dict

    @classmethod
    def get_profile(klass, user):
        return Profile.objects.get(id=user_id)
    
    @classmethod
    def init_session(klass, request):
        if 'profile' not in request.session:
            request.session['profile'] = Profile.get_profile(request.user)
            try:
                request.session.update(Profile.get_fb_user_dict(request.session['profile'].access_token))
            except Errors.fb_error:
                redirect('/logout')
    @classmethod
    def get_profile(klass, user):
        return klass.objects.get(id=user.id)

    @classmethod
    def handle_fb_errors(klass, error):
        pass

    def extend_token(self, access_token):
        url = "https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=fb_exchange_token&fb_exchange_token=%s" % (constants.client_id, constants.client_secret, access_token)
        response = requests.get(url)
        qd = QueryDict(response.text)
        access_token = qd.get('access_token')
        expiry_date = qd.get('expires')

        import pdb; pdb.set_trace()


        if access_token is not None:
            self.access_token = access_token
            self.save()

        return access_token, expiry_date
        

