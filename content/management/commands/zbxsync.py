# -*- coding: utf-8 -*-
# @Author: Geekwolf
# @Date:   2018-03-02 14:32:24
# @Last Modified by:   Geekwolf
# @Last Modified time: 2018-03-02 14:38:44

'''
	!!!Sync Zabbix Issues to FMS Database!!!
	Usage: screen python manage.py zbxsync
'''

from django.core.management import BaseCommand
from django.conf import settings
from content.zbx import update_problem_data, update_last_problem, get_problem
import time


class Command(BaseCommand):

    help = 'Sync Zabbix Issues to FMS Database'

    def handle(self, *args, **options):
        if settings.ZABBIX_AUTO_RECORD:
            print('Start Sync Zabbix Issues to FMS Database!')
            while True:
                problems = get_problem(status=1)
                # 先更新没有恢复的历史故障状态及时间
                update_last_problem()
                # 再更新当天故障状态
                update_problem_data(problems)
                time.sleep(settings.ZABBIX_SYNC_INTERVAL)
        else:
            print('The ZABBIX_AUTO_RECORD is False in settings.py,Can\'t Sync!')
