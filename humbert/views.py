import sys
import string
import re
import constants
from django.shortcuts import render_to_response
from lib.diffbotHelper import DiffBot 


def home(request):
    request.session['peter'] = 'zakin'
    c = {}
        
    return render_to_response('index.html', c)

def post_page(request, post_id):
    c = {}
    c['post_id'] = post_id
    return render_to_response('post_page.html', c)

def channel(request):
    c = {}
    return render_to_response('channel.html', c)

def render_profile(request, *args, **kwargs):
    username = kwargs.get('username')
    c = {}
    c['peter'] = request.session.get('peter')
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
    c['text'] = Annotation.find_by_id(ObjectId(annotation_id))
    return render_to_response('annotation.html', c)

def add_annotation(request):
    #use post
    url = request.POST.get('url')
    
    #has the url already been seen--> cursor
    annotations = Annotation.find_by_url(url)
    if annotations.count() == 0:
        c['text'] = Diffbot.get_article(url)
