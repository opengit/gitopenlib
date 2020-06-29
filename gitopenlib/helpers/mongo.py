#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:49:57
# @Description :  提供一系列的有关操作mongodb/pymongo的工具


__version__ = "0.1.2.5"


import time
from types import FunctionType

import pymongo
from bson.objectid import ObjectId
from pymongo.client_session import ClientSession
from pymongo.collection import Collection


class ManageDB:
    """
    A simple manager class for pymongo
    """

    def __init__(self, host="127.0.0.1", port=27017):
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

        coll(Collection):   collection object.
        page_size(int):  the page size.
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
        data = list(coll.find(condition).limit(page_size))
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


def aggregate_by_page(
    coll,
    start_id: ObjectId = ObjectId("000000000000000000000000"),
    pipeline: list = [],
    session: ClientSession = None,
    options: dict = None,
    page_size: int = 100,
    parse_func: FunctionType = None,
):
    """mongodb的聚合查询，具备分页查询功能。

    Args:

        coll(Collection): 目标Collection，要查询的Collection对象。
        start_id(ObjectId): 起始ObjectId。
        pipeline(list): 管道命令list。
        session(ClientSession): ClientSession对象。
        options(dict): aggregate的options选项设置。eg: {"allowDiskUse": True}
        page_size(int): 每页的数据条目数。
        parse_func(FunctionType): 每一个page的数据的处理函数。需要自己实现。

    Returns:
        None
    """
    current_last_id = start_id
    current_page = 0
    count = coll.find({"_id": {"$gt": current_last_id}}).count()
    page_total = (
        int(count / page_size) if count % page_size == 0 else int(count / page_size) + 1
    )
    print("# the total page : {}".format(page_total))
    data_size = 0

    while current_page < page_total:
        start_time = time.time()
        print("# processing the page : {}".format(current_page))
        # 查询
        condition = [
            {"$sort": {"_id": 1}},
            {"$match": {"_id": {"$gt": current_last_id}}},
            {"$limit": page_size},
        ]
        condition.extend(pipeline)
        cursor = (
            coll.aggregate(pipeline=condition, session=session, **options)
            if options
            else coll.aggregate(pipeline=condition, session=session)
        )
        data = [x for x in cursor]
        # 更新 current_last_id
        current_last_id = data[-1]["_id"]
        print("# current_last_id --> {}".format(current_last_id))
        # 翻页
        current_page += 1
        # 处理数据
        parse_func(data)
        data_size += len(data)
        print("# elapsed time: {}s".format(time.time() - start_time))
        print("*" * 36)

    print("# the size of all processed data : --> {}".format(data_size))
    print("# done.")
