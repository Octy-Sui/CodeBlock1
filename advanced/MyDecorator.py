#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/13 9:59 下午
# @Author  : octy
import functools
import logging as log
import random
import time

import config.logger

"""
1. 装饰器（Decoration）:
    - 装饰器是一种设计模式，经常用来实现"面向切面的编程"(AOP: 实现在不修改源代码的情况下，给程序动态添加功能的一种技术)
    -简言之，python装饰器就是用于拓展原来函数功能的一种函数，这个函数的特殊之处在于它的返回值也是一个函数
    -使用python装饰器的好处就是在不用更改原函数的代码前提下给函数增加新的功能。
2. 装饰器的作用：
    - 装饰器允许向一个现有的对象(函数)添加新的功能，同时又不改变其结构
    - 可以抽离出大量的函数中的和业务无关的功能
3. 应用场景：
    - 插入日志、性能测试、事务处理、缓存、中间件、权限控制等
"""
"""
装饰器：
1. 关键字：@，在被修饰的函数的前一行加入
2. 本质：装饰器的本质就是一个函数
3. 原理：在调用被装饰的函数时，被装饰的函数体的代码并不会被直接执行。而是在调用被装饰的函数时，将该函数传递给装饰器
"""

"""
@functools.wraps(func)，python提供的装饰器。
它能把原函数的元信息拷贝到装饰器里面的func函数中。函数的元信息包括docstring、name、参数列表等等。
"""


def timer(func):
    log.info("Before timer wrapper.")

    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        log.info("Received Executor is " + func.__name__)
        log.info("Timer start")
        st = time.time()
        func(*args, **kwargs)
        elapsed = (time.time() - st) * 1000
        log.info("Cost time is %d ms" % elapsed)
        log.info("Timer end")

    log.info("After timer wrapper.")
    return timer_wrapper


def logger(func):
    log.info("Before logger wrapper.")

    @functools.wraps(func)
    def logger_wrapper(*args, **kwargs):
        log.info("Start to execute " + func.__name__)
        func(*args, **kwargs)
        log.info("End to execute " + func.__name__)

    log.info("After logger wrapper.")
    return logger_wrapper


class ClassDecorator:
    """
    装饰器不一定只能用函数来实现，也可以使用类来装饰，用法与函数装饰器区别不大，实质上是调用了类方法中__call__魔法方法.
    因为是直接传参func，没有闭包过程，函数的元信息没有丢失。
    """

    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self._login(*args, **kwargs)

    def _login(self, *args, **kwargs):
        log.info("Executor name is " + self.__func.__name__)
        log.info("Login client successfully.")
        self.__func(*args, **kwargs)
        log.info("Exit client.")


class Person:
    """
    内置装饰器
    """

    def __init__(self, name, age, num):
        self.__name = name
        self.__age = age
        self.__id = num

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, a):
        self.__age = a

    @staticmethod
    def self_description():
        """
        静态方法的使用场景：
        如果在方法中不需要访问任何实例方法和属性，纯粹地通过传入参数并返回数据的功能性方法，那么它就适合用静态方法来定义，
        它节省了实例化对象的开销成本，往往这种方法放在类外面的模块层作为一个函数存在也是没问题的，而放在类中，仅为这个类服务。
        :return:
        """
        log.info("This is a staticmethod.")

    @classmethod
    def create_id(cls, info_dict):
        """
        类方法的使用场景有：
        作为工厂方法创建实例对象，例如内置模块 datetime.date 类中就有大量使用类方法作为工厂方法，以此来创建date对象。
        :return:
        """
        return cls(info_dict["name"], info_dict["age"], info_dict["num"])


"""装饰器的外函数和内函数之间的语句是没有装饰到目标函数上,而是在装载装饰器时的附加操作。"""
"""
main是装载装饰器的过程，相当于执行了main=logger(timer(main))，
此时先执行timer(main)，将func指向函数main、并返回函数timer_wrapper;
然后执行logger(timer_wrapper),将func指向函数timer_wrapper、并返回函数logger_wrapper;
然后最后执行。
执行顺序：logger_wrapper->timer_wrapper->main
"""


@ClassDecorator
@logger
@timer
def main(name, content=None):
    log.info("The name of executor is " + name)
    tmp = 0
    for i in range(5):
        time.sleep(random.random())
    log.info("Try to print something:" + content)


if __name__ == "__main__":
    main("TestDecorator", content="Hello World")
