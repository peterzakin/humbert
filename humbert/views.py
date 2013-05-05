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
from model.Text import Text
import simplejson

def home(request):
    c = RequestContext(request)
    if request.user.is_authenticated():
        Profile.init_session(request)
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

def logout_view(request):
    # /logout
    logout(request)
    return redirect('/?state=logged_out')


def create_annotation(request):
    """ 
    POST to create_annotation creates a text. Does not actually create an Annotation record
    Redirects to an annotation_editing_view.
    """
    
    #takes a post
    if request.method != 'POST':
        redirect('/')

    c = RequestContext(request)
    user_id = request.user.id

    url = request.POST.get('url')
    text = request.POST.get('text')

    if url:
        text_info = Text.get_or_create_text_by_url(url)
        text_id = text_info.get('_id')
    elif text:
        c['text'] = text
        text_id = Text.add_text({'text':text})
    else:
        redirect('/')
        
    redirect('/edit/%s' % text_id)


def edit_annotation(request, text_id):
    c = RequestContext(request)
    if text_id is not None and request.user.is_authenticated():
        text_info = Text.find_by_id(text_id)
    else:
        redirect('/')

    c['user'] = request.user
    c['annotation_username'] = request.user.username
    c['annotation_user_id'] = request.user.id
    c['text_id'] = text_id
    c['text'] = text_info.get('text')
    c['edit_mode'] = True
    
    annotation = Annotation.find_by_user_id_and_text_id(request.user.id, text_id)
    
    comments = []
    if annotation:
        comments = annotation.get('comments')
    
    c['initial_comments'] = simplejson.dumps(comments)
    return render_to_response('annotation.html', c)


def render_annotation(request, username, text_id):
    annotation_user = Profile.objects.get(username=username)
    text_info = Text.find_by_id(text_id)
    c = RequestContext(request)
    c['annotation_username'] = annotation_user.username
    c['annotation_user_id'] = annotation_user.id
    c['text_id'] = text_id
    c['text'] = text_info.get('text')
    annotation = Annotation.find_by_user_id_and_text_id(annotation_user.id, text_id)
    
    comments = []
    if annotation:
        comments = annotation.get('comments')
    
    c['initial_comments'] = simplejson.dumps(comments)
    return render_to_response('annotation.html', c)


#AJAX FUNCTIONS
def save_annotation(request):
    comments = simplejson.loads(request.POST.get('comments'))
    user_id = request.user.id
    text_id = request.POST.get('text_id')

    annotation_id = None
    if comments and user_id:
        annotation_id = Annotation.save_annotation(user_id, text_id, comments)

    if annotation_id is None:
        raise Exception("hell fuck")

    return HttpResponse(annotation_id)
        

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
