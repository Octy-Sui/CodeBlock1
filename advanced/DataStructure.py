#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/24 2:43 下午
# @Author  : octy
"""
Array, linked list, stack, queue
heap: binary tree, red black tree
"""

import array
import collections
import queue


class AbstractCollection(object):

    def __init__(self, source_collection=None):
        self._size = 0
        if source_collection:
            for item in source_collection:
                self.add(item)

    def __len__(self):
        return self._size

    def __add__(self, other):
        temp = type(self)(self)
        for item in other:
            temp.add(item)
        return temp

    def __eq__(self, other):
        if type(self) != type(other) or len(self) != len(other):
            return False
        other_iter = iter(other)
        for item in self:
            if item != next(other_iter):
                return False
        return True

    def is_empty(self):
        return len(self) == 0


class Stack(AbstractCollection):

    def __init__(self, source_collection=None):
        self._stack = collections.deque()
        super(Stack, self).__init__(source_collection)

    def __iter__(self):
        while not self.is_empty():
            yield self.pop()

    def add(self, item):
        self.push(item)

    def push(self, data):
        self._size += 1
        return self._stack.append(data)

    def pop(self):
        self._size -= 1
        return self._stack.pop()


class Queue(AbstractCollection):

    def __init__(self, source_collection=None):
        self._queue = collections.deque()
        super(Queue, self).__init__(source_collection)

    def __iter__(self):
        while not self.is_empty():
            yield self.get()

    def add(self, item):
        self.put(item)

    def put(self, data):
        self._size += 1
        return self._queue.append(data)

    def get(self):
        self._size -= 1
        return self._queue.popleft()


def MyArray():
    """
    使用时必须先指定array类型， 整型，字符；
    类似C++的数组

    :return:
    """
    array_er = array.ArrayType("i", [0, 1, 2, 3, 4])
    for i in range(5, 10):
        array_er.append(i)
    for j in range(10):
        rv = array_er[j]
        print(rv)


def MyStack():
    """
    deque 双向队列：以双向链表实现
    stack 栈： 后进先出

    :return:
    """
    deque = collections.deque()
    for i in range(10):
        tmp = "My stack data{}".format(i)
        deque.append(tmp)
    for j in range(10):
        rv = deque.pop()
        print(rv)


def MyDeque():
    """
    deque 双向队列：以双向链表实现
    queue 队列： 先进先出

    :return:
    """
    deque = collections.deque()
    for i in range(10):
        tmp = "My deque data{}".format(i)
        deque.append(tmp)
    for j in range(10):
        rv = deque.popleft()
        print(rv)


def MyQueue():
    """
    为线程间通信服务
    Queue模块中提供了同步的、线程安全的队列类.
    实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

    :return:
    """
    queuor = queue.Queue()
    for i in range(20):
        tmp = "My queue data{}".format(i)
        queuor.put(tmp)
    for j in range(20):
        rv = queuor.get()
        print(rv)


def tes_module():
    MyArray()
    MyDeque()
    MyStack()
    MyQueue()


if __name__ == '__main__':
    tes_module()
    obj = Stack([1,2,3,4])
    obj = obj + Stack([6, 7])
    for i in obj:
        print(i)
    obj = Queue([1,2,3,4])
    for i in obj:
        print(i)
