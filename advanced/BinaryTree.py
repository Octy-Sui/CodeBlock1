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
        self.root = None
        self._length = 0

    def __len__(self):
        return self._length

    def is_empty(self):
        return len(self) == 0

    def _create_tree(self, list_nodes):
        if list_nodes is None or len(list_nodes) == 0:
            return None
        data = list_nodes.pop(0)
        if data is None:
            return None
        node = TreeNode(data)
        self._length += 1
        node.left = self._create_tree(list_nodes)
        node.right = self._create_tree(list_nodes)
        return node

    def create_tree(self, list_node=None):
        self.root = self._create_tree(list_node)

    def _pre_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            result.append(tree_node.data)
            self._pre_order_traverse(tree_node.left, result)
            self._pre_order_traverse(tree_node.right, result)

    def pre_order_traverse(self):
        rv = []
        self._pre_order_traverse(self.root, rv)
        print(rv)

    def PreOrderTraverse(self):
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

    def _mid_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            self._mid_order_traverse(tree_node.left, result)
            result.append(tree_node.data)
            self._mid_order_traverse(tree_node.right, result)

    def mid_order_traverse(self):
        rv = []
        self._mid_order_traverse(self.root, rv)
        print(rv)

    def MidOrderTraverse(self):
        rv = []
        stack = Stack()
        cursor = self.root
        while cursor is not None or not stack.is_empty():
            while cursor is not None:
                stack.push(cursor)
                cursor = cursor.left
            cursor = stack.pop()
            rv.append(cursor.data)
            cursor = cursor.right
            # if not stack.is_empty():
            #     cursor = stack.pop()
            #     if cursor is not None:
            #         rv.append(cursor.data)
            #     cursor = cursor.right
        print(rv)

    def _post_order_traverse(self, tree_node, result):
        if tree_node is None:
            return
        else:
            self._post_order_traverse(tree_node.left, result)
            self._post_order_traverse(tree_node.right, result)
            result.append(tree_node.data)

    def post_order_traverse(self):
        rv = []
        self._post_order_traverse(self.root, rv)
        print(rv)

    def PostOrderTraverse(self):
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

    def LevelOrderTraverse(self):
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


class BinHeap(BinTree):
    """
    二叉堆：
    存储方式为顺序 存储
    类别：最大堆，最小堆
    最大堆：父节点的值大于或等于左右孩子节点的数值；
    最小堆：父节点的值小于或等于左右孩子节点的数值；
    """
    def __init__(self):
        super(BinHeap, self).__init__()


if __name__ == '__main__':
    input_data = [3, 2, 9, None, None, 10, None, None, 8, None, 4]
    obj = BinTree()
    obj.create_tree(input_data)
    print(len(obj))
    obj.pre_order_traverse()
    obj.mid_order_traverse()
    obj.post_order_traverse()
    obj.PreOrderTraverse()
    obj.MidOrderTraverse()
    obj.PostOrderTraverse()
    obj.LevelOrderTraverse()
