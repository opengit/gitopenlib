#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-12-06 14:10:44
# @Description :  有关爬虫的一些工具函数


__version__ = "0.0.3"


import random
import time
from pathlib import Path

from fake_useragent import UserAgent
from gitopenlib.utils import files as gf


def have_a_sleep(min=1, max=10):
    """
    随机睡眠一段时间，小数秒
    """
    time.sleep(random.uniform(min, max))


def update_useragent():
    uas = set()
    for i in range(1000):
        ua = UserAgent()
        uas.add(ua.random)

    gf.file_writer(uas, "./ua/", "ua.txt", backup=False)


def get_ua():
    """随机获取一个 User-Agent"""
    ua_path = "./ua/ua.txt"
    if not Path(ua_path).exists():
        update_useragent()
    uas = gf.read_content(ua_path)
    idx = random.randint(0, len(uas) - 1)
    return uas[idx]
