#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-05-22 17:08:35
# @Description :  一些画图的相关工具函数


__version__ = "0.7.3.4"


import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from gitopenlib.utils import files as gf
from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MaxNLocator


def sns_barplot_text(ax: Axes, decimal: float = 2):
    """
    使用seaborn画条形图，给每个bar上添加数值标签。
    如默认字体样式不能满足需求，请copy下面代码自定义。
    """
    for p in ax.patches:
        ax.text(
            p.get_x() + p.get_width() / 2.0,
            p.get_height(),
            str(round(p.get_height(), decimal)),
            # fontsize=8,
            color="black",
            ha="center",
            va="bottom",
            rotation=90,
        )


def heatmap(
    data,
    row_labels,
    col_labels,
    ax=None,
    cbar_kw=None,
    cbarlabel="",
    **kwargs,
):
    """
    Create a heatmap from a numpy array and two lists of labels.

    The link of this helper function:
    `https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html`

    Here is the usage example:
        vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
                  "potato", "wheat", "barley"]
        farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
                   "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]
        harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                            [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                            [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                            [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                            [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                            [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                            [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
        fig, ax = plt.subplots()
        im, cbar = heatmap(harvest, vegetables, farmers, ax=ax,
                           cmap="YlGn", cbarlabel="harvest [t/year]")
        texts = annotate_heatmap(im, valfmt="{x:.1f} t")
        fig.tight_layout()
        plt.show()

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(
    im,
    data=None,
    valfmt="{x:.2f}",
    textcolors=("black", "white"),
    threshold=None,
    **textkw,
):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.0

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def set_spines_line_width(ax: Axes, left, top, right, bottom):
    """设置坐标轴的粗细"""
    ax.spines["left"].set_linewidth(left)
    ax.spines["top"].set_linewidth(top)
    ax.spines["right"].set_linewidth(right)
    ax.spines["bottom"].set_linewidth(bottom)


def set_figsize(plt, width: float or int = 4, height: float or int = 3):
    """设置图片的大小，单位为英寸"""
    plt.rcParams["figure.figsize"] = (width, height)


def save_svg(plt, path: str, dpi: int = 300, backup: bool = True):
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


def set_legend_outside(
    ax: Axes,
    title: str = "",
    loc: int = 3,
    ncol: int = 1,
    alpha: float = 1.0,
):
    """把图例放到图片的右下角；也可以调整一些参数，例如透明度，列数。"""
    ax.legend_.remove()
    legend = ax.legend(
        title=title,
        bbox_to_anchor=(1.05, 0),
        loc=loc,
        ncol=ncol,
        borderaxespad=0,
    )
    legend.get_frame().set_alpha(alpha)


def set_axis_tick(ax: Axes, axis: str = "y", format="%.2f"):
    """
    横轴或者纵轴的����度标签的格式，例如，%.2f 表示两位小数；
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


def set_font(fname: str = "SimSun", fsize: int = 12):
    """
    设置字体；
    若是在windows系统，可以使用SimSun，SimHei，SimKai，SimFang等字体；
    若在linux、macOS系统下，可搜索SimSun.ttf字体安装后使用（必要时候需要重启系统）。

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
