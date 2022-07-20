#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-03-18 10:54:33
# @Description :  一些常用的有关 机器学习、深度学习 的通用函数

__version__ = "0.2.5"


import math
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix as sk_cm


def confusion_matrix(
    y_true,
    y_pred,
    classes=None,
    normalize=False,
    decimals=3,
    figsize=(10, 10),
    fontsize=14,
    textsize=12,
    cmap=plt.cm.Blues,
):
    """
    打印出优化版的混淆矩阵及其可视化。

    Args:
        y_true: 真实标签。
        y_pred: 预测结果标签。
        classes: 类别名（标签名）。
        normalize: 是否标准化。
        decimals: 标准化数值小数位数。
        figsize: 图片大小。
        fontsize: 图片上的字体大小。
        textsize: 热力图中数值的字体大小。
        cmap: 图片的配色方案。
    """
    cm = sk_cm(y_true, y_pred)
    if normalize:
        print("Normalized confusion matrix")
        cm_norm = cm.astype("float32") / cm.sum(axis=1)[:, np.newaxis]
        print(cm_norm)
    else:
        print("Confusion matrix, without normalization")
        print(cm)

    plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.colorbar()

    if not classes:
        classes = list(range(cm.shape[0]))
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0 if classes else 45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        text = (
            "{}\n({})".format(cm[i, j], round(cm_norm[i, j], decimals))
            if normalize
            else cm[i, j]
        )
        plt.text(
            j,
            i,
            text,
            horizontalalignment="center",
            verticalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
            size=textsize,
        )

    plt.title("Confusion matrix", fontsize=fontsize)
    plt.ylabel("True label", fontsize=fontsize)
    plt.xlabel("Predicted label", fontsize=fontsize)

    plt.tight_layout()
    plt.show()


def softmax(data: list, decimal: int = None) -> List[float]:
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
