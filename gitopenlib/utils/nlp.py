# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-01-15 22:47:56
# @Description :  Powered by 存放NLP常用的一些工具函数

__version__ = "0.4.1"

import random
import re
import string

import emoji
import jieba
import jieba.posseg as psg

from gitopenlib.libs import *
from gitopenlib.utils import nlp as gn


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


def chinese_word_cut(
    text: str,
    custom_dict_file=None,
    stop_words: list = [],
    reserved_flags: list = [],
    remove_punc: bool = True,
) -> list:
    """
    对一段文本进行切分词。

    Args:
        mytext : 文本内容
        custom_dict_file : 自定义词典路径
        stop_words : 停用词列表
        reserved_flags : 切分词后保留哪些词性的词汇

    Returns:
        分词列表
    """
    if custom_dict_file:
        jieba.load_userdict(custom_dict_file)

    jieba.initialize()

    # jieba分词
    word_list = []
    # 切分结果
    seg_list = psg.cut(text)
    for seg_word in seg_list:
        if remove_punc:
            word = gn.remove_punc(seg_word.word)
            if len(word) == 0:
                continue
        else:
            word = seg_word.word
        find = 0
        for stop_word in stop_words:
            if stop_word == word or len(word) < 2:
                find = 1
                break
        if len(reserved_flags) > 1:
            if find == 0 and seg_word.flag in reserved_flags:
                word_list.append(word)
        else:
            if find == 0:
                word_list.append(word)

    return word_list


def english_word_cut(
    text: str,
    stop_words: list = [],
    remove_punc: bool = True,
) -> list:
    """对英文句子分词（按照空格）"""
    if remove_punc:
        text = gn.remove_punc(text)
    return [word for word in text.split() if word not in set(stop_words)]
