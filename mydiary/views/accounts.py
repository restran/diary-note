#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''

#必须导入的模块
from diary.mydiary import auth
from diary.mydiary.auth.forms import UserCreationForm, UserInfoEditForm, PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from diary import settings
from django.views.decorators.csrf import csrf_protect

#登录
@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            # 认证通过
            auth.login(request, user)
            # 跳转到登陆成功的页面
            return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页
        else:
            # 返回出错信息
            return render_to_response("accounts/login.html", {'login_failed':True, 'p_email':email})
    else:
        return render_to_response("accounts/login.html", {'login_failed':False})

#登出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(settings.HOME_PAGE_URL)#跳转到主页

#注册
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()#将数据保存到数据库中
            user.save()

            return render_to_response("accounts/register.html",
                {'register_success':True, 'username':user.name})#注册成功
        else:
            return render_to_response("accounts/register.html",
                {'register_success':False, 'email_hasExist':form.emial_hasExist, 
                'name_hasExist':form.name_hasExist, 'password_notMatch':form.password_notMatch,
                'p_email':request.POST['email'],'p_name':request.POST['name']})
    else:
        return render_to_response("accounts/register.html", {'register_success':False})
    

#查看个人资料
@csrf_protect
def profile(request):
    if not request.user.is_authenticated():
        return render_to_response('404.html')
  
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name', '')
        if name != user.name:
            form = UserInfoEditForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                return render_to_response("accounts/profile.html", 
                    {'user':user,'name_edited':False,'edit_success':True,'request':request}) 
            else:
                
                return render_to_response("accounts/profile.html", 
                    {'user':user,'name_edited':True,'name_hasExist':form.name_hasExist,'request':request})
        else:
            return render_to_response("accounts/profile.html", 
                    {'user':user,'name_edited':False,'request':request})
    else:
        user = request.user
        return render_to_response("accounts/profile.html", 
                    {'user':user,'name_edited':False,'request':request})
    
#修改密码
@csrf_protect
def editpassword(request):
    if not request.user.is_authenticated():
        return render_to_response('404.html')
    
    if request.method == 'POST':
        user = request.user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()#将数据保存到数据库中
            return render_to_response("accounts/editpassword.html",
                {'editpassword_success':True, 'request':request})#修改成功
        else:
            return render_to_response("accounts/editpassword.html",{'editpassword_success':False,
                'password_notMatch':form.password_notMatch,'old_password_correct':form.old_password_correct,
                'request':request})
    else:
        return render_to_response("accounts/editpassword.html", 
               {'editpassword_success':False,'request':request,'old_password_correct':True})