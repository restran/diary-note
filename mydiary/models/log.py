#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''
from django.db import models
from diary.mydiary.models.user import User

class Log(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    content_update_flag = models.BooleanField(default=False)#是否重新编辑过内容
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        app_label = 'mydiary'

    def get_name(self):
        return self.name