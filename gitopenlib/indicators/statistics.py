#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-11-05 10:23:57
# @Description :  一系列统计学相关的计算函数


__version__ = "0.19.7"

import math
from collections import Counter
from typing import List, Optional, Union

import numpy as np
from gitopenlib.utils import basics as gb
from scipy import stats


def divide_bins(data: list, bins: int = 30, fmt: str = "count"):
    """
    把一个数据列表，分成多少个区间，并统计落在每个区间中的数值数目或百分比。

    主要用于手动画直方图，例如：

    ```
    color = ["#FFFFFF"] * len(bins)
    plt.bar(
        [it[0] for it in bins],
        percents,
        width=bins[1][1] - bins[1][0],
        align="edge",
        color=color,
        alpha=1,
        edgecolor="#4D79C8",
    )
    ```


    Args:
        data: 数据列表
        bins: 区间格式
        fmt: count表示统计区间数值的数目，percent表示统计区间数值数目的百分比

    Returns:
        返回值有两个，第一个是区间列表，第二个是统计结果列表
    """
    # 划分为区间
    bin_edges = divide_interval(data, bins)

    # 在判断值属于某个区间的时候，采取与python区间相同的方法：前闭后开
    res_dict = dict()

    for it in data:
        for idx, bin in enumerate(bin_edges):
            if bin[0] not in res_dict:
                res_dict[bin[0]] = 0
            if idx == len(bin_edges) - 1:
                if it >= bin[0] and it <= bin[1]:
                    res_dict[bin[0]] += 1
            else:
                if it >= bin[0] and it < bin[1]:
                    res_dict[bin[0]] += 1

    res_dict = gb.dict_sorted(res_dict)
    if fmt == "count":
        counts = list(res_dict.values())
        return bin_edges, counts
    elif fmt == "percent":
        data_len = len(data)
        percents = [round(it / data_len, 5) for it in res_dict.values()]
        return bin_edges, percents
    else:
        raise Exception("fmt's value should be 'count' or 'percent'.")


def divide_interval(
    data: List[Union[int, float]], number: int, decimal: int = None
) -> List[list]:
    """把列表中数据，划分为区间

    Args:
        data: 列表类型数据，元素为整型或者浮点型。
        number: 划分的区间数目，整数类型。
        decimal: 区间端点的小数位数，默认不保留小数。

    Returns:
        返回值为列表类型，元素为划分的区间，tuple类型。

    """
    if number == 0:
        raise Exception("the number of interval can't be 0.")
    max_, min_ = max(data), min(data)
    poor = max_ - min_
    width = poor / number

    result = []
    interval = list()

    for i in range(number + 1):
        right = min_ + width * i
        if decimal:
            right = round(right, decimal)
        interval.append(right)
        if len(interval) == 2:
            result.append(tuple(interval))
            temp = tuple(interval)[-1]
            interval.clear()
            interval.append(temp)

    return result


def calculate_hist_bins2(data: list, k: float = 1.5) -> float:
    """求解画柱状图时的 bins 的数值，原理是 Freedman–Diaconis rule。"""
    iqr = calculate_IQR(data, k)[-1]
    bin_with = 2 * iqr * (1 / math.pow(len(data), 1 / 3))
    bins = (max(data) - min(data)) / bin_with
    return bins


def calculate_CDF(data: Union[list, dict]) -> dict:
    """计算 Cumulative Distribution Function (CDF)

    Args:
        data: 数据。

    Returns:
        每个key对应计算的累计频率。

    """

    if isinstance(data, list):
        data = dict(Counter(data))

    data = gb.dict_sorted(data)

    keys = list(data.keys())
    values = list(data.values())
    sum_ = sum(values)

    new_values = list()
    for index, item in enumerate(data):
        new_values.append(sum(values[: index + 1]) / sum_)

    return dict(zip(keys, new_values))


def calculate_CCDF(data: Union[list, dict]) -> dict:
    """计算 Complementary Cumulative Distribution Function (CCDF)

    Args:
        data: 数据。

    Returns:
        每个key对应计算的互补累计频率。

    """
    return {k: 1 - v for k, v in calculate_CDF(data).items()}


def calculate_PMF(data: Union[list, dict]) -> dict:
    """计算 Probability Mass Function (PMF)

    Args:
        data: 数据。

    Returns:
        每个key对应计算的单个频率。

    """

    if isinstance(data, list):
        data = dict(Counter(data))

    data = gb.dict_sorted(data)

    keys = list(data.keys())
    values = list(data.values())
    sum_ = sum(values)

    new_values = [it / sum_ for it in values]

    return dict(zip(keys, new_values))


