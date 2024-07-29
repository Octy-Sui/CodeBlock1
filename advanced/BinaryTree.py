#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/25 10:03 下午
# @Author  : octy

from advanced.DataStructure import Stack, Queue


class TreeNode(object):

    def __init__(self, _data, _left=None, _right=None):
        self.left = _left
        self.data = _data
        self.right = _right


class RBTreeNode(TreeNode):

    def __init__(self, _data, _left=None, _right=None):
        super(RBTreeNode, self).__init__(_data, _left, _right)
        self.color = "black"
        self.parent = None


def convert_array_to_bst_traversal(nums_list):
    if nums_list is None or len(nums_list) == 0:
        return None
    mid = len(nums_list) // 2
    root = TreeNode(nums_list[mid])
    root.left = convert_array_to_bst_traversal(nums_list[:mid])
    root.right = convert_array_to_bst_traversal(nums_list[mid + 1:])
    return root


def convert_array_to_bst_with_stack(nums_list):
    if nums_list is None or len(nums_list) == 0:
        return None
    stack = Stack()
    # Initialize the root node and stack
    len_nums_list = len(nums_list)
    mid = (len_nums_list - 1) // 2
    root = TreeNode(nums_list[mid])
    stack.push((root, 0, len_nums_list - 1))

    while not stack.is_empty():
        node, left, right = stack.pop()
        mid = (left + right) // 2

        if left <= mid - 1:
            mid_left = (left + mid - 1) // 2
            node.left = TreeNode(nums_list[mid_left])
            stack.push((node.left, left, mid - 1))

        if mid + 1 <= right:
            mid_right = (mid + 1 + right) // 2
            node.right = TreeNode(nums_list[mid_right])
            stack.push((node.right, mid + 1, right))

    return root


"""
二叉树：
物理结构存储：链表，数组
链表如TreeNode数据结构存储即可；
数组，
        R0
       /  \
     R1    R2
    / \   /  \
   R3 R4 R5  R6
Array中位置：0  1  2  3  4  5  6 
            R0,R1,R2,R3,R4,R5,R6
父节点index：parent
左孩子index：parent*2 + 1
右孩子index：parent*2 + 2
"""


