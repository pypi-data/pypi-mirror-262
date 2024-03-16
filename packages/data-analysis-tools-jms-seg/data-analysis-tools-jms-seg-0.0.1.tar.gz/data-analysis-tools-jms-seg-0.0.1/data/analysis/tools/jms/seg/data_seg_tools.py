# coding:utf8
import jieba


def data_seg_tool(data):
    words = []
    if isinstance(data, list):
        for text in data:
            words.append(jieba.lcut(text))
    else:
        words.append(jieba.lcut(data))
    return words
