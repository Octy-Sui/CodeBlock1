#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/20 7:08 下午
# @Author  : octy

from advanced.DataStructure import Stack


def calc_max_profit(price_list):
    """
    假设你有一个数组，其中第i个元素是股票在第i天的价格。你有一次买入和卖出的机会。（只有买入股票以后才能卖出）。请你设计一个算法来
    计算可以获得的最大收益。
    探索规律：
    前后差值最大的两个数字
    时间复杂度：O(n), 空间复杂度：O(n)
    """
    profits = []
    cost = price_list[0]
    for price in price_list:
        profits.append(price - cost)
        if price < cost:
            cost = price
            continue
    max_profit = max(profits)
    return max_profit if max_profit > 0 else 0


def generate_fibonacci(max_terms):
    """
    斐波那契数列
    非递归实现
    """
    prev, curr = 0, 1
    while max_terms > 0:
        max_terms -= 1
        yield curr
        prev, curr = curr, prev + curr


# 定义括号映射和常量
BRACKETS_MAP = {"{": "}", "[": "]", "(": ")"}
OPEN_BRACKETS = BRACKETS_MAP.keys()
CLOSE_BRACKETS = BRACKETS_MAP.values()
MISMATCH_MSG = "mismatch"
MATCH_MSG = "match"


def match_brackets(input_str):
    """
    有效括号匹配
    时间复杂度：O(n), 空间复杂度：O(n)
    """
    my_stack = Stack()
    for curr_marker in input_str:
        # 忽略非括号字符
        if curr_marker not in OPEN_BRACKETS and curr_marker not in CLOSE_BRACKETS:
            continue

        if my_stack.is_empty():
            my_stack.push(curr_marker)
            continue
        else:
            pre_marker = my_stack.pop()
        # 检查匹配情况
        if pre_marker in OPEN_BRACKETS and curr_marker == BRACKETS_MAP[pre_marker]:
            continue
        else:
            # 发现不匹配，重新压入栈以供后续处理或报告
            my_stack.push(pre_marker)
            my_stack.push(curr_marker)

    # 栈为空表示完全匹配
    if my_stack.is_empty():
        print(f"{input_str} {MATCH_MSG}")
    else:
        print(f"{input_str} {MISMATCH_MSG}")


if __name__ == '__main__':
    input_list = [7, 1, 5, 3, 6, 4]
    rv = calc_max_profit(input_list)
    print(rv)