def calculate_percent(data: dict, mode: str = "gte") -> None:
    """计算Counter形式的百分比。

    当 mode 为 gte 时，计算 大于等于 key 的占比；
    当 mode 为 lte 时，计算 小于等于 key 的占比。
    将结果打印到控制台。

    Args:
        data: Counter形式的数据；
        mode: 可选值为 gte 和 lte。

    Returns:
        None
    """
    data = gb.dict_sorted(data)
    x = list(data.keys())
    y = list(data.values())
    if isinstance(y[0], list):
        y = [sum(v) for v in y]
    total_count = sum(y)

    if mode == "gte":
        for flag in x:
            count = 0
            for i, k in enumerate(x):
                if k >= flag:
                    count += y[i]
            msg = f"key->{flag}->count->{count}->gte percent->{round(count/total_count,5)*100}%"
            print(msg)
    elif mode == "lte":
        res = calculate_CDF(data)
        for key, value in res.items():
            msg = f"key->{key}->count->{data[key]}->lte percent->{round(value,5)*100}%"
            print(msg)
    else:
        raise Exception("This operation has not been implemented.")


def curve_fit(x: np.array, y: np.array, deg: int) -> tuple:
    """
    对x,y进行曲线拟合。

    使用方法：
    1. 先画出散点图，观察数据的大致形状（如3次函数）；
    2. 使用该函数进行拟合，deg设置为3；
    3. 得到拟合后的x对应的y_fit值、R^2、已经方程。

    Args:
        x (np.array): 自变量x的值，可用list数据转为np.array。
        y (np.array): 因变量y的值，可用list数据转为np.array。

    Returns:
        y_fit (np.array): 拟合曲线对应的y值。
        r2 (np.float64): 拟合效果评价指标。
        aa (str): 方程的表现形式。
    """
    parameter = np.polyfit(x, y, deg)
    p = np.poly1d(parameter)
    print(p)
    aa = ""
    for i in range(deg + 1):

        bb = parameter[i]

        sup = deg - i
        if i != 0:
            if bb < 0:
                aa = list(aa)
                aa[-1] = "-"
                aa = "".join(aa)
                bb = 0 - bb
        if sup != 0:
            aa += "{:.3g}".format(bb) + " $x^{" + str(sup) + "}$ " + "+"
        else:
            aa += "{:.3g}".format(bb)

    r2 = round(np.corrcoef(y, p(x))[0, 1] ** 2, 3)
    y_fit = p(x)
    aa = "$y_{fit}$ = " + aa
    return y_fit, r2, aa


def normal_distribution_values(u: Union[int, float], std: Union[int, float]) -> tuple:
    """生成均值为u标准差为std的正态分布数据

    用处：当样本数据集确定（list），可以求出均值、标准差，
    生成相应的符合正态分布的y值，画出正态分布曲线，
    用于比较样本集与正态分布的区别，帮助判断


    Args:
        u: 平均值。
        std: 标准差。

    Returns:
        x (list): x轴的数据
        y (list): y轴的数据

    """
    x = np.linspace(u - 3 * std, u + 3 * std, 100)
    y = np.exp(-((x - u) ** 2) / (2 * std ** 2)) / (math.sqrt(2 * math.pi) * std)
    return x, y


def Cdf(t, x) -> float:
    """累计分布函数，就是值到其在分布中百分等级的映射。

    计算给定x的CDF(x)，就是计算样本中小于等于x的值的比例。
    在画图时，样本的CDF是一个阶跃函数（图形形状类似向上的阶梯）。

    Args:
        t (list): 样本集
        x (int or float): 给定值

    Returns:
        (float): 概率，小于等于x的值的概率

    """
    count = 0.0
    for value in t:
        if value <= x:
            count += 1.0
    prob = count / len(t)
    return prob


def percentile_rank(scores: list, your_score: Union[int, float]) -> Union[int, float]:
    """获取百分等级

    百分等级就是原始分数不 高于你的人在全部考试人数中所占的比例再乘以100。
    如果你 在 90 百分位数，那就是说你比 90% 的人成绩好，或者至少不比 90% 的考试人员差。

    Args:
        scores (list): 分数列表
        your_score (int or float): 考察对象的分数

    Returns:
        (int or float): 百分位数
    """
    count = 0
    for score in scores:
        if score <= your_score:
            count += 1
    percentile_rank = 100.0 * count / len(scores)
    return percentile_rank


