#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-01-15 22:47:56
# @Description :  Powered by 存放NLP常用的一些工具函数

__version__ = "0.2.0"

import random
import re
import string

import emoji


def remove_punc(text, repl=""):
    """
    默认去除替换所有半角全角符号，只留字母、数字、中文；

    或者把所有半角全角符号替换为指定的占位符(repl的值)。
    """
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    text = rule.sub(repl, text)
    return text


def is_all_chinese(text: str):
    """
    检验是否全是中文字符（不包含标点）
    """
    text = remove_punc(text)
    for _char in text:
        if not "\u4e00" <= _char <= "\u9fa5":
            return False
    return True


def is_contains_chinese(text: str):
    """检验是否含有中文字符（不包含标点）"""
    text = remove_punc(text)
    for _char in text:
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
