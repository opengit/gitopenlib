#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-03-25 14:35:21
# @Description :  Powered by GitOPEN


__version__ = "0.1.0"


import json
from pathlib import Path
from typing import Callable

from gitopenlib.utils import basics as gb
from gitopenlib.utils import files as gf


def parse_refworks(dir_path: str, parse_func: Callable[[list], None] = None):
    """
    对RefWorks的题录数据进行格式化，保存到json文件中，或者使用parse_func直接处理。

    Args:
        dir_path (str): 存放 txt 文件类型的RefWorks数据目录；
        parse_func (Callable): 处理函数；

    Returns:
        None
    """
    file_paths = gf.get_paths_from_dir(dirs=dir_path, types="txt")
    for path in file_paths:
        path = Path(path)
        file_name = path.name
        save_dir = str(path.parent) + "/"

        data = list()
        item = dict()

        f = open(path, "r")
        for row in f:
            row = str(row).strip()
            if row == "":
                continue

            subs = row.split(" ", 1)
            flag = subs[0].strip()
            if len(flag) == 2:
                if flag in ["A1", "AD", "K1"]:
                    subs[1] = gb.remove_0_str(subs[1].split(";"))
                item[subs[0]] = subs[1]
                if flag == "DS":
                    data.append(json.dumps(item, ensure_ascii=False))
                    item.clear()
        f.close()

        # save data to json format file.
        if parse_func is None:
            save_dir = gf.new_dirs(save_dir + "json/")[0]
            gf.file_writer(lines=data, dir_path=save_dir, file_name=f"{file_name}.json")
        # parse data by custom function.
        else:
            parse_func(data)
