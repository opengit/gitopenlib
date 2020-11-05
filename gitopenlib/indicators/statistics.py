#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-05 10:23:57
# @Description :  一系列统计学相关的计算函数

import numpy as np
from numpy import ndarray

__version__ = "0.1.1"


def normalization(data: list or ndarray):
    """
    对一系列数据进行归一化处理，对原始数据进行线性变换把数据映射到[0,1]之间。

    Args:

        data(list or ndarray): 需要被归一化的数据。

    Returns:
        ndarray: 处理后的数据
    """
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def standardization(data: list or ndarray):
    """
    对一系列数据进行标准化处理，常用的方法是z-score标准化，处理后数据均值为0，标准差为1。

    Args:

        data(list or ndarray): 需要被标准化的数据。

    Returns:
        ndarray: 处理后的数据
    """
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma
