#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2020/11/18 8:50 下午
# @Author  : octy


def returnSub(l):
    length = len(l)
    for i in range(2 ** length):
        combo = []
        for j in range(length):
            if (i >> j) % 2:
                combo.append(l[j])
        print(combo)


if __name__ == "__main__":
    p_list = [1, 2, 3]
    returnSub(p_list)
