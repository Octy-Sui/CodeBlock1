# File   : practice.py
# Created: 2026-08-07 14:32:36
# Author : octy Sui

"""算法训练."""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    lst = [[5, 9], [2, 6], [8, 10], [15, 18]]
    lst = [[1, 3], [2, 6], [8, 10], [15, 18]]
    lst = [[1, 4], [4, 5]]
    lst = [[1, 4]]
    """
    if not len(intervals):
        raise ValueError("intervals 无具体数据")
    for i in range(len(intervals)):
        min_left_value = intervals[i][0]
        min_left_index = i
        for j in range(i + 1, len(intervals)):
            if min_left_value > intervals[j][0]:
                min_left_value = intervals[j][0]
                min_left_index = j
        if i != min_left_index:
            intervals[i], intervals[min_left_index] = (
                intervals[min_left_index],
                intervals[i],
            )

    if len(intervals) == 1:
        return intervals
    tmp = []
    merge_lst = intervals[0]
    for k in range(1, len(intervals)):
        if intervals[k][0] <= merge_lst[1]:
            merge_lst = [
                min(merge_lst[0], intervals[k][0]),
                max(merge_lst[1], intervals[k][1]),
            ]
        else:
            tmp.append(merge_lst)
            merge_lst = intervals[k]
    tmp.append(merge_lst)

    return tmp


def calc_max_sub_array_length(nums: list[int], k: int) -> int:
    """最多 K 个重复元素的最长子数组长度"""
    len_max_sub_array = 0
    from collections import deque

    cursor = left = 0

    while cursor < len(nums):
        elem_cnt: dict[int, tuple[int, deque[int]]] = {}
        for ind in range(left, len(nums)):
            num = nums[ind]
            if num in elem_cnt:
                count, indexes = elem_cnt[num]
                count += 1
                indexes.append(ind)
                elem_cnt[num] = (count, indexes)
                if elem_cnt[num][0] > k:
                    len_max_sub_array = max(ind - left, len_max_sub_array)
                    cursor = left = elem_cnt[num][1].popleft() + 1
                    break
            else:
                d = deque(maxlen=k + 1)  # 防止自行丢元素
                d.append(ind)
                elem_cnt[num] = (1, d)
            cursor = ind + 1
            len_max_sub_array = max(ind - left + 1, len_max_sub_array)
    return len_max_sub_array


def calc_max_sub_array_length_v2(nums: list[int], k: int) -> int:
    """
    标准滑动窗口
    """
    max_length = left = 0
    counts: dict[int, int] = {}

    for right, num in enumerate(nums):
        counts[num] = counts.get(num, 0) + 1

        while counts[num] > k:
            counts[nums[left]] -= 1
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length


def main() -> None:
    lst = [[5, 9], [2, 6], [8, 10], [15, 18]]
    print(merge_intervals(lst))


if __name__ == "__main__":
    nums = [2, 2, 3]
    k = 1
    print(calc_max_sub_array_length(nums=nums, k=k))
