#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-03-18 10:54:33
# @Description :  一些常用的有关 机器学习、深度学习 的函数

__version__ = "0.1.0"


import math


def softmax(data: list, decimal: int = None):
    """
    归一化指数函数softmax，将一个任意实数的K维向量，压缩到另一个K维向量中，使得每一个元素
    的范围都在(0,1)之间，并且所有元素的和为1。
    """
    z_exp = [math.exp(i) for i in data]
    sum_z_exp = sum(z_exp)

    softmax = [
        round(i / sum_z_exp, decimal) if decimal is not None else (i / sum_z_exp)
        for i in z_exp
    ]
    return softmax


#  if __name__ == "__main__":
#      data = [1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0]
#      print(softmax(data))
#      print(softmax(data, 0))
#      print(softmax(data, 3))
