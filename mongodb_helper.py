#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import time, datetime

from pymongo import MongoClient


def get_collection(name):
    """
    获取collection
    :param name:
    :return:
    """
    c = MongoClient(host="mongodb://10.108.182.149:27021,10.108.182.150:27021,zj195:27020,zj198:27020,zj199:27020/yunke")
    db = c.get_database()
    return db.get_collection(name)



def delete_user():
    c = get_collection("user")
    cursor = list(c.find({"userRoleList": [], "telephone": {"$ne": None}, "createTime": {"$lte": datetime(2021, 10, 11)}}))
    print("数据总条数为：", len(cursor))
    print("数据详细为：")
    for _ in cursor:
        print(_ + "\n")
    # for _ in cursor:
    #     c.delete_one({"_id": _.get("_id")})
    #     print("数据已删除,id为：", _.get("_id"))


def fix_user():
    c = get_collection("user")
    cursor = list(c.find({"userRoleList.areaIds": 271, "userRoleList.schoolIds": [], "email": {"$ne": None}}))
    print("数据总条数为：", len(cursor))
    print("数据详细为：")
    for _ in cursor:
        print(_ + "\n")
    # for _ in cursor:
    #     c.update_one({"_id": _.get("_id")},
    #                  {"$addToSet": {"userRoleList.$.schoolIds": 10010, "userRoleList.$.classIds": 10033}})
    #     print("数据已更新,id为：", _.get("_id"))
    #     print("更新之后数据为：", c.find_one({"_id": _.get("_id")}))



if __name__ == '__main__':
    delete_user()
    fix_user()

