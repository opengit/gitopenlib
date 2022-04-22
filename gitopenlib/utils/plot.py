#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-05-22 17:08:35
# @Description :  一些画图的相关工具函数


__version__ = "0.7.3"


from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from gitopenlib.utils import files as gf


def save_svg(plt, path: str, dpi: int = 350, backup: bool = True):
    """保存为svg格式的矢量图。

    Parameters
    ----------
    plt : pyplot
        pyplot别名。
    path : str
        图片路径。
    dpi : int
        dpi大小，默认350。
    backup : bool
        默认为True，表示如果path存在，则备份之前的文件。
    """
    if backup:
        gf.if_path_exist_then_backup(path)
    plt.savefig(path, dpi=dpi)


def set_ax_space(plt, w: float = 0.2, h: float = 0.2):
    """设置子图间距

    Parameters
    ----------
    plt : pyplot
        pyplot别名。
    w : float
        横向的间距，值为小数，表示横向间距是子图平均宽度的百分比。
    h : float
        纵向的间距，值为小数，表示纵向间距是子图平均高度的百分比。
    """
    plt.tight_layout()
    plt.subplots_adjust(wspace=w, hspace=h)


def set_tick_integer(ax: Axes, axis: str = "both"):
    """设置横纵轴刻度值为整数

    Parameters
    ----------
    ax : Axes
        轴，可以理解为某个子图存放的位置。

    axis : str
        默认值为'both'，表示横纵轴的刻度都设置为整数；可选值维'x'或'y'。

    """
    if axis == "both":
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    elif axis == "x":
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    elif axis == "y":
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        pass


def set_legend_outside(ax: Axes, loc: int = 3, ncol: int = 1, alpha: float = 1.0):
    """把图例放到图片的右下角；也可以调整一些参数，例如透明度，列数。"""
    ax.legend_.remove()
    legend = ax.legend(bbox_to_anchor=(1.05, 0), loc=loc, ncol=ncol, borderaxespad=0)
    legend.get_frame().set_alpha(alpha)


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


def set_font(fname: str = "SimHei", fsize: int = 12):
    """
    设置字体

    Args:
        fname (str): 字体的名称。
        fsize (int): 字体的大小。

    Returns:
        None
    """
    # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"].insert(0, fname)
    # 用来设置字体大小
    plt.rcParams["font.size"] = fsize
    # 用来正常显示负号
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "cm"
