#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''
'''
from user import User
from log import Log

__all__ = [    
           'User', 'Log'
        ]

'''
import django.db.models        
import sys                     

appname = 'mydiary'
from user import User
from log import Log
from invite_code import Invite_Code
__all__ = []     

for decl in globals().values():
    try:
        if decl.__module__.startswith(__name__) and issubclass(decl, django.db.models.Model):
            decl._meta.db_table = decl._meta.db_table.replace('models', appname)
            decl._meta.app_label = appname   
            __all__.append(decl.__name__)
            django.db.models.loading.register_models(appname, decl)
    except:
        pass
