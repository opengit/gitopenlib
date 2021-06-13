#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:49:57
# @Description :  提供一系列的有关操作mongodb/pymongo的工具


__version__ = "0.1.2.23"


import asyncio
import time
from typing import Callable

import pymongo
from bson.objectid import ObjectId
from gitopenlib.utils import basics as gb
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
        coll(Collection): collection object.
        page_size(int): the page size.
        parse_func: A handler function, with a parameter of type list,
            implemented by itself.

    Returns: None.
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


def aggregate_by_page_asyncio(
    coll,
    start_id: ObjectId = ObjectId("000000000000000000000000"),
    pipeline: list = [],
    session: ClientSession = None,
    options: dict = None,
    page_size: int = 100,
    parse_func: Callable[[list], None] = None,
    open_log: bool = False,
    log_file: str = "./aggregate_by_page.log",
    open_async: bool = False,
    slave_num: int = 4,
):
    """mongodb的聚合查询，具备分页查询、异步io处理数据功能。

    Args:
        coll(Collection): 目标Collection，要查询的Collection对象。
        start_id(ObjectId): 起始ObjectId。
        pipeline(list): 管道命令list。
        session(ClientSession): ClientSession对象。
        options(dict): aggregate的options选项设置。eg: {"allowDiskUse": True}
        page_size(int): 每页的数据条目数。
        parse_func(Callable): 每一个page的数据的处理函数。需要自己实现。
        open_log(bool): 是否开启日志，记录当前的Current ObjectId，
           方便打断任务后，再次运行时扔给start_id。
        log_file(str): 日志文件完整路径，open_log为True时需要填写，False可不填写。
        open_async(bool): 是否开启异步io处理数据，默认不开启。
        slave_num(int): 执行任务的协程数目，默认为4。

    Returns:
        None
    """

    def wprint(log_msg):
        print(log_msg)
        if open_log:
            log_file.write(log_msg + "\n")

    if open_log:
        log_file = open(log_file, "a+")

    async def parse_(loop, chunk):
        run_func = lambda: parse_func(chunk)
        await loop.run_in_executor(None, run_func)

    current_last_id = start_id
    current_page = 0

    count = coll.find().count()

    page_total = (
        int(count / page_size) if count % page_size == 0 else int(count / page_size) + 1
    )
    log_msg = "# the total page : {}".format(page_total)
    print(log_msg)

    data_size = 0
    total_time = time.time()
    while current_page < page_total:
        start_time = time.time()
        log_msg = "# processing the page : {}".format(current_page)
        wprint(log_msg)
        # 查询
        condition = [
            #  {"$sort": {"_id": 1}},
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

        log_msg = "# find this page data cost time: {}s".format(
            time.time() - start_time
        )
        wprint(log_msg)

        # 更新 current_last_id
        current_last_id = data[-1]["_id"]
        log_msg = "# current_last_id --> {}".format(current_last_id)
        wprint(log_msg)

        # 翻页
        current_page += 1
        # 处理数据
        if open_async:
            loop = asyncio.get_event_loop()
            chunks = gb.chunks(data, slave_num)
            loop.run_until_complete(
                asyncio.gather(*[parse_(loop, chunk) for chunk in chunks])
            )
            chunks.clear()
        else:
            parse_func(data)

        data_size += len(data)
        data.clear()
        log_msg = "# elapsed time: {}s".format(time.time() - start_time)
        wprint(log_msg)
        log_msg = "*" * 36
        wprint(log_msg)

    log_msg = "# the size of all processed data : --> {}\n".format(data_size)
    log_msg += "# total time cost is : --> {}\n".format(time.time() - total_time)
    log_msg += "# done."
    wprint(log_msg)
    if open_log:
        log_file.close()


def aggregate_by_page(
    coll,
    start_id: ObjectId = ObjectId("000000000000000000000000"),
    pipeline: list = [],
    session: ClientSession = None,
    options: dict = None,
    page_size: int = 100,
    parse_func: Callable[[list], None] = None,
    open_log: bool = False,
    log_file: str = "./aggregate_by_page.log",
):
    """mongodb的聚合查询，具备分页查询功能。

    Args:
        coll(Collection): 目标Collection，要查询的Collection对象。
        start_id(ObjectId): 起始ObjectId。
        pipeline(list): 管道命令list。
        session(ClientSession): ClientSession对象。
        options(dict): aggregate的options选项设置。eg: {"allowDiskUse": True}
        page_size(int): 每页的数据条目数。
        parse_func(Callable): 每一个page的数据的处理函数。需要自己实现。
        open_log(bool): 是否开启日志，记录当前的Current ObjectId，
            方便打断任务后，再次运行时扔给start_id。
        log_file(str): 日志文件完整路径，open_log为True时需要填写，False可不填写。

    Returns:
        None
    """

    def wprint(log_msg):
        print(log_msg)
        if open_log:
            log_file.write(log_msg + "\n")

    if open_log:
        log_file = open("aggregate_by_page.log", "a+")

    current_last_id = start_id
    current_page = 0
    #  count = coll.find({"_id": {"$gt": current_last_id}}).count()
    count = coll.find().count()
    page_total = (
        int(count / page_size) if count % page_size == 0 else int(count / page_size) + 1
    )
    log_msg = "# the total page : {}".format(page_total)
    print(log_msg)

    data_size = 0
    total_time = time.time()

    while current_page < page_total:
        start_time = time.time()
        log_msg = "# processing the page : {}".format(current_page)
        wprint(log_msg)
        # 查询
        condition = [
            #  {"$sort": {"_id": 1}},
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
        log_msg = "# current_last_id --> {}".format(current_last_id)
        wprint(log_msg)
        # 翻页
        current_page += 1
        # 处理数据
        parse_func(data)
        data_size += len(data)
        data.clear()
        log_msg = "# elapsed time: {}s".format(time.time() - start_time)
        wprint(log_msg)
        log_msg = "*" * 36
        wprint(log_msg)

    log_msg = "# the size of all processed data : --> {}\n".format(data_size)
    log_msg += "# total time cost is : --> {}\n".format(time.time() - total_time)
    log_msg += "# done."
    wprint(log_msg)
    if open_log:
        log_file.close()
