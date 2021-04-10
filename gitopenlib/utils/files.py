#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-10-29 13:38:36
# @Description :  Powered by GitOPEN

__version__ = "0.2.9"

import json
import time
from pathlib import Path, PosixPath
from types import FunctionType
from typing import Optional

from gitopenlib.utils import basics as gb


def new_dirs(dir_paths: str or list):
    """
    初始化文件夹，检验文件夹的存在状态，并返回准备好的文件夹路径。

    Args:
        dir_paths (str or list): 字符串类型的全路径，可以为单个路径，也可以放入列表中，批量创建。
    """
    if isinstance(dir_paths, str):
        dir_paths = [dir_paths]

    for dir in dir_paths:
        dir_path = Path(dir)
        dir_path.mkdir(parents=True, exist_ok=True)

    return dir_paths


def get_paths_from_dir(
    dirs: str or list, types: Optional[str or list] = None, recusive: bool = False
):
    """
    从指定目录下获取所有指定扩展名文件的路径

    Args:
        dirs (list): 文件夹路径（绝对路径），单个用str表示，多个用list
        types (types): 指定文件的扩展名，单个用str表示，多个用list，默认为None，表示所有类型文件
        recusive (bool): 默认为False，不递归子文件夹

    Returns:
        list: 文件路径字符串列表
    """

    if isinstance(dirs, str):
        dirs = [dirs]
    if types is not None:
        if isinstance(types, str):
            types = [types]
        rule = "**/*." if recusive else "*."
    else:
        rule = "**/*" if recusive else "*"
        types = [""]

    result = []
    for d in dirs:
        path = Path(d).resolve()
        for t in types:
            res = path.glob(rule + t)
            result.extend(list(res))

    return [str(item) for item in result]


def file_writer(
    lines: str or list,
    dir_path: str or Path,
    file_name: str = "file_writer.txt",
    mode: str = "a+",
    separator: str = "\n",
    encoding: str = "utf-8",
    backup: bool = True,
):
    """向文件中写内容

    Args:
        lines (str or list): 可以是单个字符串或者字符串的列表
        dir_path (str or Path): 文件的绝对路径
        file_name (str): 文件名称，有默认值
        mode (str): 写文件的的模式，默认为 a+
        separator (str): 每一行末尾的分隔符，有默认值
        encoding (str): 文件的编码格式，默认为utf-8
        backup (bool): 如果文件已经存在，是否对原文件进行备份，默认为True；
            如果为False，当文件已经存在的情况下，会追加到存在的文件中。

    Returns:
        None: 无返回值
    """
    dir_path: Path = Path(dir_path) if isinstance(dir_path, str) else dir_path

    if not dir_path.exists():
        print(
            "## Warning: The dir path you submit is not exist, "
            + "it will be created automatically."
        )
        dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / file_name

    if backup:
        if file_path.exists():
            file_path.rename(
                file_path.with_suffix(
                    f'.{str(time.strftime("%Y%m%d_%H%M%S",time.localtime()))}{file_path.suffix}'
                )
            )

    if isinstance(lines, str):
        lines = [lines]

    with open(file_path, mode=mode, encoding=encoding) as file:
        for line in lines:
            if separator != "":
                file.write(f"{line}{separator}")
            else:
                file.write(line)

    print("## file_writer done...")
    pass


def read_txt_by_page(
    file_path: str,
    parse_func: FunctionType,
    page_size: int = 100,
    encoding: str = "utf-8",
):
    """
    从文本文件中分页读取内容

    Args:
        file_path (str): 文件路径
        parse_func (FunctionType): 每一页数据处理函数，必须定义
        page_size (int): 每一页数据量
        encoding (str): 文本文件的编码格式

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
        file_path (str or PosixPath): 文件路径
        encoding (str): 文件的编码方式

    Returns:
        list: 每行字符串组成的列表
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    return gb.remove_0_str(
        [line.strip() for line in file_path.read_text(encoding=encoding).split("\n")]
    )


def read_jsons(file_path: str or PosixPath, encoding: str = "utf-8"):
    """
    从存放json的文本文件中读取内容，并转化为dict组成的list

    Args:
        file_path (str): 文件路径
        encoding (str): 文件的编码方式

    Returns:
        list: dict组成的list
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    result = gb.remove_0_str(
        [line.strip() for line in file_path.read_text(encoding=encoding).split("\n")]
    )

    return [json.loads(item) for item in result]
