#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from __future__ import unicode_literals

from django.conf.urls import url
from dashboard import views, zbx

urlpatterns = [

    url(r'^cus$', views.index, name='cus_dashboard_index'),
    url(r'^cus/index$', views.index_data, name='cus_index_data'),
    url(r'^cus/select$', views.select_data, name='cus_select_data'),

    url(r'^zbx$', zbx.index, name='zbx_dashboard_index'),
    url(r'^zbx/index$', zbx.index_data, name='zbx_index_data'),
    # url(r'^zbx/select$', zbx.select_data, name='zbx_select_data'),
]
