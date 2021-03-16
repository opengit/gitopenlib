#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-03-16 16:07:34
# @Description :  使用k-mean++算法进行聚类

__version__ = "0.1.0"

import json
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
from gitopenlib.utils import files as gf
from gitopenlib.utils import wonders
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, silhouette_score


@wonders.timing
def run_kmeans(K_range: list, data: list, tags: list, base_dir: str):
    """
    data 是一个 list 类型，其中的每一个 sublist 都和 labels 中的标签对应

    Args:
        max_K (list): K值试验范围
        data (list): 特征数据集，元素是list类型的特征数据
        tags (list): 每一个特征数据对应的标签
        base_dir (str): 工作目录，在该目录下生成一系列的文件和聚类结果

    """
    BASE_DIR = gf.new_dirs(base_dir)[0]

    Ks = list(range(K_range[0], K_range[1] + 1))
    models = list()
    sil_coeff_list = list()
    bss_list = list()
    chs_list = list()
    sse_list = list()

    for k_ in Ks:
        # # 创建存放结果的文件夹
        print(f"#1# the n_clusters is: {k_}")
        base_k_dir = gf.new_dirs(BASE_DIR + f"clusters/{k_}/")[0]

        # # 进行聚类
        random_state = 10
        kmeans = KMeans(n_clusters=k_, random_state=random_state).fit(X=data)
        models.append(kmeans)

        # # 评价指标，经实验观察，当以下评价指标的线型图中，
        # # 首次出现曲率最大的转折点，就是最优的聚类类别数目
        # 使用Silhouette Coefficient 评价，轮廓系数
        # Silhouette Coefficient是对象与其自身簇（内聚力）相比与其他簇（分离）相似程度的度量。
        # 值从-1到+1，其中高值表示对象与其自己的簇很好地匹配并且与相邻簇不匹配。
        # 如果大多数对象具有高值，则聚类结果是合适的。 如果许多点具有低值或负值，则聚类效果不好，可能具有太多或太少的簇。
        # 最大值的那个位置就是聚类最好的位置
        sil_coeff = silhouette_score(data, kmeans.labels_, metric="euclidean")
        sil_coeff_list.append(sil_coeff)

        # 使用between_ss，组内平方误差和法
        # 是组间平方和与总的距离平方和的商
        # 越小越好
        bss = sum_of_square_scores(
            data, kmeans.labels_, kmeans.cluster_centers_, kmeans.n_clusters
        )
        bss_list.append(bss)

        # 使用 calinski_harabaz_score 方法评价聚类效果的好坏,大概是类间距除以类内距，因此这个值越大越好
        # 越大越好
        chs = calinski_harabasz_score(data, kmeans.labels_)
        chs_list.append(chs)

        # 使用 SSE 均方误差
        # SSE越接近于0，说明模型选择和拟合更好，数据预测也越成功
        sse = kmeans.inertia_
        sse_list.append(sse)

        # 将聚类结果的一些参数写入文件中，方便后续检验和观察
        msg = (
            "#" * 23
            + "\n"
            + "n_clusters: {}\n".format(k_)
            + "cluster_centers_: {}\n".format(kmeans.cluster_centers_)
            + "sil_coeff: "
            + str(sil_coeff)
            + "\n"
            + "between_ss / total_ss: "
            + str(bss)
            + "\n"
            + "chs: "
            + str(chs)
            + "\n"
            + "sse: "
            + str(sse)
            + "\n"
        )
        gf.file_writer(msg, base_k_dir, "run_cluster_result.txt")

    # 分析
    # 评价指标的线型图
    fig: Figure = plt.figure()
    ax: Axes = fig.add_subplot(221)
    ax.plot(
        Ks, sil_coeff_list, marker="o", markersize=4, label="Silhouette Coefficient"
    )
    ax.legend()

    ax: Axes = fig.add_subplot(222)
    ax.plot(Ks, bss_list, marker="o", markersize=4, label="Between SS")
    ax.legend()

    ax: Axes = fig.add_subplot(223)
    ax.plot(Ks, chs_list, marker="o", markersize=4, label="Calinski Harabaz Score")
    ax.legend()

    ax: Axes = fig.add_subplot(224)
    ax.plot(Ks, sse_list, marker="o", markersize=4, label="SSE")

    ax.legend()

    plt.show()

    # 让用户判断哪个K值是合适的
    user_command = input("请输入您选择的K值，若输入N，则直接退出:\n")
    if user_command == "N" or user_command == "n":
        os._exit(0)

    # 捕捉异常
    try:
        k_best = int(user_command)
    except ValueError as e:
        print(e)
        os._exit(1)

    # 得到模型
    km = models[Ks.index(k_best)]
    # 分类 类别
    labels_ = km.labels_
    # 质心，质心分类号 与 质心标签的关系数据
    centers = km.cluster_centers_
    # 求出与每个质心（中心）距离最近的一个 样本点
    center_sample_points = list()
    # 求质心最近样本点所属的聚类类别
    center_sample_labels = list()
    # 求质心最近样本点的tag
    center_sample_tags = list()
    for center in centers:
        dist_list = list()
        for idx, val in enumerate(data):
            dist = np.linalg.norm(center - np.array(val))
            dist_list.append(dist)
        dist_min = min(dist_list)
        dist_min_idx = dist_list.index(dist_min)
        point = data[dist_min_idx]
        center_sample_points.append(list(point))
        label = labels_[dist_min_idx]
        center_sample_labels.append(label)
        tag = tags[dist_min_idx]
        center_sample_tags.append(tag)

    # 如果是二维的数据，那么画出来聚类结果
    # 可视化结果
    # 画出所有样例点，属于同一类的绘制同样的颜色
    if len(data[0]) == 2:
        colors = plt.cm.Spectral(np.linspace(0, 1, k_best))
        for idx, val in enumerate(data):
            plt.plot(
                val[0],
                val[1],
                marker="o",
                color=colors[int(labels_[idx])],
                markeredgecolor="black",
                markersize=6,
            )

        # 画出质点，用特殊图型
        for i in range(k_best):
            plt.plot(
                centers[i][0],
                centers[i][1],
                marker="p",
                markeredgecolor="red",
                markersize=10,
            )

        # 画出质心最近点，用特殊图型，五角星
        for i in range(k_best):
            plt.plot(
                center_sample_points[i][0],
                center_sample_points[i][1],
                marker="*",
                markeredgecolor="red",
                markersize=10,
            )
        plt.show()

    # 将聚类好的数据进行格式化整理
    # 保存模型
    joblib.dump(km, BASE_DIR + "/km_model.pkl")
    # 载入模型
    #  joblib.load(BASE_DIR + "/km_model.pkl")

    # 保存质心、质心最近点，质心最近点类别
    # {"centers":[], "center_sample":[],"label":[]}
    center_dict = {
        "centers": centers.tolist(),
        "center_sample": center_sample_points,
        "label": [int(label) for label in center_sample_labels],
    }
    gf.file_writer(
        json.dumps(center_dict, ensure_ascii=False), BASE_DIR, "center_data.txt"
    )

    # 保存质心、质心最近点，质心最近点类别
    # {"centers":[], "center_sample":[],"label":[]}
    center_sample_tags_dict = {
        "center_sample_tags": center_sample_tags,
        "label": [int(label) for label in center_sample_labels],
    }
    gf.file_writer(
        json.dumps(center_sample_tags_dict, ensure_ascii=False),
        BASE_DIR,
        "center_sample_tags_data.txt",
    )

    # 对于一个聚类类别，将数据格式化为如下格式
    # {"center_tag":xxx,"label":xxxx,"tags":[..., ..., ...]}
    cluster_dict = {"clusters": list()}
    for csp, csl in zip(center_sample_points, center_sample_labels):
        cluster = dict()

        tag_idx = int(data.index(csp))
        center_tag = tags[tag_idx]

        cluster["center_tag"] = dict()
        cluster["center_tag"]["tag"] = center_tag
        cluster["center_tag"]["data"] = csp
        cluster["label"] = int(csl)
        cluster["tags"] = list()
        for index_, label_ in enumerate(labels_):
            if label_ == csl:
                tag_ = tags[index_]
                data_ = list(data[index_])
                cluster["tags"].append({"tag": tag_, "data": data_})

        cluster_dict["clusters"].append(cluster)

    gf.file_writer(
        json.dumps(cluster_dict, ensure_ascii=False), BASE_DIR, "cluster_data.txt"
    )

    # 保存 labels ，方便使用
    labels = [int(it) for it in labels_.tolist()]
    gf.file_writer(labels, BASE_DIR, "labels.txt")

    print("#done ...")

    return labels, center_dict, cluster_dict


def sum_of_square_scores(original_data, predict_labels, cluster_centers, n_clusters):
    """
    定义between_SS / total_SS 的计算方法
    """
    avg = np.mean(original_data, axis=0)
    dist = np.power(original_data - avg, 2)
    total_ss = np.sum(dist)
    within_squares = np.zeros((n_clusters, len(original_data[0])))
    for i in range(0, len(original_data)):
        cluster = predict_labels[i]
        within_squares[cluster] += np.power(
            original_data[i] - cluster_centers[cluster], 2
        )
    within_ss = np.sum(within_squares)
    return (total_ss - within_ss) / total_ss


#  if __name__ == "__main__":
#      import random
#
#      n = 300
#
#      labels = [f"A{i}" for i in range(n)]
#      data = [[random.randint(1, n), random.randint(1, n)] for i in range(n)]
#      print(data)
#      print(labels)
#      run_kmeans([2, 20], data, labels, "/Users/sunjiajia/Downloads/test/cluster/")
