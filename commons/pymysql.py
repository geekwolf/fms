# -*- coding: utf-8 -*-
# @Author: Geekwolf
# @Date:   2018-02-27 13:18:37
# @Last Modified by:   Geekwolf
# @Last Modified time: 2018-02-27 13:19:10
import pymysql.cursors
from django.conf import settings


def initdb(**kwargs):

    if kwargs:
        if kwargs['type'] == 'dict':
            connection = pymysql.connect(host=settings.ZABBIX_DB_HOST,
                                         user=settings.ZABBIX_DB_USER,
                                         password=settings.ZABBIX_DB_PASSWORD,
                                         db=settings.ZABBIX_DB_NAME,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor,)
    else:
        connection = pymysql.connect(host=settings.ZABBIX_DB_HOST,
                                     user=settings.ZABBIX_DB_USER,
                                     password=settings.ZABBIX_DB_PASSWORD,
                                     db=settings.ZABBIX_DB_NAME,
                                     charset='utf8')

    cur = connection.cursor()

    return (connection, cur)


def query(sql):

    try:
        connection, cur = initdb()
        cur.execute(sql)
        rec = cur.fetchall()
        return rec
    except Exception as e:
        print(e)
    finally:
        connection.close()


def query_dict(sql):

    try:
        connection, cur = initdb(type='dict')
        cur.execute(sql)
        rec = cur.fetchall()
        return rec
    except Exception as e:
        print(e)
    finally:
        connection.close()


def update(sql):

    error = ''
    try:
        connection, cur = initdb()
        cur.execute(sql)
        connection.commit()
    except Exception as e:
        error = str(e)
        print(e)
    finally:
        connection.close()
    return error
