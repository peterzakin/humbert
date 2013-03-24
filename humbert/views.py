from django.contrib.auth import authenticate, login
import sys
import string
import re
import constants
from django.shortcuts import render_to_response, redirect
from lib.diffbotHelper import DiffBot 
from django.template import RequestContext
from model.User import User, Profile
from django.http import HttpResponse
from django.contrib.auth import logout
from model.Annotation import Annotation


def home(request):
    c = RequestContext(request)
    if request.user.is_authenticated():
        Profile.init_session(request)
        url = "http://www.paulgraham.com/start.html"
        #c['text'] = DiffBot.get_article(url)
        c['bio'] = request.session['bio']
        return render_to_response('logged_in_home.html', c)

    return render_to_response('landing.html', c)


def render_profile(request, *args, **kwargs):
    username = kwargs.get('username')
    c = {}
    profile_user = User.find_by_username(username)
    if profile_user is not None:

        #get list of annotations
        c['annotations'] = Annotation.find_by_user_id(profile_user.id)
        c['username'] = username
    return render_to_response('profile.html', c)


def render_annotation(request, *args, **kwargs):
    username = kwargs.get('username')
    annotation_id = kwargs.get('annotation_id')
    c = {}
    c['username'] = username
    
    url = "http://www.paulgraham.com/start.html"

    #create annotation if the text doesn't exist
    annotation = Annotation.find_by_url(url)
    if annotation is None:
        #create new annotation
        try:
            import pdb; pdb.set_trace()
            text = DiffBot.get_article(url)
            doc = {
                'url':url,
                'text':text
                }
            Annotation.add_annotation(doc)
            c['text'] = text
        except:
            raise Exception('oh shit diffbot')
    else:
        #annotation exists
        c['text'] = annotation.text

    return render_to_response('annotation.html', c)

def logout_view(request):
    # /logout
    logout(request)
    return redirect('/?state=logged_out')


#AJAX FUNCTIONS
def fb_login_with_token_and_id(request):
    #check to see if we have a user with this fb_id
    fb_id = request.POST.get('fb_id')
    access_token = request.POST.get('access_token')
    user_set = Profile.objects.filter(fb_id=fb_id)

    # could probably change this to access token; i.e lookup by access token and not id
    if len(user_set) == 0:
        # create new user
        user = Profile.create_new_fb_user(fb_id, access_token)
        if user is not None:
            #if we created the user alright lets log him in 
            user.backend = 'django.contrib.auth.backends.ModelBackend'    
            login(request,user)
            
    else:
        user = user_set[0]
        #update the access token
        user.extend_token(access_token)
        user.backend = 'django.contrib.auth.backends.ModelBackend'    
        login(request,user)

    print user.__dict__
    return HttpResponse('Hey client side, we just logged u in. -serverside out')
