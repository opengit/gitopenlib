#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN / Big Teacher Brother
# @Email  :  gitopen@gmail.com
# @Date   :  2021-04-01 15:01:56
# @Description :  熵权法，计算指标的权重

__version__ = "0.2.0"

import math

import numpy as np
import pandas as pd
from pandas import DataFrame


class EntropyValueMethod:
    """使用熵权法计算指标的权重(Method 2)

    example:
        ```python
        evm = EntropyValueMethod(df_new.to_numpy())
        entropy_values = [
            str(round(it, 5)) for it in list(evm.calculate_entropy())
        ]
        weight_values = [
            str(round(it, 5)) for it in list(evm.calculate_weights())
        ]
        scores = evm.calculate_scores()
        ```
    """

    def __init__(self, data):
        self.data = data

    def calculate_entropy(self):
        m, n = self.data.shape
        K = 1 / np.log(m)
        data_p = self.data / self.data.sum(axis=0)
        self.e_j = -K * (data_p * np.log(data_p)).sum(axis=0)
        return self.e_j

    def calculate_weights(self):
        self.e_j = self.calculate_entropy()
        d_j = 1 - self.e_j
        W_j = d_j / d_j.sum()
        return W_j

    def calculate_scores(self):
        self.W_j = self.calculate_weights()
        self.scores = (self.data * self.W_j).sum(axis=1)
        return self.scores

    def show_result(self, lang="en"):
        if lang == "en":
            print("Entropy values of indicators: ", self.e_j)
            print("Weights of indicators: ", self.W_j)
            print("Efficiency scores of objects: ", self.scores)
        else:
            print("各指标的熵值：", self.e_j)
            print("各指标的权重：", self.W_j)
            print("各对象的效率得分：", self.scores)


def cal_weight(data: DataFrame or list, out_dict: bool = True):
    """
    使用熵权法计算指标的权重(Method 1)

    Args:
        data (DataFrame or list): 类型为list或者pandas的DataFrame。
        out_dict (bool): 若为True，则转化为键值对以dict类型返回；否则，以DataFrame类型返回。

    return:
        dict or DataFrame: 返回的权重值。

    """

    if isinstance(data, list):
        data = pd.DataFrame(data)

    # 去除空值
    data.dropna()

    # 归一化
    data = data.apply(
        lambda data: ((data - np.min(data)) / (np.max(data) - np.min(data)))
    )
    # 列名，也就是每个参数的名称
    columns = data.columns

    # 求k，即 -1/ln(n)
    rows = data.index.size  # 行
    cols = data.columns.size  # 列
    k = 1.0 / math.log(rows)

    # 矩阵计算
    # 信息熵
    data = np.array(data)
    lnf = [[None] * cols for i in range(rows)]
    lnf = np.array(lnf)
    for i in range(0, rows):
        for j in range(0, cols):
            if data[i][j] == 0:
                lnfij = 0.0
            else:
                p = data[i][j] / data.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(lnf)
    E = lnf

    # 计算冗余度
    d = 1 - E.sum(axis=0)

    # 计算各指标的权重
    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj

    w = pd.DataFrame(w)
    w.index = columns
    w.columns = ["weight"]
    result = w.transpose()
    if out_dict:
        for idx, row in result.iterrows():
            result = dict(row)
    return result
