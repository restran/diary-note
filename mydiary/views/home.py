#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from diary import settings

def base(request):
    return render_to_response('base.html')

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL + 'diary/write/')#跳转到写日志页面  
    else:
        return render_to_response('index.html', {'request':request})

def error_404(request):
    return render_to_response('404.html')