class BinTree(object):

    def __init__(self):
        self.root: TreeNode = None
        self._length = 0

    def __len__(self):
        return self._length

    def add(self, data):
        insert_node = TreeNode(data)
        if not self.root:
            self.root = insert_node
            self._length += 1
            return
        cursor = self.root
        while cursor.data != data:  # return if the value is already in the tree
            if data < cursor.data:
                if cursor.left:
                    cursor = cursor.left
                else:
                    cursor.left = insert_node
                    self._length += 1
                    break
            else:
                if cursor.right:
                    cursor = cursor.right
                else:
                    cursor.right = insert_node
                    self._length += 1
                    break

    def delete(self, data):
        parent = None
        cursor = self.root

        # Find the node to delete and its parent
        while cursor and cursor.data != data:
            parent = cursor
            if data < cursor.data:
                cursor = cursor.left
            else:
                cursor = cursor.right
        if not cursor:
            return  # Value not found in the tree

        # Case 1: Node to be deleted has no children (it's a leaf node)
        if not cursor.left and not cursor.right:
            if not parent:  # Root node
                self.root = None
            elif parent.left == cursor:
                parent.left = None
            else:
                parent.right = None

        # Case 2: Node to be deleted has only one child
        elif not cursor.left or not cursor.right:
            child = cursor.left if cursor.left else cursor.right
            if not parent:  # Root node
                self.root = child
            elif parent.left == cursor:
                parent.left = child
            else:
                parent.right = child

        # Case 3: Node to be deleted has two children
        else:
            # Find the in-order successor (smallest node in the right subtree: because left < root < right in bst)
            successor_parent = cursor
            successor = cursor.right
            while successor.left:
                successor_parent = successor
                successor = successor.left

            # Replace current node's value with the successor's value
            cursor.data = successor.data

            # Delete the successor node
            # successor's right child is the left child of successor's parent
            # because left < root < right in bst; above is true, so successor.left is None
            # but successor.right would be None or have a data value
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right

    def remove(self, data):
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node, data):
        if not node:
            return node

        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            min_larger_node = self._get_min(node.right)
            node.data = min_larger_node.data
            node.right = self._delete_recursive(node.right, min_larger_node.data)

        return node

    @staticmethod
    def _get_min(node):
        current = node
        while current.left:
            current = current.left
        return current

    def is_empty(self):
        return len(self) == 0

    def _convert_array_to_bst_traversal(self, sorted_array):
        if sorted_array is None or len(sorted_array) == 0:
            return None
        mid = len(sorted_array) // 2
        root = TreeNode(sorted_array[mid])
        root.left = self._convert_array_to_bst_traversal(sorted_array[:mid])
        root.right = self._convert_array_to_bst_traversal(sorted_array[mid + 1:])
        return root

    def create_tree_from_array(self, sorted_array=None):
        self.root = self._convert_array_to_bst_traversal(sorted_array)

    def _pre_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            result.append(tree_node.data)
            self._pre_order_traverse(tree_node.left, result)
            self._pre_order_traverse(tree_node.right, result)

    def pre_order_traversal(self):
        rv = []
        self._pre_order_traverse(self.root, rv)
        print(rv)

    def preorder_with_stack(self):
        rv = []
        stack = Stack()
        cursor = self.root
        while cursor is not None or not stack.is_empty():
            while cursor is not None:
                rv.append(cursor.data)
                stack.push(cursor)
                cursor = cursor.left
            cursor = stack.pop()
            cursor = cursor.right
        print(rv)

    def preorder_with_stack_v2(self):
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            cursor = stack.pop()
            if cursor is None:
                continue
            yield cursor.data
            stack.push(cursor.right)
            stack.push(cursor.left)

    def _mid_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            self._mid_order_traverse(tree_node.left, result)
            result.append(tree_node.data)
            self._mid_order_traverse(tree_node.right, result)

    def mid_order_traversal(self):
        rv = []
        self._mid_order_traverse(self.root, rv)
        print(rv)

    def inorder_with_stack(self):
        stack = Stack()
        cursor = self.root
        while cursor is not None or not stack.is_empty():
            while cursor is not None:
                stack.push(cursor)
                cursor = cursor.left
            cursor = stack.pop()
            yield cursor.data
            cursor = cursor.right

    def _post_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            self._post_order_traverse(tree_node.left, result)
            self._post_order_traverse(tree_node.right, result)
            result.append(tree_node.data)

    def post_order_traversal(self):
        rv = []
        self._post_order_traverse(self.root, rv)
        print(rv)

    def postorder_with_stack(self):
        if self.root is None:
            print([])
            return
        rv = []
        stack1 = Stack([self.root])
        stack2 = Stack()
        while not stack1.is_empty():
            cursor = stack1.pop()
            stack2.push(cursor)
            if cursor.left is not None:
                stack1.push(cursor.left)
            if cursor.right is not None:
                stack1.push(cursor.right)
        for item in stack2:
            rv.append(item.data)
        print(rv)

    def postorder_with_stack_v2(self):
        """
        后序遍历（Postorder Traversal）的顺序是“左-右-根”，即先遍历左子树，然后遍历右子树，最后访问根节点。
        第一次遍历，类似前序遍历，但将节点值先放入output; 第二次遍历，反转output，得到正确的后序遍历顺序
        """
        stack = Stack()
        output = []
        stack.push(self.root)
        while not stack.is_empty():
            cursor = stack.pop()
            if cursor is None:
                continue
            output.append(cursor.data)
            stack.push(cursor.left)
            stack.push(cursor.right)
        for item in reversed(output):
            yield item

    def level_order_with_stack(self):
        rv = []
        my_queue = Queue()
        cursor = self.root
        my_queue.put(cursor)
        while not my_queue.is_empty():
            cursor = my_queue.get()
            if cursor is not None:
                rv.append(cursor.data)
            else:
                continue
            my_queue.put(cursor.left)
            my_queue.put(cursor.right)
        print(rv)

    def print_tree(self):
        my_queue = Queue()
        cursor = self.root
        my_queue.put([cursor])
        while not my_queue.is_empty():
            level = []
            level_nodes = my_queue.get()
            for cursor in level_nodes:
                if cursor is not None:
                    print(cursor.data, end=' ')
                else:
                    continue
                level.append(cursor.left)
                level.append(cursor.right)
            print("\n")
            if not level:
                break
            my_queue.put(level)

    def left_rotate(self, node):
        if not node or not node.right:
            return node

        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def right_rotate(self, node):
        if not node or not node.left:
            return node

        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def rotate_left(self, root, data):
        if not root:
            return root

        if data < root.data:
            root.left = self.rotate_left(root.left, data)
        elif data > root.data:
            root.right = self.rotate_left(root.right, data)
        else:
            root = self.left_rotate(root)

        return root

    def rotate_right(self, root, data):
        if not root:
            return root

        if data < root.data:
            root.left = self.rotate_right(root.left, data)
        elif data > root.data:
            root.right = self.rotate_right(root.right, data)
        else:
            root = self.right_rotate(root)

        return root


from collections import deque


def print_tree_pretty(node):
    if node is None:
        return

    # 使用队列进行层次遍历
    queue = deque([(node, 0)])
    level_widths = {}

    while queue:
        current_node, level = queue.popleft()

        if level not in level_widths:
            level_widths[level] = []

        if current_node is None:
            level_widths[level].append(None)
        else:
            level_widths[level].append(current_node.data)
            queue.append((current_node.left, level + 1))
            queue.append((current_node.right, level + 1))

    # 打印每个层级
    for level, nodes in level_widths.items():
        print(' '.join(str(node).rjust(3) for node in nodes))


