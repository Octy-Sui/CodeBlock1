# @Time    :2024/7/20 11:19
# @Author  : octy


from heapq import heapify, heappop, heappush

from advanced.data_structure import Stack
from advanced.list_node import ListNode, convert_list_to_link_list
from config.timer import timer


def two_sum(nums, target):
    """
    LeetCode 经典题库 1. 两数之和
    给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
    你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。
    你可以按任意顺序返回答案。
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    You can return the answer in any order.
    >>> two_sum(nums = [2,7,11,15], target = 9)
    [0,1]
    >>> two_sum(nums = [3,2,4], target = 6)
    [1,2]
    解题思路：
    方法一：暴力枚举，遍历数组 时间复杂度: O(n^2) 空间复杂度: O(1)
    方法二: hash表 时间复杂度: O(n) 空间复杂度: O(n) - [主要为hash表的空间开销]
    """
    hashmap = {}
    for ind, num in enumerate(nums):
        hashmap[num] = ind
    for i, num in enumerate(nums):
        j = hashmap.get(target - num)
        if j is not None and i != j:
            return [i, j]


def add_two_str_numbers(l1, l2):
    """
    LeetCode 经典题库 2. 两数相加
    给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
    如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
    您可以假设除了数字 0 之外，这两个数都不会以 0 开头。
    >>> add_two_str_numbers(l1 = [2,4,3],l2 = [5,6,4])
    [7,0,8] (807)
    >>> add_two_str_numbers(l1 = [0], l2 = [0])
    [0] (0)
    >>> add_two_str_numbers(l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9])
    [8,9,9,9,0,0,0,1] (10009998)
    解题思路：
    模拟：顺序相加即可，注意处理进位的不同场景; 时间复杂度: O(max(m,n)) 空间复杂度: O(1)
    """
    head_node = work_node = ListNode(0)
    left, right = l1, l2
    while True:
        if left is None:
            left_value = 0
        else:
            left_value = left.data
            left = left.next
        if right is None:
            right_value = 0
        else:
            right_value = right.data
            right = right.next
        add_two = left_value + right_value + work_node.val
        work_node.val = add_two % 10
        if left is None and right is None:
            break
        work_node.next = ListNode(add_two // 10)
        work_node = work_node.next
    if add_two // 10:
        work_node.next = ListNode(add_two // 10)
    return head_node


def calc_max_length_of_sub_str(string):
    """
    LeetCode 经典题库 3. 无重复字符的最长子串
    给定一个字符串 s ，请你找出其中不含有重复字符的最长子串的长度。 s 由英文字母、数字、符号和空格组成
    >>> calc_max_length_of_sub_str(s = "abcabcbb")
    3 (abc)
    >>> calc_max_length_of_sub_str(s = "bbbbb")
    1(b)
    >>> calc_max_length_of_sub_str(s = "pwwkew")
    3(kew)
    解题思路：
    滑动窗口 注意左右窗口边界和整个序列的左右边界处理 时间复杂度: O(n) -> O(n^2), 空间复杂度: O(∣Σ∣)
    """
    max_length = 0
    head = tail = 0
    length_str = len(string)
    while tail < length_str:
        for pointer in range(tail, length_str):
            if string[pointer] in string[head:tail]:
                break
            tail += 1
        max_length = max(max_length, tail - head)
        if tail < length_str:
            head = head + string[head:tail].index(string[tail]) + 1
    print(max_length)
    return max_length


def calc_max_length_of_sub_str_v2(string):
    """
    LeetCode 经典题库 3. 无重复字符的最长子串
    给定一个字符串 s ，请你找出其中不含有重复字符的最长子串的长度。 s 由英文字母、数字、符号和空格组成
    >>> calc_max_length_of_sub_str(s = "abcabcbb")
    3 (abc)
    >>> calc_max_length_of_sub_str(s = "bbbbb")
    1(b)
    >>> calc_max_length_of_sub_str(s = "pwwkew")
    """
    char_set = set()
    max_length = 0
    left = 0

    for right in range(len(string)):
        while string[right] in char_set:
            char_set.remove(string[left])
            left += 1
        char_set.add(string[right])
        max_length = max(max_length, right - left + 1)

    return max_length


def find_median_in_two_arrays(array1, array2):
    """
    LeetCode 经典题库 4. 寻找两个正序数组的中位数
    给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的 中位数 。
    >>> find_median_in_two_arrays(nums1 = [1,3], nums2 = [2])
    2.00000
    >>> find_median_in_two_arrays(nums1 = [1,2], nums2 = [3,4])
    2.5000
    解题思路：
    方法一：粗暴合并数组、排序、取中位数 时间复杂度: O(m+n) 空间复杂度: O(m+n)
    方法二：指针遍历 时间复杂度: O(m+n) 空间复杂度: O(1); 本函数采用方法
    方法三：基于中位数K进行二分查找 时间复杂度: O(log(m+n)) 空间复杂度: O(1); 求中位数，实际是求第k大的数；数组有序，适合采用二分查找
    方法四：基于最小数组的长度，二分查找 时间复杂度: O(log(min(m,n))) 空间复杂度: O(1); 假设m<=n，则数组1为最小数组，数组2为最大数组
    """
    pointer1 = pointer2 = 0
    len_array1, len_array2 = len(array1), len(array2)
    len_arrays = len_array1 + len_array2
    median_pointer1, median_pointer2 = len_arrays // 2 - 1, len_arrays // 2
    tmp_median_pointer1, tmp_median_pointer2 = -1, -1
    tmp_median_value1, tmp_median_value2 = -1, -1
    while pointer1 < len_array1 or pointer2 < len_array2:
        if pointer1 == len_array1:
            small_value = array2[pointer2]
            if pointer2 < len_array2:
                pointer2 += 1
        if pointer2 == len_array2:
            small_value = array1[pointer1]
            if pointer1 < len_array1:
                pointer1 += 1
        if pointer1 < len_array1 and pointer2 < len_array2:
            if array1[pointer1] < array2[pointer2]:
                small_value = array1[pointer1]
                if pointer1 < len_array1:
                    pointer1 += 1
            else:
                small_value = array2[pointer2]
                if pointer2 < len_array2:
                    pointer2 += 1
        tmp_median_pointer1 += 1
        tmp_median_pointer2 += 1
        if tmp_median_pointer1 == median_pointer1:
            tmp_median_value1 = small_value
        if tmp_median_pointer2 == median_pointer2:
            tmp_median_value2 = small_value
            break
    if len_arrays % 2 == 0:
        return (tmp_median_value1 + tmp_median_value2) / 2.0
    else:
        return tmp_median_value2


def match_brackets(input_str):
    """
    LeetCode 经典题库 20. 有效括号匹配
    时间复杂度：O(n), 空间复杂度：O(n)
    """
    my_stack = Stack()
    # 定义括号映射和常量
    BRACKETS_MAP = {"{": "}", "[": "]", "(": ")"}
    OPEN_BRACKETS = BRACKETS_MAP.keys()
    CLOSE_BRACKETS = BRACKETS_MAP.values()
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
        print(f"{input_str} mismatch")
    else:
        print(f"{input_str} match")


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """
    LeetCode 经典题库 21. 合并两个有序链表
    时间复杂度：O(n+m), 空间复杂度：O(1)
    """
    if a is None or b is None:
        return a if a is not None else b

    head = ListNode(0)
    tail = head

    a_ptr = a
    b_ptr = b

    while a_ptr is not None and b_ptr is not None:
        if a_ptr.val < b_ptr.val:
            tail.next = a_ptr
            a_ptr = a_ptr.next
        else:
            tail.next = b_ptr
            b_ptr = b_ptr.next

        tail = tail.next

    tail.next = a_ptr if a_ptr is not None else b_ptr

    return head.next


def generate_parenthesis(n: int) -> list[str]:
    """
    动态规划：
    dp[i]表示i组括号的所有有效组合
    dp[i] = "(dp[p]的所有有效组合)+【dp[q]的组合】"，
    其中 p + q = i - 1 , p从0遍历到i-1, q则相应从i-1到0, p q均可为0
    """
    dp = [[] for _ in range(n + 1)]  # dp[i]存放i组括号的所有有效组合
    dp[0] = [""]  # 初始化dp[0]
    for i in range(1, n + 1):  # 计算dp[i]
        for p in range(i):  # 遍历p
            l1 = dp[p]  # 得到dp[p]的所有有效组合
            l2 = dp[i - 1 - p]  # 得到dp[q]的所有有效组合
            for k1 in l1:
                for k2 in l2:
                    dp[i].append(f"({k1}){k2}")
    return dp[n]


def merge_k_list(lists: list[ListNode | None]) -> ListNode | None:
    """
    LeetCode LCR78. 合并k个升序链表
    时间复杂度：O(k^2n), 空间复杂度：O(1)
    """
    if not lists or lists[0] is None:
        return None
    head = tmp = None
    while True:
        min_value = None
        min_ptr = None
        for i in range(len(lists)):
            cursor = lists[i]
            if cursor is None:
                continue
            if min_value is None or cursor.val <= min_value:
                min_value = cursor.val
                min_ptr = i
        if min_value is None or min_ptr is None:
            break
        if tmp is None:
            tmp = ListNode(min_value)
            if head is None:
                head = tmp
        else:
            tmp.next = ListNode(min_value)
            tmp = tmp.next
        node = lists[min_ptr]
        if node is not None:
            lists[min_ptr] = node.next
    return head


def merge_k_list_partition(lists: list[ListNode | None]) -> ListNode | None:
    m = len(lists)
    if m == 0:
        return None  # 注意输入的 lists 可能是空的
    if m == 1:
        return lists[0]  # 无需合并，直接返回
    left = merge_k_list_partition(lists[: m // 2])  # 合并左半部分
    right = merge_k_list_partition(lists[m // 2 :])  # 合并右半部分
    return merge_two_lists(left, right)  # 最后把左半和右半合并


def merge_k_list_min_heap(lists: list[ListNode | None]) -> ListNode | None:
    cur = dummy = ListNode(0)  # 哨兵节点，作为合并后链表头节点的前一个节点
    h = [head for head in lists if head]  # 初始把所有链表的头节点入堆
    heapify(h)  # 堆化
    while h:  # 循环直到堆为空
        node = heappop(h)  # 剩余节点中的最小节点
        if node.next:  # 下一个节点不为空
            heappush(h, node.next)  # 下一个节点有可能是最小节点，入堆
        cur.next = node  # 合并到新链表中
        cur = cur.next  # 准备合并下一个节点
    return dummy.next  # 哨兵节点的下一个节点就是新链表的头节点


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    LeetCode 经典题库56. 合并区间
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


def return_length_of_last_word(s):
    """
    LeetCode 经典题库58. 最后一个单词的长度
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


def climb_stairs(num):
    """
    LeetCode 经典题库70. 爬楼梯
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


def calc_max_profit(price_list):
    """
    LeetCode 经典题库 121. 买卖股票的最佳时机
    假设你有一个数组，其中第i个元素是股票在第i天的价格。你有一次买入和卖出的机会。（只有买入股票以后才能卖出）。请你设计一个算法来
    计算可以获得的最大收益。
    探索规律：
    前后差值最大的两个数字
    时间复杂度：O(n), 空间复杂度：O(1)
    """
    max_profit = 0
    cost = price_list[0]
    for price in price_list:
        max_profit = max(max_profit, (price - cost))
        if price < cost:
            cost = price
            continue
    return majority_frequency_group


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """
    LeetCode 经典题库219. 存在重复元素 II
    解决方案：
    固定滑动窗口
    时间复杂度：O(n), 空间复杂度：O(1)
    """
    for left, left_value in enumerate(nums):
        for right in range(
            left + 1, min(left + k + 1, len(nums))
        ):  # 只关心距离 <= k， 后面的元素都没必要再检查
            if left_value == nums[right]:
                return True
    return False


def contains_nearby_duplicate_v2(nums: list[int], k: int) -> bool:
    """哈希表记录最近一次出现位置"""
    last_index: dict[int, int] = {}

    for index, num in enumerate(nums):
        if num in last_index and index - last_index[num] <= k:
            return True

        last_index[num] = index

    return False


def can_construct(ransomNote: str, magazine: str) -> bool:
    """
    LeetCode 经典题库 383 赎金信
    """
    note_map: dict[str, int] = {}
    mgz_map: dict[str, int] = {}
    for i in ransomNote:
        note_map[i] = note_map.get(i, 0) + 1
    for j in magazine:
        mgz_map[j] = mgz_map.get(j, 0) + 1
    for k, cnt in note_map.items():
        if k not in mgz_map:
            return False
        if cnt > mgz_map[k]:
            return False
    return True


def can_construct_v2(ransomNote: str, magazine: str) -> bool:
    """限定字符为小写英文字母，因此不需要 dict, 使用 list"""
    if len(ransomNote) > len(magazine):
        return False

    counts = [0] * 26

    for char in magazine:
        counts[ord(char) - 97] += 1

    for char in ransomNote:
        index = ord(char) - 97
        counts[index] -= 1

        if counts[index] < 0:
            return False

    return True


def calc_max_sum_of_almost_only_subarray(nums: list[int], m: int, k: int) -> int:
    """
    LeetCode 经典题库2841. 几乎唯一子数组的最大和
    本method实现为，包含任意k个中含m个不同元素的组合数组，非v2中的顺序k个元素包含m个不同元素
    """
    num_cnt_map: dict[int, int] = {}
    for num in nums:
        num_cnt_map[num] = num_cnt_map.get(num, 0) + 1
    if len(num_cnt_map) < m:
        return 0
    if len(nums) == k:
        return sum(nums)
    if m == k:
        return sum(num_cnt_map.keys())
    sub = k - m
    result = 0
    for num, cnt in sorted(num_cnt_map.items(), reverse=True):
        if m:
            m -= 1
            result += num
        if not m and not sub:
            break
        if sub:
            delta = cnt - 1
            if delta >= sub:
                result += num * sub
                sub -= sub
            else:
                result += num * delta
                sub -= delta
    return result


def calc_max_sum_of_almost_only_subarray_v2(nums: list[int], m: int, k: int) -> int:
    num_cnt_map: dict[int, int] = {}
    max_sum = tmp_sum = 0
    for i in range(k):
        num = nums[i]
        num_cnt_map[num] = num_cnt_map.get(num, 0) + 1
        tmp_sum += num
    if len(num_cnt_map) >= m:
        max_sum = max(max_sum, tmp_sum)
    for left in range(1, len(nums)):
        right = left + k
        if right > len(nums):
            break
        to_delete_num = nums[left - 1]
        tmp_sum -= to_delete_num
        num_cnt_map[to_delete_num] = num_cnt_map.get(to_delete_num, 1) - 1
        if not num_cnt_map[to_delete_num]:
            del num_cnt_map[to_delete_num]
        new_added_num = nums[right - 1]
        tmp_sum += new_added_num
        num_cnt_map[new_added_num] = num_cnt_map.get(new_added_num, 0) + 1
        if len(num_cnt_map) >= m:
            max_sum = max(max_sum, tmp_sum)
    return max_sum


def calc_max_sub_array_length(nums: list[int], k: int) -> int:
    """
    LeetCode 经典题库2958. 最多 K 个重复元素的最长子数组长度
    """
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


def majority_frequency_group(s: str) -> str:
    """
    LeetCode 经典题库3692. 众数频率字符
    如果题目限定 s 只有 a-z; 可使用counts[ord(char) - 97] += 1统计频率
    """
    if not s:
        raise ValueError("输入字段s为空")
    char_cnt: dict[str, int] = {}
    for char in s:
        char_cnt[char] = char_cnt.get(char, 0) + 1

    frep_map: dict[int, list[str]] = {}
    max_group_size = 0
    best_freq = 0
    for char, freq in char_cnt.items():
        if freq in frep_map:
            frep_map[freq].append(char)
        else:
            frep_map[freq] = [char]
            # if len(frep_map[freq]) > 1:
        if len(frep_map[freq]) > max_group_size:
            max_group_size = len(frep_map[freq])
            best_freq = freq
        elif len(frep_map[freq]) == max_group_size:
            best_freq = max(best_freq, freq)
    return "".join(frep_map[best_freq])


@timer
def count_distinct(n: int) -> int:
    """
    LeetCode 经典题库3747. 统计移除零后不同整数的数目
    归纳总结
    设 n 的十进制长度为 m。
    对于长为 1,2,…,m−1 的不含 0 整数，每一位 1 到 9 可以随便填，所以长为 k 的不含 0 整数有 9
    k个。
    """
    if n < 10:
        return n
    no_zero_cnt = 9
    ind = 0
    for i in range(10, n + 1):
        remainder = i // (10**ind) % 10
        ind_cnt = ind
        head = i // 10**ind_cnt
        while remainder:
            if not head:
                break
            ind_cnt += 1
            remainder = head % 10
            head = i // (10**ind_cnt)
        if remainder:
            if not head:
                no_zero_cnt += 1
            else:
                ind = max(ind, ind_cnt)
    return no_zero_cnt


@timer
def countDistinct(n: int) -> int:
    """
    LeetCode 经典题库3747. 统计移除零后不同整数的数目
    """
    s = str(n)
    m = len(s)

    # 计算长度小于 m 的不含 0 的整数个数
    # 9^1 + 9^2 + ... + 9^(m-1) = (9^m - 9) / 8
    pow9 = 9**m
    ans = (pow9 - 9) // 8

    # 计算长度恰好等于 m 的不含 0 的整数个数
    for i, d in enumerate(s):
        if d == "0":  # 只能填 0，不合法，跳出循环
            break
        # 这一位填 1 到 d-1，后面的数位可以随便填 1 到 9
        v = int(d) - 1
        if i == m - 1:
            v += 1  # 最低位可以等于 d
        pow9 //= 9
        ans += v * pow9
        # 然后，这一位填 d，继续遍历

    return ans


if __name__ == "__main__":
    # rv = find_median_in_two_arrays(array1=[1, 3], array2=[2])
    # print(rv)
    nodes_list = []
    listss = [[1, 4, 5], [1, 3, 4], [2, 6]]
    for lst in listss:
        nodes_list.append(convert_list_to_link_list(lst))
    res = merge_k_list_min_heap(nodes_list)
    while res is not None:
        print(res.val)
        res = res.next
