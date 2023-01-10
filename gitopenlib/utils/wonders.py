#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-02-01 10:25:51
# @Description :  一些高级功能用法

__version__ = "0.8.5"

import asyncio
import warnings
from functools import wraps
from multiprocessing import Process, cpu_count
from time import time
from typing import Callable

from gitopenlib.utils import basics as gb
from gitopenlib.utils import wonders as gw


import traceback


def catch_exception(f: Callable):
    """A simple exception catcher.

    装饰器，用于捕获函数的异常信息。
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            print(f"Error # {f.__name__} # : {e}")
            print("Traceback: ")
            traceback.print_exc()
            result = None
        return result

    return wrapper


def filterwarnings(action="ignore"):
    """默认忽略警告信息。

    action 的取值如下：
        "error"     将匹配警告转换为异常
        "ignore"    忽略匹配的警告
        "always"    始终输出匹配的警告
        "default"   对于同样的警告只输出第一次出现的警告
        "module"    在一个模块中只输出第一次出现的警告
        "once"      输出第一次出现的警告,而不考虑它们的位置
    """
    warnings.filterwarnings(action)
    warnings.simplefilter(action="ignore", category=FutureWarning)


def timing(f: Callable):
    """A simple timer decorator.

    装饰器，用于统计函数的运行时间。
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_ = time()
        result = f(*args, **kwargs)
        end_ = time()
        print(
            f"Elapsed time # {f.__name__} # : {gb.time_formatter(end_ - start_, False)}"
        )
        return result

    return wrapper


@timing
def run_tasks_parallel(
    data: list,
    parse_func: Callable[[list], None],
    slave_num: int = 4,
):
    """
    并行处理数据的函数，加快处理速度。

    Args:
        data: list类型，需要被处理的数据。
        parse_func: 处理数据的函数，自行定义。
        slave_num: 并行任务数目。
    """

    async def parse_(loop, chunk):
        await loop.run_in_executor(None, lambda: parse_func(chunk))

    loop = asyncio.get_event_loop()
    chunks = gb.chunks(data, slave_num)
    loop.run_until_complete(asyncio.gather(*[parse_(loop, chunk) for chunk in chunks]))


@timing
def run_tasks_by_multithread(
    data: list,
    parse_func: Callable[[list], None],
    thread_num: int = 4,
):
    """
    使用多线程并行执行。

    Args:
        data: list类型，需要被处理的数据。
        parse_func: 处理数据的函数，自行定义。
        thread_num: 线程数目。
    """

    async def parse_(loop, chunk):
        await loop.run_in_executor(None, lambda: parse_func(chunk))

    loop = asyncio.get_event_loop()
    chunks = gb.chunks(data, thread_num)
    loop.run_until_complete(asyncio.gather(*[parse_(loop, chunk) for chunk in chunks]))


def cpu_core_count():
    """
    获取CPU的核数，等于线程数除以2。
    """
    return cpu_count() / 2


@timing
def run_tasks_by_multiprocess(
    data,
    parse_func: Callable[[list], None],
    process_num: int = 4,
):
    """
    使用多进程并行执行。
    **注意**：使用多进程时，parse_func需要放在py文件的顶级缩进（顶着行首），
    即，不能放到任何其他块体内。

    Args:
        data: list类型，需要被处理的数据。
        parse_func: 处理数据的函数，自行定义。
        process_num: 多进程数目。
    """
    chunks = gb.chunks(data, process_num)
    process_list = []
    for index, chunk in enumerate(chunks):
        p = Process(target=parse_func, args=(chunk,))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
