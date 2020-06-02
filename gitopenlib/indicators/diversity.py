#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 10:28:49
# @Description :  some useful functions of indexes or indicators that measure
#                   the degree of diversity.

__version__ = "0.1.0"

import math


def category_count(data: list):
    """学科数量丰富度variety，即category count（MacArthur 1965）

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        int: 学科数量，也可以理解为分类的数量
    """
    return len(data)


def disparity(data: list):
    """学科差异度，（Weizman(1992a)、Solow & Polasky(1994a)

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        int: 返回差异性指标
    """
    pass


def shannon_evenness(data: list):
    """学科分布均匀度balance，即Shannon evenness(Pielou 1969)，又称为Shannon’s equitability

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: Shannon evenness的数值，衡量社区（当前区域/领域)的物种均匀程度

    """
    si = shannon_index(data)

    # Maximum diversity possible
    h_max = math.log(category_count(data))

    return float(si) / h_max


def shannon_index(data: list):
    """考虑了variety/balance，Shamono & Weaver（1962）。

    Shannon指数是生态文献中比较流行的多样性指数，
    也叫Shannon Diversity Index、Shannon-Wiener指数、Shannon-Weaver指数和Shannon Entropy。

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: Shannon Diversity Index
    """

    def p(n, N):
        """
        计算相对丰富度

        Args:
            n(int): 每个物种（分类）的数目
            N(int): 所有物种（分类）的总数

        Returns:
            float: 相对丰度值
        """
        ratio = float(n) / N
        return ratio * math.log(ratio)

    N = sum(data)
    return -sum(p(n, N) for n in data)


def simpson_index(data: list):
    """考虑了 variety/balance，Simpson（1949），有关Simpson Index的名称（叫法），
    在不同的地方有不同的形式，请参考链接 http://www.countrysideinfo.co.uk/simpsons.htm。

    Simpson Index 衡量个体被分类时的集中程度，描述从一个群落中连续两次抽样所得到的个体属于同一种的概率
    SI 的值域为[0, 1]，0意味着无限多样性，1意味着没有多样性，即值越大，多样性越小。
    由于该形式的定义通常成反比，因此，通常使用 Inverse Simpson Index 和 Gini-Simpson Index。

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: Simpson Index 的数值
    """
    N = sum(data)
    si = sum((float(n) / N) ** 2 for n in data)
    return si


def inverse_simpson_index(data: list):
    """Inverse Simpson Index，即逆辛普森指数，也叫做Simpson's Reciprocal Index。

    ISI指数的值，最小值为1，表示多样性最小，只有一个物种的群落。
    其最大值为样本中的物种数目。如果样本中有5个物种，则最大值为5。

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: Inverse Simpson Index 的数值
    """
    return float(1) / simpson_index(data)


def gini_simpson_index(data: list):
    """考虑了variety/balance，Simpson（1949），即Gini-Simpson Index，
    也称为Simpson Diversity Index，衡量物种多样性的指数。
    指从一个群落中连续两次抽样所得到的个体不属于同一种的概率，该值越大，说明该群落的多样性越高。

    GSI的值域为[0, 1]，值越大，表示多样性越高。

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: Gini-Simpson Index 的数值
    """
    return 1 - simpson_index(data)


def brillouin_diveresity_index(data: list):
    """计算布里渊多样性指数。如，计算作者A的BI指数，传入[30,20,10,10]，
    表示该作者在4个学科领域上的reference次数

    Args:
        data(list): 列表中存放不同（物种）分类的出现次数

    Returns:
        float: brillouin index的值
    """
    sum_ = sum(data)
    a = math.factorial(sum_)
    A = math.log10(a)

    bs = [math.log10(math.factorial(n)) for n in data]
    B = sum(bs)

    H = (A - B) / sum_

    return H


if __name__ == "__main__":
    # 测试BI指数
    #  H = brillouin_diveresity_index([30, 10, 10])
    #  print(H)

    # 测试shannon index
    #  SI = shannon_index([10, 20, 30])
    #  print(SI)

    # 测试simpson index
    # SI = simpson_index([10, 20, 30])
    # inverse_SI = inverse_simpson_index([10, 20, 30])
    # print(SI)
    # print(inverse_SI)
    pass
