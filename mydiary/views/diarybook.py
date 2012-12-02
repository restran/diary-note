#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import datetime, json
from diary.mydiary.models import Log
from diary import settings
from diary.mydiary.models import Archive_Year, Archive_Month
@csrf_protect
def write(request):
    #import logging
    #logging.debug("A log message")
    #只有登录用户，才可以操作
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页面 
    log_count = Log.objects.filter(user=request.user).count()
    if request.method == 'POST':
        content = (request.POST.get('textcontent')).strip()
        if content != '':
            log = Log(user=request.user, content=content)
            log.no = log_count + 1
            log.save()
            
            try:
                archive_year = Archive_Year.objects.get(user=request.user, year=str(datetime.datetime.now().year))
                archive_year.log_count += 1#增加该年的日志计数
                archive_year.save()
                try:
                    archive_month = Archive_Month.objects.get(ar_year=archive_year, month=str(datetime.datetime.now().month))
                    archive_month.log_count += 1#增加该月的日志计数
                    archive_month.save()
                except Archive_Month.DoesNotExist:
                    archive_month = Archive_Month(ar_year=archive_year, month=str(datetime.datetime.now().month))
                    #log_count默认初始化为1
                    archive_month.save()
            except Archive_Year.DoesNotExist:
                archive_year = Archive_Year(user=request.user, year=str(datetime.datetime.now().year))
                archive_year.save()
                archive_month = Archive_Month(ar_year=archive_year, month=str(datetime.datetime.now().month))
                #log_count默认初始化为1
                archive_month.save()
                    
            return HttpResponseRedirect(settings.HOME_PAGE_URL + 'diary/past/')#跳转到过往日志页面  
    else:
        current_time = datetime.datetime.now()
        ctstr = current_time.strftime('%Y, %B %d, %A, %H:%M')
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
    
#在past页面中获取归档信息
def get_past_archive(user):
    archive_list = Archive_Year.objects.filter(user=user).order_by('-year')#年份大的在前面
    for ar_y in archive_list:
        ar_y.ar_m_list = Archive_Month.objects.filter(ar_year=ar_y).order_by('-month')
        
    return archive_list

#只显示最近15条日志
def past(request):
    #只有登录用户，才可以操作
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页面
    
    log_list = Log.objects.filter(user=request.user).order_by('-date_posted')[0:15]#加-号表示逆向排序
    for log in log_list:
        log.date_posted_str = log.date_posted.strftime('%Y/%m/%d, %A, %H:%M')
    
    archive_list = get_past_archive(request.user)
    return render_to_response("diary/past.html", {'request':request, 'log_list':log_list, 'archive_list':archive_list})

#按年月查看
def past_year_month(request, year, month):
    #只有登录用户，才可以操作
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页面
    
    log_list = Log.objects.filter(user=request.user, date_posted__year=int(year),date_posted__month=int(month)).order_by('-date_posted')[0:15]#加-号表示逆向排序
    for log in log_list:
        log.date_posted_str = log.date_posted.strftime('%Y, %m, %d, %A, %H:%M')
    
    archive_list = get_past_archive(request.user)
    return render_to_response("diary/past.html", {'request':request, 'log_list':log_list, 'archive_list':archive_list})