def percentile(scores, prank) -> Union[int, float]:
    """根据百分等级，找到百分位数

    Args:
        scores (list): 分数列表
        prank (list): 百分等级

    Returns:
        (int or float): 百分位数

    """
    scores.sort()
    for score in scores:
        if percentile_rank(scores, score) >= prank:
            return score


def percentile2(scores, prank) -> Union[int, float]:
    """根据百分等级，找到百分位数，优化版

    Args:
        scores (list): 分数列表
        prank (list): 百分等级

    Returns:
        (int or float): 百分位数

    """
    scores.sort()
    index = percentile_rank * (len(scores) - 1) / 100
    return scores[index]


def get_high_low_threshold(minimum_count: int) -> float:
    """
    获取关键词的高低频临界值。高频低频词界分公式是 Donohue 根据齐普夫第二定律。
    依据的论文：
    Donohue J C. Understanding Scientific Literatures—A Bibliometric Approach [ M] . Cambridge:The MIT Press, 1973 :49 –50 .

    Args:
        minimum_count (int): 频次为1的关键词的数量。

    Returns:
        float : 临界值是浮点型。
    """
    return (-1 + math.sqrt(1 + 8 * minimum_count)) / 2


def get_extremum(data: Optional[dict or list], type: str = "max"):
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


def coefficient_of_variation(data: list) -> float:
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

    k_ = stats.kurtosis(arr_)
    s_ = stats.skew(arr_)

    return k_, s_


def KL_divergence(p: list, q: list):
    """计算KL散度，两者越相似，KL散度越小。

    KL散度满足非负性
    KL散度是不对称的，交换P、Q的位置将得到不同结果。

    """
    p_arr = np.asarray(p)
    q_arr = np.asarray(q)

    return stats.entropy(p_arr, q_arr)


def JS_divergence(p: list, q: list):
    """计算JS散度，两者越相似，JS散度越小。

    JS散度的取值范围在0-1之间，完全相同时为0
    JS散度是对称的

    """
    p_arr = np.asarray(p)
    q_arr = np.asarray(q)

    M = (p_arr + q_arr) / 2

    return 0.5 * stats.entropy(p, M) + 0.5 * stats.entropy(q, M)


def calculate_hist_bins1(N: int, mode: int = 0) -> tuple:
    """计算柱状图的bins，依据 Sturges' rule 和 Rice's rule 两种方法。

    参见 http://onlinestatbook.com/2/graphing_distributions/histograms.html

    Args:
        N (int): 数据的数目
        mode (int): Sturges' rule 的计算方法选择，0 是 1+log2(N)，1 是 1+3.3log10(N)

    Returns:
        两种方法求 hist bins 的值

    """

    s_rule = (1 + np.log2(N)) if mode == 0 else (1 + 3.3 * np.log10(N))
    r_rule = 2 * np.power(N, 1 / 3)

    return round(s_rule), round(r_rule)


def counter2percenter(data: dict) -> dict:
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


def calculate_IQR(data: list, k: float = 1.5) -> tuple:
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


def filter_outliers_by_IQR(data: list, k: float = 1.5) -> tuple:
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


def remove_outliers_by_IQR(data: list, k: float = 1.5) -> list:
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


def calculate_list_count_percent(data: list, decimals: Optional[int] = None) -> tuple:
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


def smooth_ma(data: Optional[list or np.array], window_size=3):
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


def smooth_matlab(data: Optional[list or np.array], window_size: int = 3):
    """
    这个方法是matlab中平滑函数的python实现。它的窗口只能为奇数。
    平滑后的数组的长度为：len(data)

    Args:
        data (list or np.array): 原始数组。
        window_size (int): 窗口大小。

    Returns:
        np.array: 平滑后的数组。

    """

    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(data, np.ones(window_size, dtype=int), "valid") / window_size
    r = np.arange(1, window_size - 1, 2)
    start = np.cumsum(data[: window_size - 1])[::2] / r
    stop = (np.cumsum(data[:-window_size:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))


def normalization(data: Optional[list or np.array], decimals: None or int = None):
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


def standardization(data: Optional[list or np.array], decimals: None or int = None):
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


def zero_centered(data: Optional[list or np.array], decimals: None or int = None):
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
