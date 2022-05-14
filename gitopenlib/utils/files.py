#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-10-29 13:38:36
# @Description :  有关文件操作的相关工具函数

__version__ = "0.7.06"

import asyncio
import json
import pickle
import time
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Union

from gitopenlib.utils import basics as gb
from pandas import DataFrame


def save_df(
    df: DataFrame,
    path: str,
    format: str = "xlsx|pkl",
    encoding="utf-8-sig",
    backup: bool = True,
) -> None:
    """把 pandas 的 Dataframe 保存为 xlsx(csv) 和 pkl 。

    Args:
        df: `DataFrame`数据。
        path: 文件路径，给出一个文件路径即可。
        format: 可选格式包括`xlsx|pkl'、`csv|pkl`、`pkl`、`xlsx`、`csv`；
            默认为`xlsx|pkl`。
        encoding: `xlsx(csv)`的编码格式，`utf-8-sig`方便 windows
            系统打开它时不乱码。
        backup: `True`表示文件存在时进行备份(推荐)，`False`表示不备份。
    Returns:
        None.
    """

    path = path.replace(".xlsx", "").replace(".csv", "").replace(".pkl", "")
    path = path + ".{}"

    def to_file(ft):
        file_path = path.format(ft)
        if backup:
            if_path_exist_then_backup(file_path)
        if ft == "xlsx":
            df.to_excel(file_path, encoding=encoding, index=False)
        if ft == "csv":
            df.to_csv(file_path, encoding=encoding, index=False)
        if ft == "pkl":
            save_pkl(df, file_path)

    fts = format.split("|")
    for ft in fts:
        to_file(ft)


def save_pkl(obj, path: str, backup: bool = True):
    """序列化对象并保存到磁盘。

    Args:
        object: 序列化对象
        path: 目标路径
        backup: `True`表示文件存在时进行备份(推荐)，`False`表示不备份。

    Returns:
        bool: 保存成功，返回 True，保存失败，返回 False，抛出异常。
    """
    if backup:
        if_path_exist_then_backup(path)
    file = open(path, mode="wb")
    pickle.dump(obj, file)
    file.close()


def read_pkl(path: str):
    """从磁盘读取序列化对象"""
    return pickle.load(open(path, "rb"))


def if_path_exist_then_backup(pathes: Union[str, List[str]]) -> bool:
    """
    检查路径是否存在，如路径存在，则备份。

    Args:
        pathes: 路径，可以是单个字符串或者字符串的列表。

    Returns:
        bool: 如果有文件被备份了，则为True，否则为False
    """
    if isinstance(pathes, str):
        pathes = [pathes]

    has_backup_files = False
    for path in pathes:
        path = Path(path)
        if path.exists():
            path.rename(
                path.with_suffix(
                    f'.{str(time.strftime("%Y%m%d_%H%M%S",time.localtime()))}{path.suffix}'
                )
            )
            has_backup_files = True
    return has_backup_files


def new_dirs(dir_paths: Union[str, List[str]]) -> List[str]:
    """
    初始化文件夹，检验文件夹的存在状态，并返回准备好的文件夹路径。

    Args:
        dir_paths: 字符串类型的全路径，可以为单个路径，也可以放入列表中，批量创建。

    Returns:
        包含创建的文件夹路径字符串的list
    """
    if isinstance(dir_paths, str):
        dir_paths = [dir_paths]

    for dir in dir_paths:
        dir_path = Path(dir)
        dir_path.mkdir(parents=True, exist_ok=True)

    return dir_paths


def get_paths_from_dir(
    dirs: Union[str, List[str]],
    types: Optional[Union[str, List[str]]] = None,
    recusive: bool = False,
) -> List[str]:
    """
    从指定目录下获取所有指定扩展名文件的路径

    Args:
        dirs: 文件夹路径（绝对路径），单个用str表示，多个用list
        types: 指定文件的扩展名，单个用str表示，多个用list，默认为None，表示所有类型文件
        recusive: 默认为False，不递归子文件夹

    Returns:
        文件路径字符串列表
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
    lines: Union[str, Iterable[str]],
    dir_path: Union[str, Path],
    file_name: str = "file_writer.txt",
    mode: str = "a+",
    separator: str = "\n",
    encoding: str = "utf-8",
    backup: bool = True,
) -> None:
    """向文件中写内容

    Args:
        lines: 可以是单个字符串或者字符串的列表
        dir_path: 文件的绝对路径
        file_name: 文件名称，有默认值
        mode: 写文件的的模式，默认为 a+
        separator: 每一行末尾的分隔符，有默认值
        encoding: 文件的编码格式，默认为utf-8
        backup: 如果文件已经存在，是否对原文件进行备份，默认为True；
            如果为False，当文件已经存在的情况下，会追加到存在的文件中。
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


