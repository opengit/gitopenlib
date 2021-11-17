#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-05-22 17:08:35
# @Description :  一些画图的相关工具函数


__version__ = "0.3.2"


import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.offsetbox import AnchoredText
from matplotlib import ticker


def set_legend_outside(ax: Axes):
    """
    把图例放到图片的右下角
    """
    ax.legend_.remove()
    ax.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)


def set_axis_tick(ax: Axes, axis: str = "y", format="%.2f"):
    """
    横轴或者纵轴的刻度标签的格式，例如，%.2f 表示两位小数；
    %.2e 科学计数法
    """
    if axis == "x":
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(format))
    if axis == "y":
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(format))


def legend_text(
    ax: Axes, text: str, loc=2, fontsize: int = 10, fontcolor: str = "black"
):
    """
    在ax上添加一个仅包含文本的legend

    Args:
        ax (Axes): 子图的轴
        text (str): 要显示的文字内容
        loc (int): legend的位置，1表示右上角，2表示左上角，3表示左下角，4表示右下角
        fontsize (int): 字体大小
        fontcolor (str): 字体颜色

    Returns:
        AnchoredText: 返回AnchoredText实例
    """
    at = AnchoredText(
        text, prop=dict(size=fontsize, color=fontcolor), frameon=True, loc=loc
    )
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    return at


def set_font(fname: str = "SimHei", fsize: int = 10):
    """
    设置字体

    Args:
        fname (str): 字体的名称。
        fsize (int): 字体的大小。

    Returns:
        None
    """
    # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"] = [fname]
    # 用来设置字体大小
    plt.rcParams["font.size"] = fsize
    # 用来正常显示负号
    plt.rcParams["axes.unicode_minus"] = False


#  if __name__ == "__main__":
#      at = legend_text(plt.gca(), "Line 2\nLine 2", loc=2)
#      at = legend_text(plt.gca(), "Line 3\nLine 3", loc=3)
#      at = legend_text(plt.gca(), "Line 1\nLine 1", loc=1, fontsize=8, fontcolor="green")
#      at = legend_text(plt.gca(), "Line 4\nLine 4", loc=4, fontsize=55)
#      plt.gcf().show()
#      input("pause")
