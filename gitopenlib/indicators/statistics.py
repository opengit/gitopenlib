#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-05 10:23:57
# @Description :  一系列统计学相关的计算函数

from collections import Counter

import numpy as np
import scipy

__version__ = "0.9.0"


def get_extremum(data: dict or list, type: str = "max"):
    """获取最大值和最小值"""
    if isinstance(data, dict):
        keys, values = list(data.keys()), list(data.values())
    elif isinstance(data, list):
        keys, values = [key for key in range(len(data))], data
    else:
        raise Exception("please check the data parameter and its type.")

    if type == "max":
        extremum = max(values)
    elif type == "min":
        extremum = min(values)
    else:
        raise Exception("please check the type parameter.")

    res_keys, res_values = list(), list()
    for k, v in zip(keys, values):
        if type == "max":
            if v >= extremum:
                res_keys.append(k)
                res_values.append(v)
        elif type == "min":
            if v <= extremum:
                res_keys.append(k)
                res_values.append(v)
    return res_keys, res_values


def coefficient_of_variation(data: list):
    """计算变异系数，又称离散系数，是一个衡量数据离散程度的、没有量纲的统计量。

    通常用来比较两组量纲差异明显的数据的离散程度，例如粉丝数量差距显著的社交媒体帐号的推文点赞量的离散程度。

    """
    mean = np.mean(data)  # 计算平均值
    std = np.std(data, ddof=0)  # 计算标准差
    cv = std / mean
    return cv


def kurtosis_skewness(data: list):
    """求一组数据的峰度 kurtosis 和 偏度 Skewness。

    正态分布的峰度为3，若峰度大于0，则说明该组数据的分布曲线相较于正态分布更加陡峭；若峰度小于0，则说明该组数据的分布曲线相较于正态分布更加平缓。换言之，峰度越大，则数据在靠近均值的部分分布得越多，在距离均值较远的部分分布得较少。
    峰度可以用来衡量风险，同样的方差下，峰度越高，越容易取极端值，风险越大。
    峰度可以帮助衡量众数的统计学意义，峰度越高，众数在描述该组数据的集中趋势的作用就越高。

    正态分布的偏度为0，用来衡量数据分布的对称性，
    当偏度小于0时，称为 Negative Skew，出现左侧长尾，
    当偏度大于0时，称为 Positive Skew，出现右侧长尾，
    当偏度的绝对值过大时，长尾一侧出现极端值的可能性较高。

    """
    arr_ = np.asarray(data)

    k_ = scipy.stats.kurtosis(arr_)
    s_ = scipy.stats.skew(arr_)

    return k_, s_


def KL_divergence(p: list, q: list):
    """计算KL散度，两者越相似，KL散度越小。

    KL散度满足非负性
    KL散度是不对称的，交换P、Q的位置将得到不同结果。

    """
    p_arr = np.asarray(p)
    q_arr = np.asarray(q)

    return scipy.stats.entropy(p_arr, q_arr)


def JS_divergence(p: list, q: list):
    """计算JS散度，两者越相似，JS散度越小。

    JS散度的取值范围在0-1之间，完全相同时为0
    JS散度是对称的

    """
    p_arr = np.asarray(p)
    q_arr = np.asarray(q)

    M = (p_arr + q_arr) / 2

    return 0.5 * scipy.stats.entropy(p, M) + 0.5 * scipy.stats.entropy(q, M)


def hist_bins(N: int, mode: int = 0):
    """计算柱状图的bins，依据 Sturges' rule 和 Rice's rule 两种方法。

    参见 http://onlinestatbook.com/2/graphing_distributions/histograms.html

    Args:
        N (int): 数据的数目
        mode (int): Sturges' rule 的计算方法选择，0 是 1+log2(N)，1 是 1+3.3log10(N)

    Returns:
        tuple: 由

    """

    s_rule = (1 + np.log2(N)) if mode == 0 else (1 + 3.3 * np.log10(N))
    r_rule = 2 * np.power(N, 1 / 3)

    return round(s_rule), round(r_rule)


def counter2percenter(data: dict):
    """convert counter dict to percenter dict.

    将 key/value 分别为数值、数值频次的字典类型数据，
    转换为，key/value 分别为数值、数值频次百分比的字典类型数据。

    Args:
        data (dict): dict类型的数据，key/value分别为数值、数值频次。

    Returns:
        dict: dict类型的数据，key/value分别为数值、数值频次百分比。
    """
    sum_ = sum(list(data.values()))

    return dict([(key, value / sum_) for key, value in data.items()])


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
