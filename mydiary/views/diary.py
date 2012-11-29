#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import get_template
from django.template.context import Context
import string, datetime, json
from django.http import HttpResponseRedirect
from diary.mydiary.models import Log
@csrf_protect
def write(request):
   
    #只有登录用户，才可以操作，
    if not request.user.is_authenticated():
        return render_to_response('404.html')
    if request.method == 'POST':
        content = (request.POST.get('content')).strip()
        if content != '':
            log = Log(user=request.user, content=content)
            log.save()
            return HttpResponseRedirect('diary/past.html')#跳转到过往日志页面  
    else:
        current_time = datetime.datetime.now()
        ctstr = current_time.strftime('%Y, %B %d, %A, %H:%M')
        return render_to_response("diary/write.html", {'request':request, 'current_time':ctstr})

@csrf_exempt # 若没有csrf处理，服务器会返回403 forbidden错误
def ajax_write(request, user_id):
    if not request.is_ajax() or (request.method != 'POST'):
        return HttpResponse(json.dumps({"status":'error0'}))
         
    #只有登录用户，才可以操作，
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"status":'error1'}))
    content = (request.POST.get('content')).strip()
    if content != '':
        return render_to_response("accounts/login.html", {'login_failed':False})
    