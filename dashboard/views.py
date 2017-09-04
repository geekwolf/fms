#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render, reverse
import json
import collections
import datetime
from content.models import Content, Type, Project
from django.conf import settings


def index(request):

    request.breadcrumbs((('首页', '/'),('故障列表',reverse('fms_list')),('故障统计',reverse('dashboard_index'))))
    return render_to_response('dashboard/index.html', {'request': request})


def get_verbose_name(field):

    data = {}
    params = [v for v in Content._meta.fields]
    for msg in params:
        data[msg.name] = msg.verbose_name
    verbose_name = data[field]
    return verbose_name


# def calculate_percent(item_data):

# 	item_legend = []
# 	total = sum([i['value'] for i in item_data])
# 	for i in item_data:
# 		percent="%.2f%%" % (float(i['value'])/total*100)
# 		tname = "%s:%s(%s)" % (i['name'],percent,i['value'])
# 		item_legend.append(tname)
# 	return item_legend

def get_month():

    year_month = []
    # get current month
    # now_month = datetime.datetime.now().month
    # for i in range(1,now_month+1):
    # 	delta = (now_month - i)*365/12
    # 	year_month.append((datetime.date.today() - datetime.timedelta(delta)).strftime("%Y-%m"))
    # get current year all months
    year = int(datetime.datetime.now().strftime("%Y"))
    year_month = [datetime.date(year, m, 1).strftime('%Y-%m') for m in range(1, 13)]

    return year_month


def get_pie_data(data, item):

    result = {}
    _data = set(data)
    item_data = []
    item_legend = []
    for i in _data:
        item_data.append({"name": i, "value": data.count(i)})
        item_legend.append(i)

    item_text = get_verbose_name(item.split('_')[1])
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


def get_line_data(data, item):

    item_legend = data.keys()
    result = {}
    item_data = []
    now_month = datetime.datetime.now().month
    for k, v in data.items():
        for i in range(1, now_month + 1):
            delta = (now_month - i) * 365 / 12
            month = (datetime.date.today() - datetime.timedelta(delta)).strftime("%Y-%m")
            if month not in v:
                v[month] = 0
        per_item = {"name": k, "stack": '总量', "data": list(v.values()), "type": 'line'}
        item_data.append(per_item)

    for i in range(1, now_month + 1):
        delta = (now_month - i) * 365 / 12
        month = (datetime.date.today() - datetime.timedelta(delta)).strftime("%Y-%m")

    xaxis_month = get_month()
    text = "今年故障统计"
    if item == "fms_application_sum":
        subtext = "针对业务故障类型"
    elif item == "fms_sum":
        subtext = "针对所有故障类型"
    else:
        pass

    result = {"text": text, "subtext": subtext, "data": item_data, "legend": list(item_legend), "xaxis_data": xaxis_month, "type": 'line'}
    return result


def index_data(request):

    data = {}
    items_pie = ['fms_level', 'fms_type', 'fms_project']
    history = ['fms_type_history']
    items_line = ['fms_sum', 'fms_application_sum']

    content = Content.objects.raw('SELECT * FROM content_content WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(ctime)')
    content_history = Content.objects.raw(
        'SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) GROUP BY type_id')
    project_list = Project.objects.all()

    # all project list
    project = [i.name for i in project_list]

    fms_level = []
    fms_type = []
    fms_project = []
    fms_type_history = []

    _tmp = {}
    for i in content:
        fms_level.append(i.get_level_display())
        fms_type.append(str(i.type))
        fms_project.append(str(i.project))

    _tmp['fms_level'] = fms_level
    _tmp['fms_type'] = fms_type
    _tmp['fms_project'] = fms_project

    _year_sum = Content.objects.raw(
        'SELECT id,count(*) as count,project_id,DATE_FORMAT(ctime,"%%Y-%%m") as date from content_content where YEAR(ctime) = YEAR(CURDATE()) GROUP  by project_id,DATE_FORMAT(ctime,"%%Y-%%m")')
    # 针对业务故障，查询条件设置成该类型ID
    _year_application_sum = Content.objects.raw('SELECT id,count(*) as count,project_id,DATE_FORMAT(ctime,"%%Y-%%m") as date from content_content where YEAR(ctime) = YEAR(CURDATE()) and type_id in {0} GROUP  by project_id,DATE_FORMAT(ctime,"%%Y-%%m")'.format(tuple(settings.SPECIAL_TYPES)))


    year_sum = collections.defaultdict(dict)
    year_application_sum = collections.defaultdict(dict)

    for i in _year_sum:
        year_sum[str(i.project)][i.date] = i.count

    for i in _year_application_sum:
        year_application_sum[str(i.project)][i.date] = i.count

    for k in items_pie:
        data[k] = get_pie_data(_tmp[k], k)

    for k in items_line:
        if k == "fms_application_sum":
            data[k] = get_line_data(year_application_sum, k)
        else:
            data[k] = get_line_data(year_sum, k)

    for k in history:
        data[k] = get_pie_history_data(content_history, k)
    data['project'] = project

    return HttpResponse(json.dumps(data))


def select_data(request):

    data = {}
    history = ['fms_type_history']

    if request.method == "POST":
        if request.POST.get('type') == "project":
            project = request.POST.get('selected')
            if project == "All":
                sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE())  GROUP BY type_id"
            else:
                project_id = Project.objects.filter(name=project).values('id')[0]['id']
                sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) and project_id=%s GROUP BY type_id" % project_id
            content_history = Content.objects.raw(sql)
            for k in history:
                data[k] = get_pie_history_data(content_history, k)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect('/')
