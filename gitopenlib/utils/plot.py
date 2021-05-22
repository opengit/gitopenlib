#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-05-22 17:08:35
# @Description :  一些画图的相关工具函数


__version__ = "0.0.1"


import matplotlib.pyplot as plt


def set_font(fname="SimHei"):
    """
    设置中文字体
    """
    # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"] = [fname]
    # 用来正常显示负号
    plt.rcParams["axes.unicode_minus"] = False
