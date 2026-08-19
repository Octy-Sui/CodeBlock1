# @Time    :2021/6/15 9:57 下午
# @Author  : octy


def count_character_in_str_without_repeat(string):
    """
    统计给定字符中每个字符出现次数
    解决方案：
    遍历+哈希表
    时间复杂度: O(n), 空间复杂度: O(n)
    """
    tmp = {}
    for s in string:
        if s in tmp:
            tmp[s] = tmp[s] + 1
        else:
            tmp[s] = 1
    return tmp


if __name__ == "__main__":
    print("hello")
