#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-12-06 14:10:44
# @Description :  有关爬虫的一些工具函数


__version__ = "0.0.1"


import random

from fake_useragent import UserAgent
from gitopenlib.utils import files as gf


def update_useragent():
    uas = set()
    for i in range(1000):
        ua = UserAgent()
        uas.add(ua.random)

    gf.file_writer(uas, "./data/", "ua.txt", backup=False)


def get_ua():
    uas = gf.read_content("./data/ua.txt")
    idx = random.randint(0, len(uas))
    return uas[idx]
