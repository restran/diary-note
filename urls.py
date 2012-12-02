#-*- encoding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^diary/', include('diary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root':settings.MEDIA_ROOT}, name="media"),#映射media文件
)

#元组是可累加的，但累加后是生成新的元组，而非在原来的基础上修改
urlpatterns += patterns('diary.mydiary.views',#第一个参数可设置公共前缀
    (r'^$', 'home.index'),#当设置公共前缀时，应使用字符串
    (r'^accounts/login/$', 'accounts.login'),
    (r'^accounts/logout/$', 'accounts.logout'),
    (r'^accounts/register/$', 'accounts.register'),
    (r'^accounts/profile/$', 'accounts.profile'),
    (r'^accounts/editpassword/$', 'accounts.editpassword'),
)

urlpatterns += patterns('diary.mydiary.views',#第一个参数可设置公共前缀
    (r'^diary/write/$', 'diarybook.write'),
    (r'^diary/past/$', 'diarybook.past'),
    (r'^diary/past/(?P<year>\d{4})/(?P<month>\d{2})/$', 'diarybook.past_year_month'),
    (r'^', 'home.error_404'),
)
