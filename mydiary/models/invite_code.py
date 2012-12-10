#-*- encoding: utf-8 -*-
'''
Created on 2012-12-1

@author: Neil
'''
from django.db import models

#邀请码
class Invite_Code(models.Model):
    code = models.CharField(max_length=24)
    used_count = models.IntegerField(default=0)#使用计数
    is_actived = models.BooleanField(default=True)#是否有效

    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        app_label = 'mydiary'

    def gen_invit_code(self):
        from random import Random
        randomlength = 24
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        while True:
            str = ''
            random = Random()
            for i in range(randomlength):
                str += chars[random.randint(0, length)]
            try:
                Invite_Code.objects.get(code=str)
            except Invite_Code.DoesNotExist:
                self.code = str
                self.save()
                break
            
        return str

