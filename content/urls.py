#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from __future__ import unicode_literals
from django.conf.urls import url
from content import views, api, zbx

urlpatterns = [
    # url(r'^login/$', associate_openid, name='associate_openid'),
    url(r'^list$', views.fms_list, name='fms_list'),
    url(r'^add$', views.fms_add, name='fms_add'),
    url(r'^edit$', views.fms_edit, name='fms_edit'),
    url(r'^detail/(?P<id>[a-zA-Z0-9]{32,32})$', views.fms_detail, name='fms_detail'),
    url(r'^search$', api.fms_search, name='fms_search'),
]
