#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-19 15:04:53
# @Description :  自定义的打印log的函数

__version__ = "0.1.0"

import inspect
import time


def glog(msg: str = ""):
    function_name = str(inspect.stack()[1][3])
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"## INFO # {function_name} # {log_time}")
    print(f"{msg}")
