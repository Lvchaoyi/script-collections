#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os, sys
import time
import re
import MySQLdb


# 源系统数据库连接
SOURCE_URL = "jdbc:mysql://kideng-db-reader.corp.yodao.com:3336/db_yunke?allowMultiQueries=true"
# 源系统用户名
SOURCE_USER = "yunke_read"
# 源系统密码
SOURCE_PASSWD = "c3Dx4#6dHNHi"
# 源系统数据库名称
SOURCE_DBNAME = "db_yunke"


# 获取MYSQL连接
def openConn(hostStr, port, userStr, passwdStr, tableSchema):
    conn = MySQLdb.connect(host='%s' % (hostStr), user='%s' % (userStr), passwd='%s' % (passwdStr),
                           db='%s' % (tableSchema), port=port, charset="utf8", use_unicode="True")
    return conn


# 获取查询结果
def getRs(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        return rows
    except Exception as  e:
        print(str(e))
        pass
    finally:
        try:
            cursor.close()
        except:
            pass


# 执行SQL
def execSql(conn, sql):
    try:
        cursor = conn.cursor()
        cnt = cursor.execute(sql)
        conn.commit()
        return cnt
    except Exception as  e:
        print(str(e))
        pass
    finally:
        try:
            cursor.close()
        except:
            pass
    return -1


# 连接数据库：
def excuteSql_select(sql):
    # 获取源系统mysql连接
    if "mysql" in SOURCE_URL:
        mysqlStr = SOURCE_URL.split(":")
        print(mysqlStr[2].replace("//", ""))
        print(int(mysqlStr[3].split("/")[0]))
        conn = openConn(mysqlStr[2].replace("//", ""), int(mysqlStr[3].split("/")[0]), SOURCE_USER, SOURCE_PASSWD,
                        SOURCE_DBNAME)
        return getRs(conn, sql)
    else:
        print
        "未知类型数据库"
        sys.exit(1)


# 连接数据库：
def excuteSql(sql):
    # 获取源系统mysql连接
    if "mysql" in SOURCE_URL:
        mysqlStr = SOURCE_URL.split(":")
        conn = openConn(mysqlStr[2].replace("//", ""), int(mysqlStr[3].split("/")[0]), SOURCE_USER, SOURCE_PASSWD,
                        SOURCE_DBNAME)
        return execSql(conn, sql)
    else:
        print
        "未知类型数据库"
        sys.exit(1)


def transferTime(timestamp):
    # 获得当前时间时间戳
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(timestamp / 1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

if __name__ == '__main__':
    input = []
    output = []

    for _ in input:
        output.append()


def f(n):
    return n

# 查询数据：
# result_select = excuteSql_select("select goods_snapshot from TB_ORDER where payment_time > '2021-03-13 20:00:00' and payment_time < '2021-03-15 14:00:00' and status = 4 and goods_type in (0) and sell_price = 0")
# count = 0
# d_count = 0
# goods_id_set = set()
# start_time_set = set()
# for result in result_select:
#     result = json.loads(result[0])
#     if 'lessonPlanList' in result:
#         lesson_plan_list = json.loads(result.get('lessonPlanList'))
#         lesson_start_time = min([_.get('startTime') for _ in lesson_plan_list])
#         start_time = result.get('startTime')
#         sale_start_time = result.get('saleStartTime')
#         if start_time != lesson_start_time:
#             count += 1
#             print(result.get('goodsId'))
#             start_time_set.add(start_time)
#             goods_id_set.add(result.get('goodsId'))
#             print(transferTime(start_time))
#             print(transferTime(start_time), transferTime(sale_start_time), [transferTime(_.get('startTime')) for _ in lesson_plan_list])
#             print(count)
# print(goods_id_set)
# print(start_time_set)
# print('查询结果总条数：' + str(result_select[0][0]))

# 执行操作：
# result = excuteSql("insert into test values(3)")
# print('插入数据成功：' + str(result))
