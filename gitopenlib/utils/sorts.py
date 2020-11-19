#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2020-06-01 12:05:26
# @Description :  10种排序的方法，初步测试结果（仅供参考），quick_sort < insert_sort <
# count_sort < shell_sort < merge_sort < bucket_sort < radix_sort < heap_sort <
# select_sort < bubble_sort


def bubble_sort(arr):
    """冒泡排序

    bubble_sort 耗时：284314 毫秒
    """
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(listt, left, right):
    """快速排序

    当left=0, right=1000时，耗时 2 毫秒
    """
    if left >= right:
        return listt

    # 选择参考点，该调整范围的第1个值
    pivot = listt[left]
    low = left
    high = right

    while left < right:
        # 从右边开始查找大于参考点的值
        while left < right and listt[right] >= pivot:
            right -= 1
        # 这个位置的值先挪到左边
        listt[left] = listt[right]

        # 从左边开始查找小于参考点的值
        while left < right and listt[left] <= pivot:
            left += 1
        # 这个位置的值先挪到右边
        listt[right] = listt[left]

    # 写回改成的值
    listt[left] = pivot

    # 递归，并返回结果
    quick_sort(listt, low, left - 1)  # 递归左边部分
    quick_sort(listt, left + 1, high)  # 递归右边部分
    return listt


def insert_sort(alist):
    """插入排序

    insert_sort 耗时：16 毫秒
    """
    length = len(alist)
    for i in range(1, length):
        for j in range(i, 0, -1):
            if alist[j] < alist[j - 1]:
                alist[j], alist[j - 1] = alist[j - 1], alist[i]
            else:
                break
    return alist


def shell_sort(alist):
    """希尔排序

    shell_sort 耗时：150 毫秒
    """
    n = len(alist)
    gap = n // 2
    while gap >= 1:
        for i in range(gap, n):
            while (i - gap) >= 0:
                if alist[i] < alist[i - gap]:
                    alist[i], alist[i - gap] = alist[i - gap], alist[i]
                    i = i - gap
                else:
                    break
        gap = gap // 2
    return alist


def select_sort(alist):
    """选择排序

    select_sort 耗时：121566 毫秒
    """
    n = len(alist)
    for i in range(n):
        # 设置索引 i为最小值的索引
        min_idx = i
        # 通过比较，不断调整最小值的索引位置
        for j in range(i, n):
            if alist[j] < alist[min_idx]:
                min_idx = j
        # 交换第i个值与最小值
        alist[i], alist[min_idx] = alist[min_idx], alist[i]
    return alist


def heap_sort(heap):
    """堆排序，将根节点取出与最后一位对调，对前面len-1个节点继续进行对调过程

    heap_sort 耗时：520 毫秒
    """

    def max_heap(heap, heapsize, root):
        """
        调整堆的结构，使其父节点的值大于子节点的值
        """
        left = 2 * root + 1
        right = left + 1
        large = root
        if left < heapsize and heap[large] < heap[left]:
            large = left
        if right < heapsize and heap[large] < heap[right]:
            large = right
        # 若large=right或large=left，则说明，出现比父节点大的子节点，这时对调，使子节点变为父节点
        if large != root:
            heap[large], heap[root] = heap[root], heap[large]
            max_heap(heap, heapsize, large)

    def build_max_heap(heap):
        """
        构造一个堆，对堆中数据重新排序
        """
        length = len(heap)
        # 从后往前调整结构
        for i in range((length - 2) // 2, -1, -1):
            max_heap(heap, length, i)

    build_max_heap(heap)
    for i in range(len(heap) - 1, -1, -1):
        heap[0], heap[i] = heap[i], heap[0]
        max_heap(heap, i, 0)
    return heap


def merge_sort(alist):
    """归并排序

    merge_sort 耗时：239 毫秒
    """

    def merge(left, right):
        i = 0
        j = 0
        result = []
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result

    if len(alist) < 2:
        return alist
    # 将列表分成更小的两个列表
    mid = int(len(alist) / 2)
    # 分别对左右两个列表进行处理，分别返回两个排序好的列表
    left = merge_sort(alist[:mid])
    right = merge_sort(alist[mid:])
    # 对排序好的两个列表合并，产生一个新的排序好的列表
    return merge(left, right)


def count_sort(alist):
    """技术排序

    count_sort 耗时：47 毫秒
    """
    # 找到最大最小值
    min_num = min(alist)
    max_num = max(alist)
    # 初始化计数列表
    count_list = [0] * (max_num - min_num + 1)
    # 对列表中的每一个元素计数
    for num in alist:
        count_list[num - min_num] += 1
    alist.clear()
    # 当某个元素的个数不为 0，将该元素填回alist列表
    for cur_num, count in enumerate(count_list):
        while count != 0:
            alist.append(cur_num + min_num)
            count -= 1
    return alist


def bucket_sort(alist):
    """桶排序

    bucket_sort 耗时：290 毫秒
    """
    min_num = min(alist)
    max_num = max(alist)
    # 设置桶的大小
    bucket_size = (max_num - min_num) / len(alist)
    # 创建桶数组
    bucket_list = [[] for i in range(len(alist) + 1)]
    # 向桶数组填数
    for num in alist:
        bucket_list[int((num - min_num) // bucket_size)].append(num)
    alist.clear()
    # 回填，这里桶内部排序直接调用了sorted
    for i in bucket_list:
        for j in sorted(i):
            alist.append(j)
    return alist


def radix_sort(alist):
    """基数排序

    radix_sort 耗时：439 毫秒
    """
    # 记录正在对哪一位进行排序，最低位为个位
    i = 0
    # 最大值的位数
    max_num = max(alist)
    j = len(str(max_num))
    while i < j:
        # 建立桶数组，数字为0-9，所以建10个桶
        bucket_list = [[] for i in range(10)]
        # 按位数的大小分别装进不同的桶里
        for num in alist:
            bucket_list[int(num / (10 ** i) % 10)].append(num)
        # 将原列表清空，将各个桶里的数据依次添加进原列表
        alist.clear()
        for l in bucket_list:
            for b in l:
                alist.append(b)
        # 再进行前一位的排序，依次循环，直到排序的位数大于最大值的位数
        i += 1
    return alist


# def test(arr, func):
# """
# 测试排序函数的时间效率
# """
# start_time = time.time()
# if func.__name__ == "quick_sort":
#   func(arr, 0, 1000)
# else:
#   func(arr)
# end_time = time.time()
# print(
#   "{} 耗时：{} 毫秒".format(func.__name__, int(round((end_time - start_time) * 1000)))
# )
# print("-" * 128)


#  if __name__ == "__main__":
#      # import nump as np
#      # import time
#
#      # arr = list(np.random.randint(1, 100000, (50000)))
#      # test(arr, bubble_sort)
#      # test(arr, bucket_sort)
#      # test(arr, count_sort)
#      # test(arr, heap_sort)
#      # test(arr, insert_sort)
#      # test(arr, merge_sort)
#      # test(arr, quick_sort)
#      # test(arr, radix_sort)
#      # test(arr, select_sort)
#      # test(arr, shell_sort)
#
#      pass
