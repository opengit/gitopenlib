#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 10:28:49
# @Description :  some useful functions of indexes or indicators


__version__ = "0.1.0"


import math

import numpy as np
import pandas as pd


def brillouin_diveresity_index(X):
    """计算布里渊多样性指数。如，计算作者A的BI指数，传入[30,20,10,10]，
    表示该作者在4个学科领域上的reference次数

    Args:
        X(list): 列表中存放不同分类的出现次数

    Returns:
        float: 指数的数值
    """
    sum_ = sum(X)
    a = math.factorial(sum_)
    A = math.log10(a)

    bs = [math.log10(math.factorial(x)) for x in X]
    B = sum(bs)

    h = (A - B) / sum_

    return h


if __name__ == "__main__":
    # 测试BI指数
    #  H = brillouin_diveresity_index([30, 10, 10])
    #  print(H)
    pass
