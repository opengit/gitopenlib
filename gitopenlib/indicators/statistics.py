#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-05 10:23:57
# @Description :  一系列统计学相关的计算函数

from collections import Counter

import numpy as np

__version__ = "0.4.0"


def calculate_IQR(data: list, k: float = 1.5):
    """计算四分位距（IQR, Interquartile range）

    Args:
        data (list): list类型的数据，每个元素为 int 或 float 类型。
        k (float): 表示异常系数，k = 1.5表示中度异常，k = 3表示极度异常。

    Returns:
        tuple: 顺序为：upper whisker, upper quartile, median, lower quartile, lower whisker, IQR
    """
    Percentile = np.percentile(data, [0, 25, 50, 75, 100])
    upper_quartile = Percentile[3]
    lower_quartile = Percentile[1]
    IQR = upper_quartile - lower_quartile
    upper_whisker = upper_quartile + IQR * k
    lower_whisker = lower_quartile - IQR * k
    median = Percentile[2]

    return upper_whisker, upper_quartile, median, lower_quartile, lower_whisker, IQR


def filter_outliers_by_IQR(data: list, k: float = 1.5):
    """
    使用IQR对异常值进行检测，又称为 Tukey's test。

    Args:
        data (list): list类型的数据，每个元素为 int 或 float 类型。
        k (float): 表示异常系数，k = 1.5表示中度异常，k = 3表示极度异常。

    Returns:
        tuple: upper outliers, lower outliers

    """
    (
        upper_whisker,
        upper_quartile,
        median,
        lower_quartile,
        lower_whisker,
        IQR,
    ) = calculate_IQR(data, k=k)
    print(" upper_whisker : ", upper_whisker)
    print(" lower_whisker : ", lower_whisker)
    upper_outliers = [item for item in data if item > upper_whisker]
    lower_outliers = [item for item in data if item < lower_whisker]

    return upper_outliers, lower_outliers


def remove_outliers_by_IQR(data: list, k: float = 1.5):
    """
    使用IQR从数据中移除异常值，返回移除异常值的数据

    Args:
        data (list): list类型的数据，每个元素为 int 或 float 类型。
        k (float): 表示异常系数，k = 1.5表示中度异常，k = 3表示极度异常。

    Returns:
        list: 移除异常值后的数据
    """
    (
        upper_whisker,
        upper_quartile,
        median,
        lower_quartile,
        lower_whisker,
        IQR,
    ) = calculate_IQR(data, k=k)

    new_data = [
        item for item in data if item <= upper_whisker and item >= lower_whisker
    ]
    return new_data


def calculate_list_count_percent(data: list, decimals: None or int = None):
    """计算list中元素的次数和百分比

    Args:
        data (list): list类型数据。
        decimals (None or int): 保留的小数位数，默认为None，则不进行位数操作；如果>=0，则保留相应的小数位数。

    Returns:
        tuple: 元组第一个元素为次数统计结果，第二个元素为百分比统计结果。

    """
    counter = dict(Counter(data))

    total_count = sum(list(counter.values()))

    percenter = dict(
        [
            (
                key,
                value / total_count
                if decimals is None
                else round(value / total_count, decimals),
            )
            for key, value in counter.items()
        ]
    )
    return counter, percenter


def smooth_ma(data: list or np.array, window_size=3):
    """
    平滑后的数组的长度为：len(data) - window_size + 1

    Args:
        data (list or np.array): 原始数组。
        window_size (int): 窗口大小。

    Returns:
        np.array: 平滑后的数组
    """
    cumsum_vec = np.cumsum(np.insert(data, 0, 0))
    ma_vec = (cumsum_vec[window_size:] - cumsum_vec[:-window_size]) / window_size
    return ma_vec


def smooth_matlab(data: list or np.array, window_size: int = 3):
    """
    这个方法是matlab中平滑函数的python实现。它的窗口只能为奇数。
    平滑后的数组的长度为：len(data)

    Args:
        data (list or np.array): 原始数组。
        window_size (int): 窗口大小。

    Returns:
        np.array: 平滑后的数组

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
        data (list or np.array): 需要被归一化的数据。
        decimals (None or int): 归一化后，数值保留的精度（小数位数），默认为None，不开启

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
        data (list or np.array): 需要被标准化的数据。
        decimals (None or int): 归一化后，数值保留的精度（小数位数），默认为None，不开启

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
        data (list or np.array): 需要被零均值化的数据。
        decimals (None or int): 数值保留的精度（小数位数），默认为None，不开启

    Returns:
        np.array: 处理后的数据
    """
    mu = np.mean(data, axis=0)
    ret = data - mu
    return ret if decimals is None else np.around(ret, decimals=decimals)
