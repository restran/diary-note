# Create your views here.
#-*- encoding: utf-8 -*-
'''
Created on 2012-12-5

@author: Neil
'''
from django.shortcuts import render_to_response

def fireworks(request):
    return render_to_response("rhtml5/fireworks.html")

def hny2012(request):
    return render_to_response("rhtml5/hny2012.html")
    
