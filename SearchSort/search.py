#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2020/6/8 7:35 下午
# @Author  : octy


def indexOfMin(lyst):
    """
    find the min number in lyst, return the index;
    Algorithm complexity：O(n)

    :param list lyst: input para
    :return: min_index
    """
    min_index = 0
    current_index = 1
    while current_index < len(lyst):
        if lyst[current_index] < lyst[min_index]:
            min_index = current_index
        current_index += 1
    return current_index


def sequentialSearch(target, lyst):
    """
    linear search, return the index of target value in lyst, -1 otherwise;
    Algorithm complexity：O(n)

    :param target: target
    :param lyst: input list
    :return:  min index
    """
    index = 0
    while index < len(lyst):
        if target == lyst[index]:
            return index
        index += 1
    return -1


def binarySearch(target, sortedLyst):
    """
    search a key value return the index;
    Algorithm complexity：O(log2N)

    :param target: target value
    :param sortedLyst: sorted lyst
    :return:  index of key value or -1 otherwise
    """
    left = 0
    right = len(sortedLyst) - 1
    while left <= right:
        mid_point = (left + right) // 2
        mid_value = sortedLyst[mid_point]
        if target == mid_value:
            return mid_point
        elif target < mid_value:
            right = mid_point - 1
        else:
            left = mid_point + 1
    return -1
