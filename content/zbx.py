# -*- coding: utf-8 -*-
# @Author: Geekwolf
# @Date:   2018-02-27 13:17:49
# @Last Modified by:   Geekwolf
# @Last Modified time: 2018-03-02 14:35:19
from django.shortcuts import render_to_response, HttpResponse, render
from commons.pymysql import query
from django.conf import settings
from content.models import ZbxContent
import re
import time


def get_today_timestamp():
    now_time = int(time.time())
    day_timestamp = now_time - now_time % 86400 + time.timezone
    return day_timestamp


def severity_name():
    severity = {}
    _severity = 'SELECT severity_name_0,severity_name_1,severity_name_2,severity_name_3,severity_name_4,severity_name_5 FROM config'
    rec = query(_severity)[0]
    for r in range(len(rec)):
        severity[r] = rec[r]
    return severity


def timestamp_to_time(timestamp):

    timestamp = int(timestamp)
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return str(dt)


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_problem(status, eventids=None):

    if status == 0:
        field = 'p.eventid in (%s)' % eventids
    elif status == 1:
        field = 'p.clock >=%s' % get_today_timestamp()

    _problem = '''
			SELECT
				DISTINCT(p.eventid),
			  	hs.host,
				p.source,
				p.objectid,
				p.clock,
				p.r_eventid,
				p.r_clock,
				t.description,
				t.priority,
			  	als.name as application_name,
			  	g.name as group_name,
			  	hs.name as hostname

			FROM
				problem AS p,
				triggers AS t,
				hosts AS hs,
				functions AS fs,
				items AS its,
				items_applications AS ia,
				applications AS als,
				hosts_groups AS hg,
				groups AS g
			WHERE
				p.source = 0 AND %s
				AND p.objectid = t.triggerid
				AND fs.triggerid = t.triggerid
			  	AND fs.itemid = its.itemid
			  	AND its.hostid = hs.hostid
				AND ia.itemid = fs.itemid
				AND ia.applicationid = als.applicationid
				AND its.hostid = hg.hostid
				AND hg.groupid = g.groupid
			''' % field
    rec = query(_problem)
    return rec


def get_description(rec):

    # host = ['{HOST.HOST}', '{IPADDRESS}', '{HOST.IP}']
    # hostname = ['{HOSTNAME}', '{HOST.NAME}']
    adict = {'{HOST.HOST}': rec[1], '{IPADDRESS}': rec[1], '{HOST.IP}': rec[1], '{HOSTNAME}': rec[11], '{HOST.NAME}': rec[11]}
    description = rec[7]
    rx = re.compile('|'.join(map(re.escape, adict)))

    def regex(match):
        return adict[match.group(0)]

    return rx.sub(regex, description)


def update_problem_data(problems):

    severity = severity_name()
    if problems:
        for p in problems:
            _rec = {}

            _rec['title'] = get_description(p)
            _rec['host'] = p[1]
            _rec['level'] = severity[p[8]]
            _rec['type'] = p[9]
            _rec['project'] = p[10]
            _rec['content'] = _rec['title']
            _rec['start_time'] = timestamp_to_time(p[4])
            if p[6]:
                _rec['end_time'] = timestamp_to_time(p[6])
                _rec['status'] = '已恢复'
            else:
                _rec['end_time'] = get_current_time()
            _rec['ctime'] = _rec['start_time']
            ZbxContent.objects.update_or_create(defaults=_rec, **{'eventid': p[0]})


def update_last_problem():

    _problem = ZbxContent.objects.filter(end_time__isnull=True)
    if _problem:
        eventids = ','.join([str(i.eventid) for i in _problem])
        problems = get_problem(status=0, eventids=eventids)
        update_problem_data(problems)
