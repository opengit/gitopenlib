#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-01-15 22:47:56
# @Description :  Powered by 存放NLP常用的一些工具函数

__version__ = "0.1.0"

import random
import re
import string

import emoji


def is_all_chinese(strs: str):
    """
    检验是否全是中文字符
    """
    for _char in strs:
        if not "\u4e00" <= _char <= "\u9fa5":
            return False
    return True


def is_contains_chinese(strs: str):
    """检验是否含有中文字符"""
    for _char in strs:
        if "\u4e00" <= _char <= "\u9fa5":
            return True
    return False


def generate_random_strs(length: int):
    """生成随机字符串"""
    return "".join(random.sample(string.digits * 5 + string.ascii_letters * 4, length))


def char_is_emoji(character):
    """判断字符是否是emoji"""
    return character in emoji.UNICODE_EMOJI


def text_has_emoji(text):
    """判断文本中是否包含emoji"""
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


def remove_punc(line):
    """去除所有半角全角符号，只留字母、数字、中文"""
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub("", line)
    return line
