#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/15 9:57 下午
# @Author  : octy


def return_sub(input_str):
    """
    子集包含：空集、自身等组合场景
    借助位运算求解
    字符串的每个位置状态，借助byte值来确定；0不取，1取
    """
    # find all sub list depending on input list
    length = len(input_str)
    combo = []
    for i in range(2 ** length):
        sub = []
        for j in range(length):
            if (i >> j) % 2:  # 确认第j位byte是否为1; 已确认该值是否选择
                sub.append(input_str[j])
        combo.append("".join(sub))
    print("length: {0}, {1}".format(len(combo), combo))


def climb_stairs(num):
    """
    一只青蛙一次可以跳上1级台阶，也可以跳上2级，求青蛙跳上一个n级的台阶总共多少种跳法（先后次序不同算不同的结果）
    探索规律：
    (1):1
    (2):11, 2
    (3):111, 12, 21或者(1)2, (2)1
    (4):1111, 112, 22, 121, 211或者(2)2, (3)1
    (5):(3)2, (4)1
    解决方案：
    递归解决
    时间复杂度: O(n^2), 空间复杂度: O(n)
    状态转移方程:
    f(1) = 1
    f(2) = 2
    f(n) = f(n-1) + f(n-2) n >= 3
    """
    if num == 1:
        return 1
    elif num == 2:
        return 2
    else:
        return climb_stairs(num - 1) + climb_stairs(num - 2)


def count_character_in_str_without_repeat(string):
    """
    统计给定字符中每个字符出现次数
    解决方案：
    遍历+哈希表
    时间复杂度: O(n), 空间复杂度: O(n)
    """
    tmp = {}
    for s in string:
        if s in tmp.keys():
            tmp[s] = tmp[s] + 1
        else:
            tmp[s] = 1
    return tmp


def in_or_not(num):
    """
    判断给定数字是否在制定列表内
    解决方案：
    二分查找
    时间复杂度: O(logn), 空间复杂度: O(1)
    """
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


def return_length_of_last_word(s):
    """
    返回字符串最后一个单词的长度
    解决方案：
    倒序遍历
    时间复杂度: O(n), 空间复杂度: O(m)
    """
    # return the length of last word in a string
    print("The result of " + s)
    delimiter = [" "]
    s = s.strip()
    length = len(s)
    if length == 0:
        print(0)
        return 0
    word_count = 0
    for i in range(length - 1, 0, -1):
        if s[i] not in delimiter:
            continue
        else:
            word_count = length - 1 - i
            break
    print(word_count)
    return word_count


class RainWaterTrapCalculator:
    # calculate the water trapped in a region
    # use two pointers to detect the left and right wall

    @staticmethod
    def calculate_water_in_region(wall_heights):
        max_height = min(wall_heights[0], wall_heights[-1])
        water_volume = 0
        for height in wall_heights:
            if height < max_height:
                water_volume += (max_height - height)
        return water_volume

    def total_trapped_water(self, heights):
        left_wall_detected = False
        left_pointer = 0
        total_water = 0
        for i in range(1, len(heights)):
            if not left_wall_detected:
                if heights[i - 1] <= heights[i]:
                    left_pointer = i
                else:
                    left_wall_detected = True
            else:
                if heights[i - 1] < heights[i]:
                    total_water = total_water + self.calculate_water_in_region(heights[left_pointer:i + 1])
                    left_wall_detected = False
                    left_pointer = i
        return total_water


if __name__ == "__main__":
    return_sub('asdfghjkl')
    # rv = countInStr("adfsdfsafefaf,;,a.da''.")
    # print(rv)
    # InOrNot(4)
    # input_list = [4, 2, 0, 3, 2, 5]
    # obj = RainWaterTrapCalculator()
    # print(obj.total_trapped_water(input_list))
