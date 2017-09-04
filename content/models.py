#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings
from accounts.models import User,Project
from content.storage import images_storage

class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"故障类型")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:

        permissions = (
            ("update_type", ("更新故障类型")),
            ("del_type", ("删除故障类型")),
        )
        default_permissions = () 

class Content(models.Model):
    fms_level = (
        (0, u"非常严重"),
        (1, u"严重"),
        (2, u"中等"),
        (3, u"一般"),
        (4, u"无影响"),
    )
    fms_status = (
        (0, u"处理中"),
        (1, u"已恢复"),
        (2, u"改进中"),
        (3, u"已完结"),
    )
    fms_improve = (
        (0, u"开发"),
        (1, u"运维"),
        (2, u"机房"),
        (3, u"网络运营商"),
        (4, u"第三方"),

    )
    fms_type = Type.objects.all().values_list('id', 'name')
    fms_project = Project.objects.all().values_list('id','name')
    title = models.CharField(max_length=255, verbose_name=u'故障简述', unique=True)
    author = models.ForeignKey(User, verbose_name=u'创建者')
    level = models.IntegerField(choices=fms_level, verbose_name=u'故障级别')
    type = models.ForeignKey(
        Type, related_name='fms_type', verbose_name=u'故障类型',null=True)
    project = models.ForeignKey(Project,related_name='fms_project',verbose_name=u'影响项目',null=True,on_delete=models.PROTECT)
    effect = models.TextField(blank=True, verbose_name=u'故障影响')
    reasons = models.TextField(blank=True, verbose_name=u'故障原因',null=True)
    solution = models.TextField(blank=True, verbose_name=u'解决方案',null=True)
    status = models.IntegerField(choices=fms_status, verbose_name=u'故障状态')
    improve = models.IntegerField(choices=fms_improve, verbose_name=u'主导改进')
    content = models.TextField(blank=True, verbose_name=u'故障分析')
    start_time = models.DateTimeField(verbose_name=u'开始时间')
    end_time = models.DateTimeField(verbose_name=u'结束时间')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.title

    class Meta:

        permissions = (
            ("get_content", ("查看故障列表")),
            ("detail_content", ("故障详情")),
            ("add_content", ("添加故障")),
            ("edit_content", ("编辑故障")),
            ("del_content", ("删除故障")),
        )
        default_permissions = () 


class Images(models.Model):

    url = models.ImageField(upload_to = 'img/%Y/%m/%d', blank=True, null=True,storage=images_storage())
    create_time = models.DateTimeField(auto_now_add=True, blank=True ,null=True)



