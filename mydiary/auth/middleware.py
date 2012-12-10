#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''
from diary.mydiary.auth import get_user
from diary import settings
class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user(request)
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session')#需要安装session中间件
        request.__class__.user = LazyUser()
        request.__class__.HOME_PAGE_URL = settings.HOME_PAGE_URL#标记主页url
        request.__class__.DOMAIN_URL = settings.DOMAIN_URL#标记域名url
        return None