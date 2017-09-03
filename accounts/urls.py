# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import views,api,project,contact,permissions
urlpatterns = [
	#Login & Logout
    url(r'^login/$', views.login,name='accounts_login'),
    url(r'^logout/$', views.logout,name='accounts_logout'),
    #User Managment
    url(r'^user$', views.accounts_user,name='accounts_user'),
    url(r'^user/add$', views.accounts_add,name='accounts_add'),
    url(r'^user/edit$', views.accounts_edit,name='accounts_edit'),
    url(r'^user/del$', views.accounts_del,name='accounts_del'),

    #Group Managment
    url(r'group$', views.accounts_group, name='accounts_group'),
    url(r'group/update$', views.accounts_group_update, name='accounts_group_update'),
    url(r'group/del$', views.accounts_group_del, name='accounts_group_del'),
    #Permissions
    url(r'permission$', permissions.permission, name='accounts_permission'),

    #Project
    url(r'^user/search$', api.user_search,name="user_search"),
    url(r'^project/list$', project.project_list,name='project_list'),
    url(r'^project/add$', project.project_add,name='project_add'),
    url(r'^project/edit$', project.project_edit,name='project_edit'),
    url(r'^project/del/(?P<id>\d+)$', project.project_del,name='project_del'),

    url(r'^contact/list$', contact.contact_list, name='contact_list'),

    url(r'^contact/add$', contact.contact_add, name='contact_add'),
    url(r'^contact/del/(?P<id>\d+)$', contact.contact_del, name='contact_del'),
    url(r'^contact/edit$', contact.contact_edit, name='contact_edit'),
]