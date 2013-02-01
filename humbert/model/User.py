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
            profile = klass(fb_id=fb_id, username=username, access_token=access_token, first_name=first_name, last_name=last_name)
            profile.save()
            return profile

    @classmethod
    def get_fb_user_dict(klass, access_token):
        #make a server side query to fb api and get the user info
        url = 'https://graph.facebook.com/me?access_token=%s' % (access_token)
        response = requests.get(url).text
        user_dict = simplejson.loads(response)
        if user_dict.get('error') is not None:
            self.handle_fb_errors(user_dict.get('error'))
        



        print user_dict
        return user_dict

    @classmethod
    def get_profile(klass, user):
        return Profile.objects.get(id=user_id)
    
    @classmethod
    def init_session(klass, request):
        if 'profile' not in request.session:
            request.session['profile'] = Profile.get_profile(request.user)
            request.session.update(Profile.get_fb_user_dict(request.session['profile'].access_token))

    @classmethod
    def get_profile(klass, user):
        return klass.objects.get(id=user.id)

    def renew_token(self, token):
        # check that the token is the same
        if token != self.access_token and token not in [None, '']:
            #either this is a bad auth
            # or we need to update the access token
            self.access_token = token
            self.save()

    def handle_fb_errors(self, error):
        pass

    def extend_token(self):
        url = https://graph.facebook.com/oauth/access_token?client_id=%&client_secret=%s&grant_type=fb_exchange_token&fb_exchange_token=%s % (constants.client_id, constants.client_secret, self.access_token)
        response = request.get(url).text
        
