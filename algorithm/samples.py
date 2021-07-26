#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/15 9:57 下午
# @Author  : octy


def returnSub(l):
    length = len(l)
    for i in range(2 ** length):
        combo = []
        print("i is {}".format(i))
        for j in range(length):
            if (i >> j) % 2:
                print("j is {}".format(j))
                print(i >> j)
                print("++++")
                combo.append(l[j])
        print(combo)


def jumpFloor(num):
    """
    一只青蛙一次可以跳上1级台阶，也可以跳上2级，求青蛙跳上一个n级的台阶总共多少种跳法（先后次序不同算不同的结果）
    探索规律：
    (1):1
    (2):11, 2
    (3):111, 12, 21或者(1)2, (2)1
    (4):1111, 112, 22, 121, 211或者(2)2, (3)1
    (5):(3)2, (4)1
    :param num:
    :return:
    """
    if num == 1:
        return 1
    elif num == 2:
        return 2
    else:
        return jumpFloor(num - 1) + jumpFloor(num - 2)


def maxProfit(price_list):
    """
    假设你有一个数组，其中第i个元素是股票在第i天的价格。你有一次买入和卖出的机会。（只有买入股票以后才能卖出）。请你设计一个算法来
    计算可以获得的最大收益。
    探索规律：
    前后差值最大的两个数字
    :param price_list:
    :return:
    """
    rv = []
    count = 0
    for buy in price_list:
        count += 1
        for sale in price_list[count:]:
            rv.append(sale - buy)
    max_profit = max(rv)
    return max_profit if max_profit > 0 else 0


def countInStr(string):
    """
    统计给定字符中每个字符出现次数
    :param string:
    :return:
    """
    tmp = {}
    for s in string:
        if s in tmp.keys():
            tmp[s] = tmp[s] + 1
        else:
            tmp[s] = 1
    return tmp


def InOrNot(num):
    lyst = [1, 3, 5, 8, 11, 15, 17, 18, 24, 26, 29, 33, 41]
    length = len(lyst)
    head = 0
    tail = length - 1
    flag = False
    while True:
        if tail - head == 1:
            if lyst[tail] == num or lyst[head] == num:
                flag = True
                break
            break
        pointer = (tail + head) // 2
        if lyst[pointer] == num:
            flag = True
            break
        if lyst[pointer] > num:
            tail = pointer
        else:
            head = pointer
    print(flag)


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


def test_demo():
    pass


if __name__ == "__main__":
    rv = countInStr("adfsdfsafefaf,;,a.da''.")
    print(rv)
    InOrNot(4)
