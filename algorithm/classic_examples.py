#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/24 3:02 下午
# @Author  : octy

"""
动态规划，位运算，贪心算法，局部最优解
实现以及应用范围
"""


def calc_max_profit_with_dp(prices):
    """
    LeetCode 经典题库 122. 买卖股票的最佳时机 II
    假设你有一个数组，其中第i个元素是股票在第i天的价格。你可以随时买入和卖出的机会。（只有买入股票以后才能卖出）。请你设计一个算法来
    计算可以获得的最大收益。
    解决方案：
    动态优化
    时间复杂度：O(n), 空间复杂度：O(n)
    """
    # calculates the maximum profit of the prices in stacks
    # use dynamic programming
    # 状态转移方程：dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
    #            dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])
    prices_length = len(prices)
    dp = [[0, 0] for _ in range(prices_length)]
    dp[0][0] = 0  # 未持有股票收益
    dp[0][1] = 0 - prices[0]  # 持有股票收益

    for i in range(1, prices_length):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
    return dp[prices_length - 1][0]


def climb_stairs_dp(num):
    """
    LeetCode 经典题库 70. 爬楼梯
    解决方案：
    动态规划
    时间复杂度: O(n), 空间复杂度: O(1)
    状态转移方程:
    f(1) = 1
    f(2) = 2
    f(n) = f(n-1) + f(n-2) n >= 3
    """
    if num == 1:
        return 1
    fn_2, fn_1 = 1, 2
    for i in range(3, num + 1):
        current = fn_2 + fn_1
        fn_2, fn_1 = fn_1, current
    return fn_1


def find_minimum_path_sum(triangle):
    """
    LeetCode 经典题库 120. 三角形最小路径之和
    给定一个三角形 triangle ，找出自顶向下的最小路径和。
    每一步只能移动到下一行中相邻的结点上。
    相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。
    也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。
    解决方案：
    动态规划：
    时间复杂度：O(n*m), 空间复杂度: O(n*m)
    """
    # calculate the minimum path sum in a triangle
    # use dynamic programming
    # 状态转移方程：
    # dp[i][j] = min(dp[i-1][j], dp[i-1][j-1]) + triangle[i][j]
    # dp[i][0] = dp[i-1][0] + triangle[i][0]
    length = len(triangle)
    min_value = []
    for i in range(length):
        min_value.append([])
        for j in range(len(triangle[i])):
            if i - 1 < 0:
                min_value[i].append(triangle[i][j])
                continue
            elif j - 1 < 0:
                min_value[i].append(min_value[i - 1][0] + triangle[i][j])
                continue
            else:
                if i - 1 < j:
                    min_value[i].append(min_value[i - 1][j - 1] + triangle[i][j])
                else:
                    min_value[i].append(min(min_value[i - 1][j], min_value[i - 1][j - 1]) + triangle[i][j])
    return min(min_value[-1])
