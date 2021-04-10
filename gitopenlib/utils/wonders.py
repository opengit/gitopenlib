#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-02-01 10:25:51
# @Description :  一些”魔术“方法

__version__ = "0.2.1"

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
