#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-01-11 18:55:11
# @Description :  存放常用的工具类

__version__ = "0.2.0"

from functools import partial


class AutoVivification(dict):
    """实现嵌套字典的自动创建"""

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class F(partial):
    """实现管道。

    examples:
        >>> range(10) | F(filter, lambda x: x % 2) | F(sum)
        >>> your_dict | F(lambda d: {k: v for k, v in d.items() if v})
    """

    def __ror__(self, other):
        if isinstance(other, tuple):
            return self(*other)
        return self(other)
