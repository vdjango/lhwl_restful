#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-12 11:48:12
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$
import random
import time
import pytz
from datetime import datetime
from django.utils.timezone import utc
from lhwill import settings


def UTCS():
    return datetime.utcnow().replace(tzinfo=utc)


def datetimenow(data=None):
    ZONE = pytz.timezone(settings.TIME_ZONE)
    if data == None:
        data = UTCS()
        return data.astimezone(ZONE)
    else:
        try:
            t = time.strptime(data, "%Y - %m - %d %H:%M")
            y, m, d = t[0:3]
            d = datetime(y, m, d)
        except Exception as e:
            t = time.strptime(data, "%Y - %m - %d")
            y, m, d = t[0:3]
            d = datetime(y, m, d)
        print(d)
    s = d.astimezone(ZONE)
    print(s)
    return s


def datetimenowS(data=None):
    local_time = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()))
    return local_time


def datetime_unix():
    unix = datetimenow()
    unix = time.mktime(unix.timetuple())
    return int(unix)


def _order_num(package_id=12345, user_id=56789):
    # 商品id后2位+下单时间的年月日12+用户后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result


def datetime_ymd():
    data = datetimenow()
    time = "%s-%s-%s %s:%s:%s" % (data.year, data.month,
                                  data.day, data.hour, data.minute, data.second)

    return time


def DateTimes(date):
    '''
    datetime_from_db = '2015-10-26 00:00:00'
    '''
    datetime_from = datetime.now()

    datetime_of = datetime.strptime(
        date, "%Y-%m-%d %H:%M:%S")

    data_year = str(datetime_of).split(" ")[0].split("-")[0]  # '年'
    data_month = str(datetime_of).split(" ")[0].split("-")[1]  # '月'
    data_day = str(datetime_of).split(" ")[0].split("-")[2]  # '日'
    data_time = str(datetime_of).split(" ")[1].split(":")[0]  # '时'
    data_branch = str(datetime_of).split(" ")[1].split(":")[1]  # '分'
    data_second = str(datetime_of).split(" ")[1].split(":")[2]  # '秒'

    data_for_year = str(datetime_from).split(" ")[0].split("-")[0]  # '年'
    data_for_month = str(datetime_from).split(" ")[0].split("-")[1]  # '月'
    data_for_day = str(datetime_from).split(" ")[0].split("-")[2]  # '日'
    data_for_time = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[0]  # '时'
    data_for_branch = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[1]  # '分'
    data_for_second = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[2]  # '秒'

    date_of = data_year + data_month + data_day
    date_for = data_for_year + data_for_month + data_for_day

    date_of_t = data_time + data_branch + data_second
    date_for_t = data_for_time + data_for_branch + data_for_second

    number = int(date_for) - int(date_of)
    # number_time = int(date_for_t) - int(date_of_t)

    # 240000
    if number < 1 and number > -1:
        return True, number
    else:
        return False, number


def date_new(date):
    '''
    将字符串时间转换时间对象
    支持 [04/25/2017]
    :param date:
    :return:
    '''
    try:
        print('DDDDDDDDDD', date)
        d = datetimenow(date)
        print('DDDDDDDDDD', d)
        return d
    except Exception as e:
        time = str(date).split('/')
        if len(time[0]) > 2:
            dates = '{} - {} - {}'.format(
                time[0],
                time[1],
                time[2],
            )
            print('0', dates)
            return datetimenow(dates)
            pass
        if len(time[2]) > 2:
            dates = '{} - {} - {}'.format(
                time[2],
                time[0],
                time[1],
            )
            print('2', dates)
            return datetimenow(dates)
            pass
    pass
