#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-02-01 10:25:51
# @Description :  一些高级功能用法

__version__ = "0.3.2"

import asyncio
from functools import wraps
from time import time
from typing import Callable

from gitopenlib.utils import basics as gb


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
