#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/7/24 2:44 下午
# @Author  : octy
import threading


class Singleton(object):

    _stance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._stance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance

