#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   libs.py
@Time    :   2021/07/26 10:54:16
@Author  :   GitOPEN
@Version :   1.0
@Contact :   gitopen@gmail.com
@License :   (C)Copyright 2021-2022
@Desc    :   用于快捷导入常用的包，注意这个文件不要格式化！
"""

__version__ = "0.2.6"


# #######################################################
# ### 注意！！这个文件不能格式化，否则下面的包顺序会乱掉！
# #######################################################


# ## 精简编程时的麻烦，常用的其他包的导入
# 画图的包
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# ## gitopenlib 本身的包的导入
from gitopenlib.helpers import mongo as gm
from gitopenlib.indicators import diversity as gd
from gitopenlib.indicators import statistics as gs
from gitopenlib.utils import basics as gb
from gitopenlib.utils import files as gf
from gitopenlib.utils import others as go
from gitopenlib.utils import plot as gp
from gitopenlib.utils import wonders as gw
from gitopenlib.utils import crawler as gc
from gitopenlib.utils import debuger as gdb

# ## 其他常用的包
import os
import time
import sys
from collections import defaultdict
from tqdm import tqdm
import traceback

# ## 科学计算常用包
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
