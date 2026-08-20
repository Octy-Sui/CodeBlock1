# @Time    :2021/7/24 4:56 下午
# @Author  : octy


class ListNode:
    """Represents a singly linked node."""

    def __init__(self, _data, _next=None):
        self.val: int = _data
        self.next: None | ListNode = _next

    def __lt__(self, other: "ListNode") -> bool:
        return self.val < other.val


class DoubleWayNode(ListNode):
    def __init__(self, _data, _previous=None, _next=None):
        super().__init__(_data, _next)
        self.previous = _previous


class SingleLinkList:
    def __init__(self):
        self._size = 0
        self.head: None | ListNode = None

    def __len__(self):
        return self._size

    def __iter__(self):
        cursor = self.head
        while cursor is not None:
            yield cursor
            cursor = cursor.next

    def __str__(self):
        rv = "Current Link Node elements:"
        for item in self:
            rv += f"{item.data} "
        return rv

    def is_empty(self):
        return len(self) == 0

    def clear(self):
        self.head = None
        self._size = 0

    def add(self, node: ListNode):
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, node):
        probe = self.head
        if probe is None:
            raise ValueError("self.head is None")
        if self.is_empty():
            self.add(node)
        else:
            while probe.next is not None:
                probe = probe.next
            probe.next = node
            self._size += 1

    def insert(self, node, index):
        while index > len(self) + 1 or index <= 0:
            print("你要插入的位置不对，请重选位置:")
            index = eval(input())
        if index == 1:
            self.add(node)
        else:
            probe = self.head
            if probe is None:
                raise ValueError("self.head is None")
            count = 1
            for item in self:
                count += 1
                if count == index:
                    node.next = item.next
                    probe.next = node
                    break
                probe = item
            self._size += 1

    def travel(self):
        print(str(self))

    def sort(self):
        for i in range(self._size - 1):
            probe = self.head
            for _ in range(self._size - i - 1):
                if probe is None or probe.next is None:
                    raise ValueError("self.head is None")
                if probe.val > probe.next.val:
                    temp = probe.val
                    probe.val = probe.next.val
                    probe.next.val = temp
                probe = probe.next

    def delete(self, index):
        if index <= 0 or index > self._size:
            while index <= 0 or index > self._size:
                print("你输入的下标不对，请重新输入需要删除的值的下标：")
                index = eval(input())
            #   return
        else:
            if index == 1:
                if self.head is None:
                    raise ValueError("self.head is None")
                self.head = self.head.next
                probe = self.head
            elif index == 2:
                probe = self.head
                if probe is None or probe.next is None:
                    raise ValueError("self.head is None")
                probe.next = probe.next.next
            else:
                probe = self.head
                for _ in range(1, index - 1):
                    if probe is None or probe.next is None:
                        raise ValueError("self.head is None")
                    probe = probe.next
                if probe is None or probe.next is None:
                    raise ValueError("self.head is None")
                probe.next = probe.next.next
        self._size -= 1

    def is_contain(self, num):
        contain = 0
        probe = self.head
        for i in range(self._size):
            if probe is None:
                raise ValueError("self.head is None")
            if probe.val == num:
                print(
                    f"{num}在链表中{i + 1}处"
                )  # i+1是在正常人认为的位置处，程序员一般是从0开始算起
                contain = 1
            probe = probe.next
        if contain == 0:
            print(f"{num}不在链表中")

    def search(self, index):
        probe = self.head
        if index <= 0 or index > self._size:
            while index <= 0 or index > self._size:
                print("你输入的下标不对，请重新输入:")
                index = eval(input())
        if index > 0 or index <= self._size:
            for i in range(index - 1):
                if probe is None or probe.next is None:
                    raise ValueError("self.head is None")
                probe = probe.next
            return probe

    def alert(self, index, num):  # index定义为下标
        probe = self.head
        if index <= 0 or index > self._size:
            print("你输入的下标不对，请重新输入!\n")
        else:
            for i in range(index - 1):
                if probe is None or probe.next is None:
                    raise ValueError("self.head is None")
                probe = probe.next
            if probe is None:
                raise ValueError("self.head is None")
            probe.val = num


def main():
    # 创建一个单链表对象
    single_link_list = SingleLinkList()  # 实例化

    print("""
          **********************************************************************************************************************
          **********************************************请选择相应的序号完成相应的操作********************************************
          **********************************************************************************************************************
          **         0、结束所有操作！！！！！！                                                                               ***
          **         1、验证链表里面有没有值！                                                                                 ***
          **         2、从头部插入数值！                                                                                       ***
          **         3、从尾部插入数值！                                                                                       ***
          **         4、按指定位置插入数值！                                                                                   ***
          **         5、删除操作！                                                                                            ***
          **         6、查找一个节点是否在链表中！                                                                             ***
          **         7、按下标查找节点处的数值！                                                                               ***
          **         8、给链表排序！                                                                                          ***
          **         9、修改！                                                                                                ***
          **********************************************************************************************************************
          """)
    while True:
        number = eval(input("——————输入下一步要进行的相应操作序号——————："))
        if number == 1:
            print("正在验证链表里面有没有值：")
            single_link_list.travel()
            print("\n")

        if number == 2:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在从头部插入数值：")
            node1 = ListNode(eval(input("输入要插入的值:")))  # 从头部插入数值
            single_link_list.add(node1)
            print("操作后链表的状态。")
            single_link_list.travel()

        if number == 3:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在尾部插入数值：")
            node2 = ListNode(eval(input("输入要插入的值:")))
            single_link_list.append(node2)
            print("操作后链表的状态。")
            single_link_list.travel()

        if number == 4:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在按指定位置插入数值：")
            node3 = ListNode(eval(input("输入插入的数：")))
            position = eval(input("输入要插入到的位置为："))
            single_link_list.insert(node3, position)
            print("操作后链表的状态。")
            single_link_list.travel()

        if number == 5:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在删除：")
            single_link_list.delete(eval(input("输入要删除哪个位置的数：")))
            print("操作后链表的状态。")
            single_link_list.travel()

        if number == 6:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在查找一个节点是否在链表中：")
            single_link_list.is_contain(eval(input("输入要验证的数：")))

        if number == 7:
            print("正在按下标查找节点处的数值：")
            node = single_link_list.search(
                eval(input("输入下标值："))
            )  # 查找某节点处的值
            print(f"这个位置的值为：{node.data}")

        if number == 8:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在排序：")
            single_link_list.sort()
            print("操作后链表的状态。")
            single_link_list.travel()

        if number == 9:
            print("目前的链表状态。")
            single_link_list.travel()
            print("正在修改（这是在上面排序后的前提下修改。）：")
            index = eval(input("输入要修改的得位置："))  # 修改的下角标
            num = eval(input("输入要修改为的数："))  # 要修改成的那个数
            single_link_list.alert(index, num)
            print("操作后链表的状态。")
            single_link_list.travel()  # 遍历一遍

        if number == 0:
            print("操作已退出.")
            break


def convert_list_to_link_list(items: list) -> None | ListNode:
    head: None | ListNode = None
    for item in items:
        if head is None:
            head = ListNode(item)
            cursor = head
        else:
            cursor.next = ListNode(item)
            cursor = cursor.next
    return head


if __name__ == "__main__":
    main()
