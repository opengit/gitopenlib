#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-10-29 13:38:36
# @Description :  Powered by GitOPEN

__version__ = "0.1.1"

import json
import time
from pathlib import Path, PosixPath
from types import FunctionType

from gitopenlib.utils.basics import remove_0_str


def read_txt_by_page(
    file_path: str,
    parse_func: FunctionType,
    page_size: int = 100,
    encoding: str = "utf-8",
):
    """
    从文本文件中分页读取内容

    Args:
        file_path(str): 文件路径
        parse_func(FunctionType): 每一页数据处理函数，必须定义
        page_size(int): 每一页数据量
        encoding(str): 文本文件的编码格式

    Returns:
        None: 在parse_func已经处理好数据，不用返回值
    """
    with open(file=file_path, encoding=encoding, mode="r") as file:
        data = list()
        curr_page_id = 0
        start_time = time.time()
        total_time = 0.0
        print("## read_txt_by_page is starting parse the data...")
        for line in file:
            data.append(line.strip())
            if len(data) == page_size:
                parse_func(data)
                data.clear()
                end_time = time.time()
                cost_time = float(end_time - start_time)
                total_time += cost_time
                start_time = end_time
                print(f"## -{curr_page_id}- page parsed done...{[cost_time]}s")
                curr_page_id += 1

            pass
        if len(data) > 0:
            parse_func(data)
            end_time = time.time()
            cost_time = float(end_time - start_time)
            total_time += cost_time
            start_time = end_time
            print(f"## -{curr_page_id}- page parsed done...{[cost_time]}s")
            curr_page_id += 1
    print(f"## All done. Total pages: {curr_page_id}. Elapsed time: {total_time}s")


def read_content(file_path: str or PosixPath, encoding: str = "utf-8"):
    """
    从文本文件中读取内容，将内容转换为list，list的元素为每行的字符串

    Args:
        file_path(str or PosixPath): 文件路径

    return:
        list: 每行字符串组成的列表
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    return remove_0_str(
        [line.strip() for line in file_path.read_text(encoding=encoding).split("\n")]
    )


def read_jsons(file_path: str or PosixPath, encoding: str = "utf-8"):
    """
    从文本文件中读取内容，并转化为dict组成的list
    Args:
        file_path: 文件路径

    Returns:
        list: dict组成的list
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    result = remove_0_str(
        [line.strip() for line in file_path.read_text(encoding=encoding).split("\n")]
    )

    return [json.loads(item) for item in result]


#  if __name__ == "__main__":
#
#      def parse(data):
#          time.sleep(0.5)
#
#      file_path = "/Users/sunjiajia/Works/Projects/PycharmProjects/interdisciplinary2/output/results/test_cits_10000.txt"
#      read_txt_by_page(file_path=file_path, parse_func=parse, page_size=1000)
