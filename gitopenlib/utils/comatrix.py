#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:52:49
# @Description :  求解共现矩阵


__version__ = "0.2.1"

import csv
import math
from collections import defaultdict
from itertools import product

from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

from gitopenlib.utils import basics as gb
from gitopenlib.utils import files as gf
from gitopenlib.utils import wonders


@wonders.timing
def generate_CoMatrix(
    dir_path: str,
    data: list,
    filter_num: int = 1,
    filter_tags: list = None,
    save: bool = False,
):
    """
    生成共现矩阵。

    Args:
        dir_path (str): 工作目录，生成文件的位置
        data (list): tags的列表，格式为 [["abc","bcd","cde"],["abc","cde","def"]]
        filter_num (int): 计算时只包含出现次数大于等于这个数值的tag
        filter_tags (list): 默认为None，只计算列表中包含的tag的共现矩阵；["abc", "cde"]表示只计算"abc","cde"的矩阵
        save (True): 默认为 False，不把向量保存到文件

    Returns:
        (tuple): (tags, frequency_vector, ochiia_correlation_vector, cosine_similarity_vector, cosine_distances_vector)，分别表示：标签list，共现矩阵，相关矩阵，余弦相似度矩阵，余弦距离矩阵

    """

    def save_matrix(path: str, labels: list, data: list):
        """
        保存到 csv
        """
        with open(path, "a+") as f:
            #  tsv_writer = csv.writer(f, delimiter="\t")
            tsv_writer = csv.writer(f)
            tsv_writer.writerow(["index"] + labels)
            for idx, item in enumerate(data):
                row_ = list()
                row_.append(labels[idx])
                row_.extend(item)
                tsv_writer.writerow(row_)

    # 工作目录
    BASE_DIR = gf.new_dirs(dir_path)[0]

    # kw 出现的次数统计
    kw_num_dict = defaultdict(int)
    for item in data:
        for kw in item:
            kw_num_dict[kw] += 1
    #  print(kw_num_dict)

    # 依据频次对关键词进行过滤
    kw_num_filter_dict = defaultdict(int)
    for kw, num in kw_num_dict.items():
        if num >= filter_num:
            kw_num_filter_dict[kw] = num

    kw_num_dict = kw_num_filter_dict

    # 关键词列表
    kws = list(kw_num_dict.keys())

    # 如果同时指定了 filter_num 和 filter_kws ，
    # 那么需要对两种情况下的关键词列表取交集
    if filter_tags:
        kws = list(set(kws).intersection(set(filter_tags)))
    kws = sorted(kws)

    # 两两组合出现的次数
    pair_count_dict = defaultdict(int)
    for item in data:
        pairs = list(product(item, item))
        for pair in pairs:
            if pair[0] in set(kws) and pair[1] in set(kws):
                pair_count_dict[pair] += 1

    # 若 pair 中的两个词汇一样，那么共现次数设置为0
    pair_count_dict = dict(
        [
            (pair, 0 if pair[0] == pair[1] else count)
            for pair, count in pair_count_dict.items()
        ]
    )

    # 转换为数据结构，因为每个词汇可能和多个词汇组成pair
    # 转换为以 {'kw1':{'kw2':2,'kw3':4}}的结构，
    # 表示 kw1 和 kw2 共现 2 次，和 kw3 共现4 次。
    kw_kw_dict = defaultdict(dict)
    for pair, count in pair_count_dict.items():
        kw_kw_dict[pair[0]][pair[1]] = count

    # 补全，有的kw之间共现为0，补全一下
    for kw, kw_count in kw_kw_dict.items():
        already_kws = set(kw_count.keys())
        diffs = set(kws).difference(already_kws)
        for diff in diffs:
            kw_kw_dict[kw][diff] = 0

    # 对 kw_kw_dict 排序，以及对kw的kw_dict排序
    kw_kw_dict = gb.dict_sorted(kw_kw_dict, 0)
    kw_kw_dict = dict(
        [(kw, gb.dict_sorted(kw_count, 0)) for kw, kw_count in kw_kw_dict.items()]
    )

    # 转为向量的格式
    kw_vector_dict = dict()
    for kw, kw_count in kw_kw_dict.items():
        kw_vector_dict[kw] = list(kw_count.values())

    # 共现频次 矩阵
    frequency_vector = list()

    # Ochiia系数将共词矩阵转换为相关矩阵
    # ochiia = kw1_kw2共现次数 / ( kw2频次平方根*kw2频次平方根 )
    correlation_matrix_dict = defaultdict(dict)
    for kw, kw_count in kw_kw_dict.items():
        frequency_vector.append(list(kw_count.values()))
        for kw_sub, count in kw_count.items():
            ochiia = count / (
                math.sqrt(kw_num_dict[kw]) * math.sqrt(kw_num_dict[kw_sub])
            )
            correlation_matrix_dict[kw][kw_sub] = ochiia

    # 相关矩阵
    ochiia_correlation_vector = [
        list(val.values()) for kw, val in correlation_matrix_dict.items()
    ]

    # 计算余弦相似度
    cosine_similarity_vector = cosine_similarity(frequency_vector)

    # 计算余弦距离
    cosine_distances_vector = cosine_distances(frequency_vector)

    # 保存为 csv 矩阵格式
    if save:
        for vector, name in zip(
            [
                frequency_vector,
                ochiia_correlation_vector,
                cosine_similarity_vector,
                cosine_distances_vector,
            ],
            [
                "frequency_vector",
                "ochiia_correlation_vector",
                "cosine_similarity_vector",
                "cosine_distances_vector",
            ],
        ):
            save_matrix(
                "{}/{}.csv".format(BASE_DIR, name).replace("_vector", "_matrix"),
                kws,
                vector,
            )

    print("...done...")

    return (
        kws,
        frequency_vector,
        ochiia_correlation_vector,
        cosine_similarity_vector,
        cosine_distances_vector,
    )


#  if __name__ == "__main__":
#      data = [["abc", "bcd", "cde"], ["abc", "cde", "def"]]
#      generate_CoMatrix(dir_path="./", data=data, filter_num=1, filter_tags=None)
#      pass
