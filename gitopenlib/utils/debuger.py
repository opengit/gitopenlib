#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-09-17 11:31:23
# @Description :  Some useful things about debug.

__version__ = "0.3.02"

import sys
import traceback
import warnings


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


def exception_print():
    """打印异常信息"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)


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
