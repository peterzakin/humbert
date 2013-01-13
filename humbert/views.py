import string
import re
from django.shortcuts import render_to_response

def home(request):
    c = {}
    return render_to_response('index.html', c)