class BinSearchTree(BinTree):
    """
    二叉查找树条件：
    1.如果左子树不为空，则左子树上所有节点的值均小于根节点的值，
    1.如果右子树不为空，则右子树上所有节点的值均大于根节点的值，
    3.左、右子树也都是二叉查找树
    遍历方式：
    1.前序遍历：根节点、左节点、右节点
    2.中序遍历：左节点、根节点、右节点
    3.后序遍历：左节点、右节点、根节点
    4.层序遍历：借助队列方式遍历树
    """

    def __init__(self):
        super(BinSearchTree, self).__init__()


class MinHeap(BinTree):
    """
    二叉堆：
    存储方式为顺序 存储
    类别：最小堆
    最小堆：父节点的值小于或等于左右孩子节点的数值；
    """

    def __init__(self):
        super(MinHeap, self).__init__()

    @staticmethod
    def down_adjust(array, cursor, length):
        tmp = array[cursor]  # 暂存当前节点, 用于最后赋值
        child_cursor = 2 * cursor + 1
        while child_cursor < length:
            # 如果存在右节点，且右节点值小于左节点值；则定位至右节点
            if child_cursor + 1 < length and array[child_cursor] > array[child_cursor + 1]:
                child_cursor += 1
            # 如果当前节点小于等于子节点值，则退出
            if tmp <= array[child_cursor]:
                break
            # 如果当前节点大于子节点，则交换子节点值；同时继续下探
            array[cursor] = array[child_cursor]
            cursor = child_cursor
            child_cursor = 2 * cursor + 1
        array[cursor] = tmp

    @staticmethod
    def up_adjust(array):
        child_cursor = len(array) - 1
        tmp = array[child_cursor]
        parent_cursor = (child_cursor - 1) // 2
        while child_cursor > 0 and array[child_cursor] < array[parent_cursor]:
            array[child_cursor] = array[parent_cursor]
            child_cursor = parent_cursor
            parent_cursor = (child_cursor - 1) // 2
        array[child_cursor] = tmp

    @staticmethod
    def build_min_heap(array):
        for i in range(len(array) // 2 - 1, -1, -1):
            MinHeap.down_adjust(array, i, len(array))
        return array


class MaxHeap(BinTree):
    """
    二叉堆：
    存储方式为顺序 存储
    类别：最大堆
    最大堆：父节点的值大于或等于左右孩子节点的数值；
    """

    def __init__(self):
        super(MaxHeap, self).__init__()

    @staticmethod
    def down_adjust(array, cursor, length):
        tmp = array[cursor]  # 暂存当前节点, 用于最后赋值
        child_cursor = 2 * cursor + 1
        while child_cursor < length:
            # 如果存在右节点，且右节点值小于左节点值；则定位至右节点
            if child_cursor + 1 < length and array[child_cursor] < array[child_cursor + 1]:
                child_cursor += 1
            # 如果当前节点小于等于子节点值，则退出
            if tmp >= array[child_cursor]:
                break
            # 如果当前节点大于子节点，则交换子节点值；同时继续下探
            array[cursor] = array[child_cursor]
            cursor = child_cursor
            child_cursor = 2 * cursor + 1
        array[cursor] = tmp

    @staticmethod
    def up_adjust(array):
        child_cursor = len(array) - 1
        tmp = array[child_cursor]
        parent_cursor = (child_cursor - 1) // 2
        while child_cursor > 0 and array[child_cursor] > array[parent_cursor]:
            array[child_cursor] = array[parent_cursor]
            child_cursor = parent_cursor
            parent_cursor = (child_cursor - 1) // 2
        array[child_cursor] = tmp

    @staticmethod
    def build_max_heap(array):
        for i in range(len(array) // 2 - 1, -1, -1):
            MaxHeap.down_adjust(array, i, len(array))
        return array


if __name__ == '__main__':
    # input_data = [3, 2, 9, None, None, 10, None, None, 8, None, 4]
    # obj = BinTree()
    # obj.create_tree(input_data)
    # print(len(obj))
    bst = BinTree()
    # bst.root = convert_array_to_bst_with_stack([1, 4, 5, 6, 10, 11, 12, 14, 15])
    # for i in [1, 4, 2, 6, 10, 7, 13]:
    #     bst.add(i)
    input_array = [1, 4, 2, 6, 15, 10, 13, 21, 34]
    bst.create_tree_from_array(input_array)
    # print(bst.root.data)
    bst.preorder_with_stack()
    bst.post_order_traversal()
    print(list(bst.postorder_with_stack_v2()))
    print_tree_pretty(bst.root)
    print(MinHeap.build_min_heap(input_array))
    print(MaxHeap.build_max_heap(input_array))

