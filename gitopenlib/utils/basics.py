#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:51:45
# @Description : 包含基本的文件读写，指定扩展名文件查找等基本工具


__version__ = "0.22.1"


import json
import math
import random
import sys
import time
from typing import Any, Dict, Iterable, List, Union

from gitopenlib.utils import basics as gb


def quit() -> None:
    """用于临时打断程序，方便调试"""
    sys.exit(0)


def pt(msg: str, start: str = "# ", end: str = "\n", length: int = 80):
    """print改写，大于 length 的 msg 拆开换行打印"""
    msg = start + msg
    len_ = len(msg)
    m = int(len_ / length)
    r = len_ % length
    for i in range(m):
        head_idx = length * i
        foot_idx = head_idx + length
        ln = msg[head_idx:foot_idx]
        if i == 0:
            print(ln)
        else:
            print(start + "\t" + ln)

    if r:
        print(start + "\t" + msg[-r:])


def dict2object(adict: dict) -> object:
    """把dict转为类对象，实现属性的快速访问"""

    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    return Struct(**adict)


def get_keys_from_dict(adict: Dict[Any, Any]) -> List[Any]:
    """获取dict中的所有key，包括嵌套dict中的key"""
    keys = set()

    def get_keys(bdict: dict, keys: set):
        keys_ = list(bdict.keys())
        keys.update(keys_)
        values_ = list(bdict.values())
        for val in values_:
            if isinstance(val, dict):
                get_keys(val, keys)

    get_keys(adict, keys)
    keys = list(keys)
    keys.sort()
    return keys


def is_subset(a: Iterable, b: Iterable) -> bool:
    """判断a是否是b的子集，顺序不敏感"""
    return set(a).issubset(set(b))


def is_sublist(a: List, b: List) -> bool:
    """判断a是否是b的子集，顺序敏感"""
    b = iter(b)
    return all(i in b for i in a)


def list_item_getter(data: list, index: list):
    """按照index索引列表从data中拿出相应元素组成新的list"""
    return [data[idx] for idx in index]


def fmt_seconds(seconds: int or float, lang: str = "zh"):
    """把秒转换为年月日小时分钟秒。"""
    if lang == "zh":
        return time.strftime("%Y年%m月%d日 %H小时%M分钟%S秒", time.gmtime(seconds))
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(seconds))


def list_intersection(listA: list, listB: list):
    """
    求两个list的交集，listA中的哪些元素，在listB中出现了。
    注意，listA和listB的顺序不一样，交集结果不一样。
    """
    return [it for it in listA if it in listB]


def dict_extremum(data: dict, type=0) -> tuple:
    """
    找到dict中value的极值，并返回key，若极值有多个，则返回多个key

    Args:
        data: dict数据，且value必须为数值类型
        type: 1表示执行最大值操作，0表示最小值操作

    Returns:
        极值，键的列表
    """
    values = list(data.values())
    if type == 1:
        # 极大值
        ex = max(values)
    elif type == 0:
        # 极小值
        ex = min(values)
    else:
        raise Exception("The value of 'type' should only be 0 or 1.")

    # 拿到所有的key
    keys_ = [k for k, v in data.items() if v == ex]

    return ex, keys_


def list_extremum(data: list, type=0) -> tuple:
    """
    找到list中的极值，并返回索引，若极值有多个，则返回多个索引

    Args:
        data: list数据
        type: 1表示执行最大值操作，0表示最小值操作

    Returns:
        极值，索引的列表
    """
    if type == 1:
        # 极大值
        ex = max(data)
    elif type == 0:
        # 极小值
        ex = min(data)
    else:
        raise Exception("The value of 'type' should only be 0 or 1.")
    # 拿到所有索引
    idx = [id for id, item in enumerate(data) if item == ex]

    return ex, idx


def split_strip(
    strings: Union[str, List[str]],
    sep: str,
    maxsplit: int = -1,
) -> List[str]:
    """
    拆分字符串，并对列表中的元素进行 strip、去除空字符串。
    """
    if isinstance(strings, str):
        return gb.remove_0_str([it.strip() for it in strings.split(sep, maxsplit)])
    elif isinstance(strings, list):
        result = []
        for item in strings:
            item = str(item).strip()
            result.append(
                gb.remove_0_str([it.strip() for it in item.split(sep, maxsplit)])
            )
        return result


def printj(
    msg: dict,
    sort_keys: bool = False,
    beautify: bool = True,
    ensure_ascii: bool = False,
) -> None:
    """
    把dict类型的数据，格式化为json字符串输出显示。
    """
    print(
        json.dumps(msg, sort_keys=sort_keys, indent=4, ensure_ascii=ensure_ascii)
        if beautify
        else json.dumps(msg, ensure_ascii=ensure_ascii)
    )


def random_color(n: int = 1) -> Union[str, List]:
    """
    随机生成颜色代码

    Args:
        n: 生成颜色代码的数目。

    Returns:
        n为1时返回一个颜色代码字符串，n不为1时返回颜色代码列表。
    """
    if n <= 0:
        raise Exception(
            "Invalid param 'n' you provided, which sholud be equal or greater than 1."
        )
    colorArr = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
    ]
    colors = list()
    for i in range(n):
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        colors.append("#" + color)

    return colors if n > 1 else colors[0]


