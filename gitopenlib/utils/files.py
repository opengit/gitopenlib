#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-10-29 13:38:36
# @Description :  有关文件操作的相关工具函数

__version__ = "1.05.01"

import asyncio
import json
import os
import pickle
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Union

import pandas as pd
from gitopenlib.utils import basics as gb
from gitopenlib.utils import files as gf
from pandas import DataFrame


def df_to_xlsx_pkl(
    df: DataFrame,
    save_path: str,
    index: bool = False,
    index_name: Union[str, Sequence] = None,
    backup: bool = True,
):
    """把 DataFrame 保存为 xlsx 文件和 pkl 文件。"""
    if save_path.endswith(".xlsx"):
        xlsx_path = save_path
        pkl_path = save_path.replace(".xlsx", ".pkl")
    elif save_path.endswith(".pkl"):
        xlsx_path = save_path.replace(".pkl", ".xlsx")
        pkl_path = save_path
    else:
        raise Exception("The save_path must end with `.xlsx` or `.pkl`.")

    parent_dir = Path(xlsx_path).parent
    if not parent_dir.exists():
        gf.new_dirs(str(parent_dir))

    if backup:
        gf.if_path_exist_then_backup(xlsx_path)
        gf.if_path_exist_then_backup(pkl_path)

    if index:
        df.to_excel(xlsx_path, index=True, index_label=index_name)
    else:
        df.to_excel(xlsx_path, index=False)
    df.to_pickle(pkl_path)


def df_to_json(
    df: DataFrame,
    path: str,
    encoding="utf-8",
    force_ascii=False,
):
    """把 DataFrame 保存为 json 文件。

    Args:
        df:
            DataFrame数据。
        path:
            保存路径。
        orient:
            保存格式，参考 `pandas.DataFrame.to_json` 的参数说明。
    """
    if_path_exist_then_backup(path)
    with open(path, "w+", encoding=encoding) as f:
        df.to_json(f, force_ascii=force_ascii)


def df_from_json(
    path: str,
    encoding="utf-8",
) -> DataFrame:
    """将json数据读取为 `pandas.DataFrame` 。"""
    return pd.read_json(path, encoding=encoding)


def save_df(
    df: DataFrame,
    path: str,
    format: str = "xlsx|json",
    encoding="utf-8-sig",
    backup: bool = True,
) -> None:
    """把 pandas 的 Dataframe 保存为 xlsx(csv) 、json 文件。

    注：该方法使用pickle在3.7和3.8两个版本中存在兼容问题，请注意这一点。

    Args:
        df:
            `DataFrame`数据。
        path:
            文件路径，给出一个文件路径即可。
        format:
            可选格式包括`xlsx|json`、`csv|json`、`json`、`xlsx`、`csv`；默认为`xlsx|json`。
        encoding:
            `xlsx(csv)`的编码格式，`utf-8-sig`方便windows系统打开它时不乱码；`json`的编码格式为`utf-8`。
        backup:
            `True`表示文件存在时进行备份(推荐)，`False`表示不备份。
    """

    path = path.replace(".xlsx", "").replace(".csv", "").replace(".json", "")
    path = path + ".{}"

    def to_file(ft):
        file_path = path.format(ft)
        if backup:
            if_path_exist_then_backup(file_path)
        if ft == "xlsx":
            df.to_excel(file_path, encoding=encoding)
        if ft == "csv":
            df.to_csv(file_path, encoding=encoding)
        if ft == "json":
            df_to_json(df, file_path)

    fts = format.split("|")
    for ft in fts:
        to_file(ft)


def save_pkl(obj, path: str, backup: bool = True):
    """序列化对象并保存到磁盘。

    Args:
        object:
            序列化对象。
        path:
            目标路径。
        backup:
            `True`表示文件存在时进行备份(推荐)，`False`表示不备份。

    Returns:
        bool: 保存成功，返回 True，保存失败，返回 False，抛出异常。
    """
    if backup:
        if_path_exist_then_backup(path)
    file = open(path, mode="wb")
    pickle.dump(obj, file)
    file.close()


