#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:49:57
# @Description :  Powered by GitOPEN


__version__ = "0.1.0"


import pymongo
from bson.objectid import ObjectId


class ManageDB:
    """
    A simple manager class for pymongo
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._client = pymongo.MongoClient(host=self.host, port=self.port)

    def client(self):
        """
        get the mongodb client.
        """
        return self._client

    def coll(self, db_name, collection_name):
        """
        get the collection from specific db.
        """
        return self._client[db_name][collection_name]


def find_by_page(coll, page_size, parse_func):
    """
    find the data by page and process it through the parse function.

    Args:

        coll:   collection object.
        page_size:  the page size.
        parse_func: A handler function, with a parameter of type list, implemented by itself.

    Returns:    None.

    """

    current_last_id = ObjectId("000000000000000000000000")
    current_page = 0
    page_total = int(coll.find().count() / page_size)
    print("the total page : {}".format(page_total))
    data_size = 0
    while current_page <= page_total:
        print("processing the page : {}".format(current_page))
        # 查询
        condition = {"_id": {"$gt": current_last_id}}
        data = list(coll.find(condition).sort("_id", 1).limit(page_size))
        # 更新 current_last_id
        current_last_id = data[-1]["_id"]
        print("current_last_id --> {}".format(current_last_id))
        # 翻页
        current_page += 1
        # 处理数据
        parse_func(data)
        data_size += len(data)

    print("the size of all processed data : --> {}".format(data_size))
    print("done.")
