#!/usr/bin/python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

from utils.excel_helper import XlsxHelper


class MongoHelper(object):
    """
    mongo数据小工具
    """

    def __init__(self, host: str, db: str):
        """
        连接初始化
        :param host: 地址
        :param db: 数据库名
        """
        self.host = host
        self.db = db
        self.conn = MongoClient(self.host).get_database(self.db)

    def get_collection(self, collection_name):
        """
        获取数据库连接
        :return:
        """
        return self.conn.get_collection(collection_name)

    def data_handler(self, collection_name, query, **kwargs):
        """
        数据处理
        :param collection_name: 表名
        :param query: 查询条件
        :param update: 更新内容
        :return:
        """
        c = self.get_collection(collection_name)
        # 首先查看需要处理数据的条数
        total = c.count_documents(query)
        print("数据总条数为：", total)
        cursor = c.find(query)
        for _ in cursor:
            _id = _.get("_id")
            print("数据id为：", _id)


if __name__ == '__main__':
    xlsx_helper = XlsxHelper()
    data_list = xlsx_helper.get_data_list("tw.xlsx")
    mongo_helper = MongoHelper(host="mongodb://zj367.corp.yodao.com:31000,zj370.corp.yodao.com:31000,zj373.corp.yodao.com:31000", db="yunke")
    print(len(data_list))
    mongo_helper.data_handler("user", {"educationId": {"$in": [str(_[0]).strip() for _ in data_list]}})
    for orgin, new in [(str(_[0]).strip(), str(_[1]).strip()) for _ in data_list]:
        # print(mongo_helper.get_collection("user").find_one({"educationId": orgin}) is None)
        origin_data = mongo_helper.get_collection("user").find_one({"educationId": orgin})
        new_data = mongo_helper.get_collection("user").find_one({"educationId": new})
        if new_data is not None:
            print("origin: ", origin_data)
            print("new: ", new_data)
        else:
            pass
            # mongo_helper.get_collection("user").update_one({"educationId": orgin}, {"$set": {"educationId": new}})
        # print(mongo_helper.get_collection("user").find_one({"educationId": new}) is None)

