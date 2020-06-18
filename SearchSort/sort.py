#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2020/6/8 10:29 下午
# @Author  : octy


def swap(lyst, i, j):
    temp =  lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def selectionSort(lyst):
    """
    Algorithm complexity：O(n^2)

    :param lyst:
    :return:
    """
    i = 0
    while i < len(lyst) - 1:
        min_index = i
        j = i + 1
        while j < len(lyst):
            if lyst[j] < lyst[min_index]:
                min_index = j
            j += 1
        if min_index != i:
            swap(lyst, min_index, i)
        i += 1


def bubbleSort(lyst):
    """
    Algorithm complexity：O(n^2)

    :param lyst:
    :return: 
    """
    n = len(lyst)
    while n > 1:
        i = 1
        while i < n:
            if lyst[i] < lyst[i - 1]:
                swap(lyst, i, i - 1)
            i += 1
        n -= 1