def filter_by_thresholds(
    data: list, thresholds: list, threshold_closed: str = None
) -> List:
    """依据阈值范围对数据进行过滤

    依据 threshold 中的规则对 data 数据进行过滤，threshold_closed
    规定区间规则的闭合状态，rl/lr 表示区间两端闭合，r表示右闭合，l表示左闭合

    Args:
        data: list类型的数据；
        thresholds: list类型的参数，元素为tuple类型；
        threshold_closed: str类型的参数，rl/lr
            表示区间两端闭合，r 表示右闭合，l 表示左闭合，None 表示两端开区间。

    Returns:
        按照区间保留下来的数据。
    """
    for th in thresholds:
        for index, value in enumerate(data):
            if threshold_closed == "rl" or threshold_closed == "lr":
                # 闭合区间，保留区间内的所有值，排除区间外的值
                if value < th[0] or value > th[1]:
                    data[index] = ""
            if threshold_closed == "r":
                # 左开右闭
                if value <= th[0] or value > th[1]:
                    data[index] = ""
            if threshold_closed == "l":
                # 左闭右开
                if value < th[0] or value >= th[1]:
                    data[index] = ""
            if threshold_closed is None:
                # 两端开区间
                if value <= th[0] or value >= th[1]:
                    data[index] = ""
        data = remove_0_str(data)

    return data


def ele2dict(data: list) -> List[dict]:
    """把元素为json字符串的list数据，转为，元素为dict类型的list数据

    Args:
        data: list类型的数据，元素为json字符串类型

    Returns:
        转换后的list数据
    """
    return [json2dict(item) for item in data]


def ele2json(data: list) -> List[str]:
    """把元素为dict类型的list数据，转为，元素为json字符串的list数据

    Args:
        data: list类型的数据，元素为dict类型

    Returns:
        转换后的list数据
    """
    return [dict2json(item) for item in data]


def dict2json(data: dict) -> str:
    """将dict转为json字符串

    Args:
        data: dict类型的数据

    Returns:
        返回json字符串
    """
    return json.dumps(data, ensure_ascii=False, separators=[",", ":"])


def json2dict(astr: str) -> dict:
    """将json字符串转���dict类���的数据对象

    Args:
        astr: json字符串转为dict类型的数据对象

    Returns:
        返回dict类型数据对象
    """
    return json.loads(astr)


def dict_sorted(data: dict, flag: int = 0, ascending: bool = True) -> dict:
    """
    对dict排序

    Args:
        data: 目标数据dict类型
        flag: 默认为0，表示按照字典的key进行排序；1表示按照value进行排序
        ascending: 默认为True，表示按照升序排序；False表示降序排序

    Returns:
        排序后的数据
    """
    return dict(sorted(data.items(), key=lambda x: x[flag], reverse=not ascending))


def list_deduplicate(data: list) -> List:
    """列表项为dict类型的去重

    Args:
        data: 目标数据，list类型

    Returns:
        去重后的数据
    """
    return [dict(t) for t in set([tuple(d.items()) for d in data])]


def sort_list(
    data: list,
    ascending: bool = True,
    flag: int = 0,
    position: int = 0,
    key: str = "",
) -> List:
    """
    对 list 进行排序

    Args:
        data: list 类型数据，item 为 dict 或者 basic type
        ascending: 默认为 True，表示升序；False 表示降序
        flag: 0 表示元素为基本类型，1 表示元素为 dict，2 表示元素为 tuple
        position: 如果元素为 basic type，position 保持默认即可；
            如果元素为 tuple，position 的数值表示以哪个 index 位置的值排序
        key: 如果元素为 dict，key 表示按照哪个 key 的 value 进行排序

    Returns:
        排序后的数据
    """
    if flag == 0:
        # basic type
        data.sort(reverse=not ascending)
    elif flag == 1:
        # dict type
        if key == "":
            key, _ = data[0].items()[0]
        data.sort(key=lambda x: x.get(key, 0), reverse=not ascending)
    elif flag == 2:
        # tuple type
        if position < 0 or position >= len(data[0]):
            position = 0
        data.sort(key=lambda x: x[position], reverse=not ascending)

    return data


def strips(string: str) -> str:
    """
    去除字符串两端的空格符和换行符，并且去除中间的换行符
    """
    return string.strip().replace("\n", "").replace("\r", "").replace("\r\n", "")


def remove_0_str(data: list) -> List:
    """
    去除list列表中为长度为0的字符串，用于字符串split后，列表中出现长度为0字符串的去除
    """
    return [item for item in data if len(str(item)) != 0]


def chunks(arr, m) -> List[list]:
    """分割列表，但是子list元素个数尽可能平均

    Args:
        arr: 待分割的list
        m: 分成几份

    Returns:
        分割后的每个子list都是返回结果list的一个元素
    """
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i : i + n] for i in range(0, len(arr), n)]


def time_formatter(seconds: int, show: bool = True):
    """将以秒为单位的时间转化为相应的分钟、小时、天。

    Args:
        seconds: 秒数
        show: 是否打印显示信息，默认为True，那么没有返回值，设置为False，不打印信息，但返回值
    Returns:
        若show为False，则有返回值，tuple中值的为天，小时，分钟，秒
    """
    d = int(seconds // 86400)
    h = int(seconds // 3600 % 24)
    m = int((seconds % 3600) // 60)
    s = round(seconds % 60, 3)

    msg = ""
    if d > 0:
        msg += f"{d} days, "
    if h > 0:
        msg += f"{h} hours, "
    if m > 0:
        msg += f"{m} minutes, "
    if s > 0:
        msg += f"{s} seconds."

    if show:
        print(msg)
    else:
        return msg
