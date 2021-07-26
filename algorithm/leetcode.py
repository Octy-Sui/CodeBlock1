#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/15 11:10 下午
# @Author  : octy
from advanced.MyDecorator import timer
from config.logger import logRecorder


"""
给定一个整数数组 nums和一个整数目标值 target，请你在该数组中找出 和为目标值 target的那两个整数，并返回它们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。
"""


@timer
def twoSum(nums, target):
    hashmap = {}
    for ind, num in enumerate(nums):
        hashmap[num] = ind
    for i, num in enumerate(nums):
        j = hashmap.get(target - num)
        if j is not None and i != j:
            return [i, j]


if __name__ == "__main__":
    twoSum([1, 2, 3, 4, 5, 6], 5)