def read_pkl(path: str):
    """从磁盘读取序列化对象。"""
    return pickle.load(open(path, "rb"))


def check_path(pathes: Union[str, List[str]]):
    """检查路径是否存在，不存在则创建。创建时会自动创建父目录。"""
    if isinstance(pathes, str):
        pathes = [pathes]
    for path in pathes:
        path = Path(path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)


def if_path_exist_then_backup(pathes: Union[str, List[str]]) -> bool:
    """检查路径是否存在，如路径存在，则备份。

    Args:
        pathes:
            路径，可以是单个字符串或者字符串的列表。

    Returns:
        bool: 如果有文件被备份了，则为True，否则为False。
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
    """初始化文件夹，检验文件夹的存在状态，并返回准备好的文件夹路径。

    如果`dir_paths`为`str`类型，则返回值为单个路径；
    如果为`list`类型，则返回值为列表。

    Args:
        dir_paths:
            字符串类型的全路径，可以为单个路径，也可以放入列表中，批量创建。

    Returns:
        参见函数说明。
    """
    if isinstance(dir_paths, str):
        dir_paths = [dir_paths]

    for dir in dir_paths:
        dir_path = Path(dir)
        dir_path.mkdir(parents=True, exist_ok=True)
    if isinstance(dir_paths, list) and len(dir_paths) == 1:
        dir_paths = dir_paths[0]
    return dir_paths


def get_paths_from_dir(
    dirs: Union[str, List[str]],
    types: Optional[Union[str, List[str]]] = None,
    recusive: bool = False,
) -> List[str]:
    """从指定目录下获取所有指定扩展名文件的路径。

    Args:
        dirs:
            文件夹路径（绝对路径），单个用str表示，多个用list。
        types:
            指定文件的扩展名，单个用str表示，多个用list，默认为None，表示所有类型文件。
        recusive:
            默认为False，不递归子文件夹。

    Returns:
        List[str]:
            文件路径字符串列表。
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
    dir_path: Union[str, Path] = None,
    file_name: str = None,
    file_path: str = None,
    separator: str = "\n",
    encoding: str = "utf-8",
    backup: bool = None,
) -> None:
    """向文件中写内容。

    Parameters
    ----------
    lines: Union[str, Iterable[str]]
        可以是单个字符串或者字符串的列表。
    dir_path: Union[str, Path]
        文件目录的绝对路径。
    file_name: str
        文件名称，有默认值。
    file_path: str
        文件绝对路径，包括目录和文件名。
            默认为None，由dir_path，file_name指定；如果不为None，则以这个为准。
    separator: str
        每一行末尾的分隔符，有默认值。
    encoding: str
        文件的编码格式，默认为utf-8。
    backup: bool
        如果为True，先备份，再写入文件；
            如果为False，不备份，覆盖存在的文件。
                如果为None，若文件存在，则不执行写入；若文件不存在，则会创建并写入文件。
    """
    if file_path is not None:
        tmp = file_path.split(os.path.sep)
        dir_path = os.path.sep.join(tmp[:-1])
        file_name = tmp[-1]

    dir_path: Path = Path(dir_path) if isinstance(dir_path, str) else dir_path

    if not dir_path.exists():
        print(
            "## Warning: The dir path you submit is not exist, "
            + "it will be created automatically."
        )
        dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / file_name

    if backup is None:
        if file_path.exists():
            print(
                "# Warning: The file you submit is already exist. So nothing will be done."
            )
            return

    if backup:
        if file_path.exists():
            file_path.rename(
                file_path.with_suffix(
                    f'.{str(time.strftime("%Y%m%d_%H%M%S",time.localtime()))}{file_path.suffix}'
                )
            )

    if isinstance(lines, str):
        lines = [lines]

    mode = "w+"
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
    """从文本文件中分页读取内容。

    Args:
        file_path:
            文件路径。
        parse_func:
            每一页数据处理函数，必须定义。
        page_size:
            每一页数据量。
        encoding:
            文本文件的编码格式。
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
    """从文本文件中分页读取内容，具备异步io处理功能。

    Args:
        file_path:
            文件路径。
        parse_func:
            每一页数据处理函数，必须定义。
        page_size:
            每一页数据量。
        encoding:
            文本文件的编码格式。
        open_async:
            是否开启异步io处理数据，默认不开启。
        slave_num:
            执行任务的协程数目，默认为4。
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
                data.clear()
                end_time = time.time()
                cost_time = float(end_time - start_time)
                total_time += cost_time
                start_time = end_time
                print(f"## -{curr_page_id}- page parsed done...{[cost_time]}s")
                curr_page_id += 1

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
    """从文本文件中读取内容，将内容转换为list，list的元素为每行的字符串。

    Args:
        file_path:
            文件路径。
        encoding:
            文件的编码方式。

    Returns:
        List[str]:
            每行字符串组成的list。
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    lines = file_path.read_text(encoding=encoding).split("\n")
    result = gb.remove_0_str([line.strip() for line in lines])
    return result


def read_content1(
    file_path: str,
    encoding: str = "utf-8",
) -> List[str]:
    """从文本文件中读取内容，将内容转换为list，list的元素为每行的字符串。

    当且仅当`read_content`函数报错时，例如`0xfa`错误时，再使用这个函数。\n
    原因是这个函数比`read_content`函数更加稳定，但是更慢。

    Parameters
    ----------
    file_path : str
        文件路径。
    encoding : str
        文件的编码方式。

    Returns
    -------
    List[str] :
        每行字符串组成的list。
    """
    lines = []
    with open(file_path, "rb") as file:
        for line in file:
            line = line.decode(encoding, "ignore").strip()
            lines.append(line)
    return lines


def read_contents(
    file_pathes: List,
    encoding: str = "utf-8",
) -> List[str]:
    """从[多个]文本文件中读取内容，将[所有]内容转换为list，list的元素为每行的字符串。

    Args:
        file_pathes:
            文件路径列表。
        encoding:
            文件的编码方式。

    Returns:
        List[str]:
            每行字符串组成的list。
    """
    result = []
    for path in file_pathes:
        result.extend(read_content(path, encoding))
    return result


def read_jsons(
    file_path: Union[str, Path, List],
    encoding: str = "utf-8",
) -> List[Dict]:
    """从存放json的文本文件中读取内容，并转化为dict组成的list。

    Parameters
    ----------
    file_path : str, Path or List
        文件路径,可以是str或者Path,也可以是list,每个元素为str或者Path.
    encoding : str
        文件的编码方式。

    Returns
    -------
    List[Dict]:
        dict组成的list
    """

    def get_lines(path):
        if isinstance(path, str):
            path = Path(path)
        lines = []
        with open(path, "r", encoding=encoding) as file:
            for line in file:
                line = line.strip()
                if line:
                    lines.append(json.loads(line))
        return lines

    if not isinstance(file_path, List):
        file_path = [file_path]

    result = []
    for path in file_path:
        result.extend(get_lines(path))

    return result


def read_jsons1(
    file_path: Union[str, Path, List],
    encoding: str = "utf-8",
) -> List[Dict]:
    """从存放json的文本文件中读取内容，并转化为dict组成的list。

    Parameters
    ----------
    file_path : str, Path or List
        文件路径,可以是str或者Path,也可以是list,每个元素为str或者Path.
    encoding : str
        文件的编码方式。

    Returns
    -------
    List[Dict]:
        dict组成的list
    """

    def get_lines(path):
        lines = []
        with open(path, "rb") as file:
            for line in file:
                line = line.decode(encoding, "ignore").strip()
                if line:
                    lines.append(json.loads(line))
        return lines

    if not isinstance(file_path, List):
        file_path = [file_path]

    result = []
    for path in file_path:
        result.extend(get_lines(path))

    return result
