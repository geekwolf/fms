#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render, reverse
import json
import collections
import datetime
from content.models import ZbxContent
from django.conf import settings


def index(request):

    request.breadcrumbs((('首页', '/'), ('故障列表', reverse('fms_list')), ('故障统计', reverse('cus_dashboard_index'))))
    return render_to_response('dashboard/zbx_index.html', {'request': request})


def get_verbose_name(field):

    data = {}
    params = [v for v in ZbxContent._meta.fields]
    for msg in params:
        data[msg.name] = msg.verbose_name
    verbose_name = data[field]
    return verbose_name


# def calculate_percent(item_data):

#   item_legend = []
#   total = sum([i['value'] for i in item_data])
#   for i in item_data:
#       percent="%.2f%%" % (float(i['value'])/total*100)
#       tname = "%s:%s(%s)" % (i['name'],percent,i['value'])
#       item_legend.append(tname)
#   return item_legend

def get_month():

    year_month = []
    # get current month
    # now_month = datetime.datetime.now().month
    # for i in range(1,now_month+1):
    #   delta = (now_month - i)*365/12
    #   year_month.append((datetime.date.today() - datetime.timedelta(delta)).strftime("%Y-%m"))
    # get current year all months
    year = int(datetime.datetime.now().strftime("%Y"))
    year_month = [datetime.date(year, m, 1).strftime('%Y-%m') for m in range(1, 13)]

    return year_month


def get_pie_data(data, item):
    result = {}
    item_data = []
    item_legend = []
    for i in data:
        item_data.append({"name": i.item, "value": i.count})
        item_legend.append(i.item)

    item_text = get_verbose_name(item)
    result = {"text": item_text, "data": item_data, "legend": item_legend, "subtext": '最近三个月数据', "type": 'pie'}
    return result


def get_pie_history_data(data, item):
    result = {}
    item_data = []
    item_legend = []
    for i in data:
        item_data.append({"name": i.name, "value": i.count})
        item_legend.append(i.name)

    item_text = get_verbose_name(item.split('_')[1])
    result = {"text": item_text, "data": item_data, "legend": item_legend, "subtext": '今年故障统计数据', "type": 'pie'}

    return result


def get_line_data(data):

    item_legend = []
    result = {}
    item_data = []
    _tmp = {}
    _data = collections.OrderedDict()
    now_month = datetime.datetime.now().month

    xaxis_month = get_month()

    for d in data:
        _tmp[d.date] = d.count
    for x in xaxis_month:
        if x in _tmp.keys():
            _data[x] = _tmp[x]
        else:
            _data[x] = 0

    item = {"name": '计数', "stack": '总量', "data": list(_data.values()), "type": 'line'}
    result = {"text": '今年故障统计数据', "subtext": 'From Zabbix', "data": item, "legend": item_legend, "xaxis_data": xaxis_month, "type": 'line'}
    return result


def index_data(request):

    data = {}
    items_pie = ['level', 'type', 'project', 'host']
    items_line = 'fms_sum'

    # 最近三个月数据
    for i in items_pie:
        
        _content = ZbxContent.objects.raw('SELECT id,%s as item,count(id) as count FROM content_zbxcontent WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(start_time) GROUP BY %s' % (i, i))
        #获取到top10的故障服务器
        if i=='host':
            content = ZbxContent.objects.raw('select * from (SELECT id,%s as item,count(id) as count FROM content_zbxcontent WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(start_time) GROUP BY %s) a order by count desc' % (i, i))
            _content = content[:10] if content
        data[i] = get_pie_data(_content, i)

    # 根据故障项目分类，今年故障数量统计
    content_history = ZbxContent.objects.raw(
        'SELECT id,count(*) as count,DATE_FORMAT(start_time,"%%Y-%%m") as date from content_zbxcontent where YEAR(start_time) = YEAR(CURDATE()) GROUP  by DATE_FORMAT(start_time,"%%Y-%%m")')

    data['fms_sum'] = get_line_data(content_history)

    project = ZbxContent.objects.values_list('project').distinct()
    data['project_item'] = [i[0] for i in project] if project else []
    return HttpResponse(json.dumps(data))


# def select_data(request):

#     data = {}
#     history = ['fms_type_history']

#     if request.method == "POST":
#         if request.POST.get('type') == "project":
#             project = request.POST.get('selected')
#             if project == "All":
#                 sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE())  GROUP BY type_id"
#             else:
#                 project_id = Project.objects.filter(name=project).values('id')[0]['id']
#                 sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) and project_id=%s GROUP BY type_id" % project_id
#             content_history = ZbxContent.objects.raw(sql)
#             for k in history:
#                 data[k] = get_pie_history_data(content_history, k)
#         return HttpResponse(json.dumps(data))
#     else:
#         return HttpResponseRedirect('/')
