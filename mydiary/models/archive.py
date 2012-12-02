#-*- encoding: utf-8 -*-
'''
Created on 2012-12-2

@author: Neil
'''
from django.db import models
from diary.mydiary.models.user import User

class Archive_Year(models.Model):
    user = models.ForeignKey(User)
    year = models.CharField(max_length=4)#年
    log_count = models.IntegerField(default=1)#该年的日志记录
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        app_label = 'mydiary'
        
class Archive_Month(models.Model):
    ar_year = models.ForeignKey(Archive_Year)
    month = models.CharField(max_length=2)#月
    log_count = models.IntegerField(default=1)#该月的日志记录
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        app_label = 'mydiary'
        
