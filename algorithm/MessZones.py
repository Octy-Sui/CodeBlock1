#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/20 7:08 下午
# @Author  : octy


def returnLastWord(s):
    print("The result of " + s)
    s = s.strip()
    length = len(s)
    if length == 0:
        print(0)
        return 0
    word_count = 0
    for i in range(length-1, 0, -1):
        if s[i] != " ":
            continue
        else:
            word_count = length - 1 - i
            break
    print(word_count)
    return word_count


def test_returnLastWord():
    returnLastWord("hi, hello  world")
    returnLastWord("hello world")
    returnLastWord("hello world ")
    returnLastWord(" ")
    returnLastWord("")


if __name__ == '__main__':
    test_returnLastWord()
