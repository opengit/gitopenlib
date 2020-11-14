#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-05 10:23:57
# @Description :  一系列统计学相关的计算函数

import numpy as np

__version__ = "0.2.2"


def smooth_ma(data: list or np.array, window_size=3):
    """
    平滑后的数组的长度为：len(data) - window_size + 1

    Args:
        data(list or np.array): 原始数组。
        window_size(int): 窗口大小。

    Returns:
        (np.array): 平滑后的数组
    """
    cumsum_vec = np.cumsum(np.insert(data, 0, 0))
    ma_vec = (cumsum_vec[window_size:] - cumsum_vec[:-window_size]) / window_size
    return ma_vec


def smooth_matlab(data: list or np.array, window_size: int = 3):
    """
    这个方法是matlab中平滑函数的python实现。它的窗口只能为奇数。
    平滑后的数组的长度为：len(data)

    Args:
        data(list or np.array): 原始数组。
        window_size(int): 窗口大小。

    Returns:
        (np.array): 平滑后的数组

    """

    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(data, np.ones(window_size, dtype=int), "valid") / window_size
    r = np.arange(1, window_size - 1, 2)
    start = np.cumsum(data[: window_size - 1])[::2] / r
    stop = (np.cumsum(data[:-window_size:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))


def normalization(data: list or np.array, decimals: None or int = None):
    """
    对一系列数据进行归一化处理，对原始数据进行线性变换把数据映射到[0,1]之间。

    Args:

        data(list or np.array): 需要被归一化的数据。
        decimals(None or int): 归一化后，数值保留的精度（小数位数），默认为None，不开启

    Returns:
        np.array: 处理后的数据
    """
    _range = np.max(data) - np.min(data)
    ret = (data - np.min(data)) / _range
    return ret if decimals is None else np.around(ret, decimals=decimals)


def standardization(data: list or np.array, decimals: None or int = None):
    """
    对一系列数据进行标准化处理，常用的方法是z-score标准化，处理后数据均值为0，标准差为1。

    Args:

        data(list or np.array): 需要被标准化的数据。
        decimals(None or int): 归一化后，数值保留的精度（小数位数），默认为None，不开启

    Returns:
        np.array: 处理后的数据
    """
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    ret = (data - mu) / sigma
    return ret if decimals is None else np.around(ret, decimals=decimals)


def zero_centered(data: list or np.array, decimals: None or int = None):
    """
    对一系列数据进行零均值化，即zero-centered。对数据的平移的一个过程，之后数据的中心点为(0,0)。

    Args:

        data(list or np.array): 需要被零均值化的数据。
        decimals(None or int): 数值保留的精度（小数位数），默认为None，不开启

    Returns:
        np.array: 处理后的数据
    """
    mu = np.mean(data, axis=0)
    ret = data - mu
    return ret if decimals is None else np.around(ret, decimals=decimals)
