#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-09-17 11:31:23
# @Description :  Some useful things about debug.

__version__ = "0.2.01"

import sys
import traceback


def catch_except_run(func, args):
    """运行指定函数，并捕获异常

    Args:
        func (function): 指定函数。
        args (tuple): 函数参数。

    Returns:
        function: 若未报错，返回函数执行结果；若报错，返回None。

    """
    try:
        return func(*args)
    except Exception:
        traceback.print_exc()
        return None


def exit(status: int = 0):
    sys.exit(status)
