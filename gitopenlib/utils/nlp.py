# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-01-15 22:47:56
# @Description :  Powered by 存放NLP常用的一些工具函数

__version__ = "0.4.3"

import random
import re
import string
from operator import itemgetter

import emoji
import jieba
import jieba.posseg as psg
from gitopenlib.libs import *
from gitopenlib.utils import nlp as gn
from jieba.analyse import TFIDF


class CutTFIDF(TFIDF):

    """对 jieba 分词的 TFIDF 类进行优化，去除单个字不能返回权重的限制。

    支持返回词汇列表对应的权重值和词性列表。
    """

    def __init__(self, idf_path=None):
        super(CutTFIDF, self).__init__(idf_path)

    def extract_tags(self, sentence, topK=100, min_length=2, allowPOS=[]):
        """切分词，并且返回词汇的 tfidf 权重和词性。

        ----------
        Parameter:
            - topK: 返回多少个top关键词。 `None` 表示所有。
            - min_length: 单词或字符的最小长度。设置为 `1` 表示单个字符。
                            如果词汇的长度小于改值，就会被过滤掉。
            - allowPOS: 允许的词性列表。例如：['ns', 'n', 'vn', 'v','nr'].
                            如果词汇的词性不在列表中，就会被过滤掉。
        """
        allowPOS = frozenset(allowPOS)
        words = self.postokenizer.cut(sentence)

        freq = {}
        flag = {}
        for w_f in words:
            w = w_f.word
            f = w_f.flag
            if len(w) < min_length:
                continue
            if allowPOS:
                if f not in allowPOS:
                    continue
            if w.lower() in self.stop_words:
                continue
            freq[w] = freq.get(w, 0.0) + 1.0
            flag[w] = f

        total = sum(freq.values())
        for k in freq:
            kw = k.word if allowPOS else k
            freq[k] *= self.idf_freq.get(kw, self.median_idf) / total

        tokens = list(freq.keys())[:topK]
        weights = list(freq.values())[:topK]
        flags = itemgetter(*tokens)(flag)
        return tokens, weights, flags


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
    word_length: int = 2,
    top_k: int = 100,
    reserved_flags: list = [],
    remove_punc: bool = True,
) -> list:
    """
    对一段文本进行切分词。

    Args:
        mytext : 文本内容
        custom_dict_file : 自定义词典路径
        stop_words : 停用词列表
        word_length : 词汇的最小长度
        top_k : 保留前多少个关键词
        reserved_flags : 切分词后保留哪些词性的词汇

    Returns:
        分词列表
    """
    if custom_dict_file:
        jieba.load_userdict(custom_dict_file)
    jieba.initialize()

    token_list, weight_list, flag_list = [], [], []
    tokens, weights, flags = CutTFIDF().extract_tags(
        sentence=text, topK=top_k, min_length=word_length, allowPOS=reserved_flags
    )
    for index, token in enumerate(tokens):
        if remove_punc:
            token = gn.remove_punc(token)
            if len(token) == 0:
                continue
        if token in stop_words:
            continue
        if reserved_flags:
            if flags[index] not in reserved_flags:
                continue
        token_list.append(token)
        weight_list.append(weights[index])
        flag_list.append(flags[index])

    return token_list, weight_list, flag_list


def english_word_cut(
    text: str,
    stop_words: list = [],
    remove_punc: bool = True,
) -> list:
    """对英文句子分词（按照空格）"""
    if remove_punc:
        text = gn.remove_punc(text)
    return [word for word in text.split() if word not in set(stop_words)]


"""
if __name__ == "__main__":
    text = "喝现挤牛羊奶有感染布鲁氏菌病的风险"
    result = chinese_word_cut(
        text=text,
        custom_dict_file="/Users/sunjiajia/Works/Projects/PycharmProjects/jiaozhen/output/ML/data/custom_dict_file.txt",
        word_length=1,
        stop_words=[],
        reserved_flags=[],
    )
    print(type(result))
    print("**" * 32)
    for item in list(zip(*result)):
        print(item)

    print("**" * 32)
    res = list(zip(*result))
    res = sorted(res, key=itemgetter(1), reverse=True)
    for item in res:
        print(item)
"""
