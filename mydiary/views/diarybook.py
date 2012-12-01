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
from diary import settings

@csrf_protect
def write(request):
    #import logging
    #logging.debug("A log message")
    #只有登录用户，才可以操作
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页面 
    if request.method == 'POST':
        content = (request.POST.get('textcontent')).strip()
        if content != '':
            log = Log(user=request.user, content=content)
            log.save()
            return HttpResponseRedirect(settings.HOME_PAGE_URL + 'diary/past/')#跳转到过往日志页面  
    else:
        current_time = datetime.datetime.now()
        ctstr = current_time.strftime('%Y, %B %d, %A, %H:%M')
        log_count = Log.objects.filter(user=request.user).count()
        return render_to_response("diary/write.html", {'request':request, 'current_time':ctstr, 'current_log_count':log_count + 1})

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
    
def past(request):
    #只有登录用户，才可以操作
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页面
    
    log_count = Log.objects.filter(user=request.user).count()
    log_list = Log.objects.filter(user=request.user).order_by('-date_posted')[0:15]#加-号表示逆向排序
    for log in log_list:
        log.no= log_count
        log.date_posted_str = log.date_posted.strftime('%Y, %B %d, %A, %H:%M')
        log_count -= 1

    return render_to_response("diary/past.html", {'request':request, 'log_list':log_list})
