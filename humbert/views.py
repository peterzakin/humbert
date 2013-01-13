import string
import re
from django.shortcuts import render_to_response

def home(request):
    c = {}
    return render_to_response('index.html', c)

def post_page(request, post_id):
    c = {}
    c['post_id'] = post_id
    return render_to_response('post_page.html', c)


def render_profile(request, *args, **kwargs):
    username = kwargs.get('username')
    c = {}
    c['username'] = username
    return render_to_response('profile.html', c)


def render_annotation(request, *args, **kwargs):
    username = kwargs.get('username')
    annotation_id = kwargs.get('annotation_id')
    c = {}
    c['username'] = username
    c['annotation_id'] = annotation_id
    return render_to_response('annotation.html', c)

