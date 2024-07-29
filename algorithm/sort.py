#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2020/6/8 10:29 下午
# @Author  : octy

from advanced.BinaryTree import MaxHeap

def swap(lyst, i, j):
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def bubble_sort(lyst):
    """
    冒泡排序
    Algorithm complexity：O(n^2)
    时间复杂度：O(n^2), 空间复杂度：O(1) 稳定
    """
    length = len(lyst)
    while length:
        i = 0
        swapped = False
        while i < length - 1:
            if lyst[i] > lyst[i + 1]:
                swap(lyst, i, i + 1)
                swapped = True
            i += 1
        if not swapped:
            break
        length -= 1
    print(lyst)


def selection_sort(lyst):
    """
    选择排序
    Algorithm complexity：O(n^2)
    时间复杂度：O(n^2), 空间复杂度：O(1) 不稳定
    """
    for i in range(len(lyst)):
        min_index = i
        for j in range(i + 1, len(lyst)):
            if lyst[min_index] > lyst[j]:
                min_index = j
        if min_index != i:
            swap(lyst, i, min_index)
    print(lyst)


def insertion_sort(arr):
    """
    插入排序
    Algorithm complexity：O(n^2)
    时间复杂度：O(n^2), 空间复杂度：O(1) 稳定
    """
    for i in range(1, len(arr)):  # 从1开始, 默认arr[0]为已排序部分
        key = arr[i]
        j = i - 1
        # 将arr[i]与已排序部分的元素从后往前比较
        while j >= 0 and key < arr[j]:
            # 如果当前元素大于key，将当前元素向后移一位
            arr[j + 1] = arr[j]
            j -= 1
        # 在已排序部分找到key的正确位置并插入
        arr[j + 1] = key


def partition(lyst, left, right):
    """
    双边循环的partition函数
    Algorithm complexity：O(n)
    时间复杂度：O(n), 空间复杂度：O(1) 不稳定
    """
    if right - left > 1:  # 如果数组长度大于2, 则选择列表第一个元素、中间元素和最后一个元素的中位数作为pivot
        mid = (left + right) // 2
        if lyst[left] <= lyst[mid] <= lyst[right]:
            pivot_index = mid
        elif lyst[left] < lyst[right] < lyst[mid]:
            pivot_index = right
        else:
            pivot_index = left
    else:  # 如果数组长度小于2, 则选择第一个元素作为pivot
        pivot_index = left
    pivot_value = lyst[pivot_index]
    while left < right:  # 循环结束条件：left == right
        while right > left and lyst[right] > pivot_value:
            # 从右往左找比pivot小的元素;
            # 找到后，结束右侧遍历; 与pivot数值swap
            # 切换至左侧遍历
            right -= 1
        # 将右侧比pivot小的元素放到目前pivot_index的位置
        lyst[pivot_index] = lyst[right]
        # 更新pivot的index
        pivot_index = right
        # lyst[pivot_index] = None
        while left < right and lyst[left] < pivot_value:
            # 从左往右找比pivot大的元素;
            # 找到后，结束左侧遍历; 与pivot数值swap
            # 切换至右侧遍历
            left += 1
        lyst[pivot_index] = lyst[left]
        pivot_index = left
        # lyst[pivot_index] = None
    lyst[pivot_index] = pivot_value
    return pivot_index


def partition_v2(arr, left, right):
    """
    单边循环的partition函数
    Algorithm complexity：O(n)
    时间复杂度：O(n), 空间复杂度：O(1) 不稳定
    """
    pivot = left
    marker = pivot
    cursor = marker
    while cursor <= right:
        if arr[cursor] < arr[pivot]:
            marker += 1  # 识别到小于pivot的元素，marker右移一位
            swap(arr, cursor, marker)  # 交换小于pivot的元素至列表左侧
        cursor += 1
    swap(arr, pivot, marker)  # 将pivot元素放到小于和大于pivot元素的中间位置
    return marker


def quick_sort(lyst, left=None, right=None):
    """
    快速排序
    Algorithm complexity：O(nlogn)
    时间复杂度：O(nlogn), 空间复杂度：O(logn) 不稳定
    """
    left = 0 if left is None else left
    right = len(lyst) - 1 if right is None else right
    if left < right:
        # print("iteration count")
        pivot_index = partition_v2(lyst, left, right)
        quick_sort(lyst, left, pivot_index - 1)
        quick_sort(lyst, pivot_index + 1, right)
    return lyst


def heap_sort(lyst):
    """
    堆排序
    Algorithm complexity：O(nlogn)
    时间复杂度：O(nlogn), 空间复杂度：O(1) 不稳定
    """
    # 把无序数组构建最大堆
    for i in range(len(lyst) // 2 - 1, -1, -1):
        MaxHeap.down_adjust(lyst, i, len(lyst))

    # 循环删除堆顶元素，移到列表尾部，并重新调整堆结构
    for i in range(len(lyst) - 1, 0, -1):
        # 把堆顶元素与末尾元素交换
        lyst[0], lyst[i] = lyst[i], lyst[0]
        MaxHeap.down_adjust(lyst, 0, i)

    return lyst


def selectionSort(lyst):
    """
    选择排序
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
    print(lyst)


def bubbleSort(lyst):
    """
    冒泡排序
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
    print(lyst)


if __name__ == '__main__':
    bubble_sort([1, 7, 11, 8, 12, 9, 10])
    selectionSort([1, 7, 11, 8, 12, 9, 10])
    print(quick_sort([12, 7, 11, 8, 21, 9, 10, 5]))
    print(heap_sort([12, 7, 11, 8, 21, 9, 10, 5]))
