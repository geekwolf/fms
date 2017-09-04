#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from __future__ import unicode_literals

from django.conf.urls import url
from dashboard import views 

urlpatterns = [

    url(r'^$', views.index, name='dashboard_index'),
    url(r'^index$', views.index_data,name='index_data'),
    url(r'^select$', views.select_data,name='select_data'),

]
