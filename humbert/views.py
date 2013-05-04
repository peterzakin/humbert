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
from model.Annotation import Annotation, Comment
from model.Text import Text


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


def render_annotation(request, *args, **kwargs):
    username = kwargs.get('username')

    c = {}
    c['username'] = username
    
    url = "http://www.paulgraham.com/start.html"
    #create annotation if the text doesn't exist
    annotations = Annotation.find_by_url(url)
    if annotations.count() <= 0:
        #create new annotation
        try:
            text_info = DiffBot.get_article(url)
            doc = {
                'url':url,
                'text':text
                }
            Annotation.add_annotation(doc)
            c['text'] = text
        except:
            raise Exception('oh shit diffbot')
    else:
        #1 or more annotations exist
        c['text'] = annotations[0].get('text')

    return render_to_response('annotation.html', c)



def logout_view(request):
    # /logout
    logout(request)
    return redirect('/?state=logged_out')


def create_annotation(request):
    #takes a post
    if request.method != 'POST':
        redirect('/')

    c = RequestContext(request)
    user_id = request.user.id

    url = request.POST.get('url')
    text = request.POST.get('text')

    if url:
        text_info = Text.get_or_create_text_by_url(url)
        c['text'] = text_info.get('text')
        c['author'] = text_info.get('author')
        c['url'] = url
        c['title'] = text_info.get('title')
    elif text:
        c['text'] = text
        Text.add_text({'text':text})
    else:
        redirect('/')

    #here we have a text. let's create an annotation for the guy
    annotation_id = Annotation.make_annotation(text_info, user_id)
    c['annotation_id'] = annotation_id
    c['username'] = request.user.username
    return render_to_response('annotation.html', c)


#AJAX FUNCTIONS
def create_comment(request):
    import pdb; pdb.set_trace()
    post_vars = request.POST
    start_span = post_vars.get('start_span')
    end_span = post_vars.get('end_span')
    comment = post_vars.get('comment')
    annotation_id = post_vars.get('annotation_id')

    if start_span and end_span and comment and annotation_id:
        comment = Comment(start_span, end_span, comment)
        Annotation.add_comment_to_annotation(comment, annotation_id)
    else:
        raise Exception('something went wrong');


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
