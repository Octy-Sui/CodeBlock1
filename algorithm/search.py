#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2020/6/8 7:35 下午
# @Author  : octy


def index_of_min_in_lyst(lyst):
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


def sequential_search(target, lyst):
    """
    线性查找
    linear search, return the index of target value in lyst, -1 otherwise;
    Algorithm complexity：O(n)
    时间复杂度：O(n), 空间复杂度：O(1)
    """
    index = 0
    while index < len(lyst):
        if target == lyst[index]:
            return index
        index += 1
    return -1


def binary_search(target, sorted_lyst):
    """
    二分查找
    search a key value return the index using in binary search
    Algorithm complexity：O(log2N)
    时间复杂度：O(log2N), 空间复杂度：O(1)
    """
    left, right = 0, len(sorted_lyst) - 1
    i = 0
    while left <= right:
        i += 1
        mid_index = (left + right) // 2
        if target == sorted_lyst[mid_index]:
            print(f"iteration count: {i}")
            return mid_index
        elif target < sorted_lyst[mid_index]:
            right = mid_index - 1
        else:
            left = mid_index + 1
    print(f"iteration count: {i}")
    return -1


def interpolation_search(target, sorted_lyst):
    """
    插值查找
    search a key value return the index using in interpolation search
    Algorithm complexity：O(log2N)
    时间复杂度：O(log2N), 空间复杂度：O(1)
    """
    left, right = 0, len(sorted_lyst) - 1
    i = 0
    while left < right:
        i += 1
        mid_index = left + (right - left) * (target - sorted_lyst[left]) // (sorted_lyst[right] - sorted_lyst[left])
        # 边界判断, 插值查找
        if mid_index < left or mid_index > right:
            print(f"iteration count: {i}")
            return -1
        if target == sorted_lyst[mid_index]:
            print(f"iteration count: {i}")
            return mid_index
        elif target < sorted_lyst[mid_index]:
            right = mid_index - 1
        else:
            left = mid_index + 1
    if left == 0:
        if target == sorted_lyst[left]:
            return left
    print(f"iteration count: {i}")
    return -1


def bst_search(target, sorted_lyst):
    """
    二叉查找树查找
    search a key value return the index using in binary search
    Algorithm complexity：O(log2N)
    时间复杂度：O(log2N), 空间复杂度：O(1)
    """
    # 见BinaryTree.py模块
    pass


if __name__ == '__main__':
    print(binary_search(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(interpolation_search(10, [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(binary_search(6, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(binary_search(6, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(interpolation_search(0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(interpolation_search(11, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(interpolation_search(11, [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]))
    print(interpolation_search(100, [1, 2, 3, 4, 5, 6, 7, 10, 90000]))
    print(binary_search(100, [100]))

