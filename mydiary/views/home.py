#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from diary import settings
from django.views.decorators.csrf import csrf_protect

def base(request):
    return render_to_response('base.html')

@csrf_protect
#在index.html的登录form中action="settings.DOMAIN_URL"
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL + 'diary/write/')#跳转到写日志页面  
    else:
        if request.method == 'POST':
            from diary.mydiary.views.accounts import login_method
            return login_method(request)
        else:
            return render_to_response('index.html', {'request':request})
    
def gen_inv_code(request, count):
    if request.user.is_authenticated() and request.user.name == 'restran':
        from diary.mydiary.models import Invite_Code
        count = int(count)
        str = u'成功生成%s个邀请码:)' % (count)
        for i in range(count):
            code = Invite_Code()
            str += '<br>' + code.gen_invit_code()#生成邀请码
         
        return HttpResponse(str)
    else:
        return render_to_response('404.html', {'request':request})

def error_404(request):
    return render_to_response('404.html', {'request':request})