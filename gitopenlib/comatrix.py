#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-05-30 22:52:49
# @Description :  基于Liu Huan进行简单的改写，改写为类。感谢Liu Huan（liuhuan@mail.las.ac.cn)


__version__ = "0.1.0"


import numpy as np
import pandas as pd


class CoMatrix:
    def __init__(self, target: list, normal=True):
        self.target = target
        self.normal = normal

    def authors_stat(self, target):
        au_dict = {}  # 单个关键词频次统计
        au_group = {}  # 两两关键词合作
        for authors in target:
            authors = authors.split(",")  # 按照逗号分开每个关键词
            authors_co = authors  # 合关键词同样构建一个样本
            for au in authors:
                # 统计单个关键词出现的频次
                if au not in au_dict:
                    au_dict[au] = 1
                else:
                    au_dict[au] += 1
                # 统计合作的频次
                authors_co = authors_co[1:]  # 去掉当前关键词
                for au_c in authors_co:
                    A, B = au, au_c  # 不能用本来的名字，否则会改变au自身
                    if A > B:
                        A, B = B, A  # 保持两个关键词名字顺序一致
                    co_au = A + "," + B  # 将两个关键词合并起来，依然以逗号隔开
                    if co_au not in au_group:
                        au_group[co_au] = 1
                    else:
                        au_group[co_au] += 1
        return au_group, au_dict

    def generate_matrix(self, au_group, au_dict):
        # 取出所有单个关键词
        au_list = list(au_dict.keys())
        # 新建一个空矩阵
        matrix = pd.DataFrame(np.identity(len(au_list)), columns=au_list, index=au_list)
        for key, value in au_group.items():
            A = key.split(",")[0]
            B = key.split(",")[1]
            Fi = au_dict[A]
            Fj = au_dict[B]
            if self.normal:
                Eij = value * value / (Fi * Fj)
            else:
                Eij = value
            # 按照关键词进行索引，更新矩阵
            matrix.loc[A, B] = Eij
            matrix.loc[B, A] = Eij
        return matrix

    def to_tsv(self, path_csv, path_tsv):
        csv_file = open(path_csv, "r")
        tsv_file = open(path_tsv, "w+")
        for index, line in enumerate(csv_file):
            if index == 0:
                line = "*" + line
            line = line.replace(",", "\t")
            tsv_file.write(line)
        tsv_file.close()
        csv_file.close()

    def run(self):
        au_group, au_dict = self.authors_stat(self.target)
        # print("au_group:", au_group)
        # print("au_dict:", au_dict)
        matrix = self.generate_matrix(au_group, au_dict)
        # print(matrix)
        # 相关系数
        # print(matrix.corr())
        if self.normal:
            file_name = "matrix_normal"
        else:
            file_name = "matrix"
        matrix.to_csv(f"{file_name}.csv", index_label="id")
        print(f"the {file_name}.csv is saved..")
        self.to_tsv(f"{file_name}.csv", f"{file_name}.tsv")
        print(f"the {file_name}.tsv is saved..")


if __name__ == "__main__":
    kws = ["a,b,c", "123,123,456"]
    cm = CoMatrix(target=kws, normal=True)
    cm.run()