def read_txt_by_page(
    file_path: str,
    parse_func: Callable[[list], None],
    page_size: int = 100,
    encoding: str = "utf-8",
) -> None:
    """
    从文本文件中分页读取内容

    Args:
        file_path: 文件路径
        parse_func: 每一页数据处理函数，必须定义
        page_size: 每一页数据量
        encoding: 文本文件的编码格式
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


def read_txt_by_page_asyncio(
    file_path: str,
    parse_func: Callable[[list], None],
    page_size: int = 100,
    encoding: str = "utf-8",
    open_async: bool = False,
    slave_num: int = 4,
) -> None:
    """
    从文本文件中分页读取内容，具备异步io处理功能

    Args:
        file_path: 文件路径
        parse_func: 每一页数据处理函数，必须定义
        page_size: 每一页数据量
        encoding: 文本文件的编码格式
        open_async: 是否开启异步io处理数据�������������默认不开启
        slave_num: �������行�������务的���程数目，默认为4
    """

    async def parse_(loop, chunk):
        run_func = lambda: parse_func(chunk)
        await loop.run_in_executor(None, run_func)

    with open(file=file_path, encoding=encoding, mode="r") as file:
        data = list()
        curr_page_id = 0
        start_time = time.time()
        total_time = 0.0
        print("## read_txt_by_page is starting parse the data...")
        for line in file:
            data.append(line.strip())
            if len(data) == page_size:
                if open_async:
                    loop = asyncio.get_event_loop()
                    chunks = gb.chunks(data, slave_num)
                    loop.run_until_complete(
                        asyncio.gather(*[parse_(loop, chunk) for chunk in chunks])
                    )
                    chunks.clear()
                else:
                    parse_func(data)
                # parse_func(data)
                data.clear()
                end_time = time.time()
                cost_time = float(end_time - start_time)
                total_time += cost_time
                start_time = end_time
                print(f"## -{curr_page_id}- page parsed done...{[cost_time]}s")
                curr_page_id += 1

            pass
        if len(data) > 0:
            if open_async:
                loop = asyncio.get_event_loop()
                chunks = gb.chunks(data, slave_num)
                loop.run_until_complete(
                    asyncio.gather(*[parse_(loop, chunk) for chunk in chunks])
                )
                chunks.clear()
            else:
                parse_func(data)
            # parse_func(data)
            end_time = time.time()
            cost_time = float(end_time - start_time)
            total_time += cost_time
            start_time = end_time
            print(f"## -{curr_page_id}- page parsed done...{[cost_time]}s")
            curr_page_id += 1
    print(f"## All done.Total pages: {curr_page_id}.Cost time: {total_time}s")


def read_content(
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> List[str]:
    """
    从文本文件中读取内容，将内容转换为list，list的元素为每行的字符串

    Args:
        file_path : 文件路径
        encoding : 文件的编码方式

    Returns:
        每行字符串组成的list
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    lines = file_path.read_text(encoding=encoding).split("\n")
    result = gb.remove_0_str([line.strip() for line in lines])
    return result


def read_contents(
    file_pathes: List,
    encoding: str = "utf-8",
) -> List[str]:
    """
    从[多个]文本文件中读取内容，将[所有]内容转换为list，list的元素为每行的字符串

    Args:
        file_pathes : 文件路径列表
        encoding : 文件的编码方式

    Returns:
        每行字符串组成的list
    """
    result = []
    for path in file_pathes:
        result.extend(read_content(path, encoding))
    return result


def read_jsons(
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> List[dict]:
    """
    从存放json的文本文件中读取内容，并转化为dict组成的list

    Args:
        file_path: 文件路径
        encoding: 文件的编码方式

    Returns:
        dict组成的list
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    lines = file_path.read_text(encoding=encoding).split("\n")
    result = gb.remove_0_str([line.strip() for line in lines])

    return [json.loads(item) for item in result]
