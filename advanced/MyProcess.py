#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/12 12:02 下午
# @Author  : octy

import json
import logging as log
import multiprocessing
import os
import random
import time

import requests

from config.logger import logRecorder


def function_process(name, num=2):
    log.info("Function Process name:" + name)
    log.info("ProcessID".format(os.getpid()))
    log.info("output number is {}".format(num + random.random()))


class MyProcess(multiprocessing.Process):

    def __init__(self, name):
        super(MyProcess, self).__init__()
        self.name = name
        log.info("Class Process name:" + self.name)

    def run(self):
        log.info("ProcessID".format(os.getpid()))


def process_usage():
    # 创建进程
    # 直接调用
    function_process1 = multiprocessing.Process(target=function_process, args=("function_process1", 5))
    # 继承式调用
    class_process1 = MyProcess("class_process1")
    # 守护进程
    """
    主进程创建守护进程
    1）守护进程会在主进程代码执行结束后就终止
    2）守护进程内无法再开启子进程,否则抛出异常：AssertionError: daemonic processes are not allowed to have children
    注意：进程之间是互相独立的，主进程代码运行结束，守护进程随即终止
    """
    protected_process1 = MyProcess("protected_process1")
    protected_process1.daemon = True

    # 启动进程
    function_process1.start()
    class_process1.start()
    protected_process1.start()
    # protected_process1.join()  # 主进程等待子进程


"""
        进程同步(锁)
进程之间数据不共享,但是共享同一套文件系统,所以访问同一个文件,或同一个打印终端,是没有问题的,
而共享带来的是竞争，竞争带来的结果就是错乱，如何控制，就是加锁处理。
"""


class TicketsBuyer(multiprocessing.Process):

    def __init__(self, name, locker):
        super(TicketsBuyer, self).__init__()
        self.name = name
        self.locker = locker
        log.info("ProcessID".format(os.getpid()))
        log.info("customer name:" + self.name)

    def query(self):
        dic = json.load(open('db.txt'))
        log.info('剩余票数:{}'.format(dic['count']))

    def order(self):
        dic = json.load(open('db.txt'))
        time.sleep(random.random())  # 模拟读数据的网络延迟
        if dic['count'] > 0:
            dic['count'] -= 1
            time.sleep(random.random())  # 模拟写数据的网络延迟
            json.dump(dic, open('db.txt', 'w'))
            log.info('{}购票成功, 剩余票数:{}'.format(self.name, dic['count']))
        else:
            log.info("{}购票失败，余票数量为{}".format(self.name, dic['count']))

    def run(self):

        self.query()
        self.locker.acquire()
        self.order()
        self.locker.release()


def lock_usage():
    locker = multiprocessing.Lock()
    for num in range(21):
        customer_name = "process_lock{}".format(num)
        pro = TicketsBuyer(customer_name, locker)
        pro.start()


"""
进程间通信
虽然可以用文件共享数据实现进程间通信，但问题是：
1）效率低（共享数据基于文件，而文件是硬盘上的数据） 2）需要自己加锁处理
因此我们最好找寻一种解决方案能够兼顾：1）效率高（多个进程共享一块内存的数据）2）帮我们处理好锁问题。
mutiprocessing模块为我们提供的基于消息的IPC通信机制：队列和管道。
1. 队列和管道都是将数据存放于内存中
2. 队列又是基于（管道+锁）实现的，可以让我们从复杂的锁问题中解脱出来， 我们应该尽量避免使用共享数据，
   尽可能使用消息传递和队列，避免处理复杂的同步和锁问题，而且在进程数目增多时，往往可以获得更好的可获展性
"""

"""
生产者消费者模式
生产者消费者模式是通过一个容器来解决生产者和消费者的强耦合问题。
生产者和消费者彼此之间不直接通讯，而通过阻塞队列来进行通讯。
生产者生产完数据之后不用等待消费者处理，直接扔给阻塞队列，消费者不找生产者要数据，而是直接从阻塞队列里取。
阻塞队列就相当于一个缓冲区，平衡了生产者和消费者的处理能力。
"""


def consumer(queue, name):
    log.info(" Consumer {} ProcessID:{}".format(name, os.getpid()))
    while True:
        food = queue.get()
        if food is None:
            log.info("Had a great meal.Thanks!")
            break
        log.info("{} gets {}".format(name, food))
        time.sleep(random.randint(1, 3))
        log.info("{} ate {}".format(name, food))


def producer(queue, name):
    log.info("Producer {} ProcessID:{}".format(name, os.getpid()))
    menu = ["蒸羊羔", "蒸熊掌", "蒸鹿尾儿", "烧花鸭", "烧雏鸡", "烧子鹅", "卤猪", "卤鸭", "酱鸡", "腊肉", "松花", "小肚儿",
            "晾肉", "香肠", "什锦苏盘", ]
    for food in menu:
        time.sleep(random.randint(1, 3))
        queue.put(food)
        log.info("{} have made {}".format(name, food))
    queue.put(None)
    log.info("Producer have made all food.")


def queue_usage():
    """
    Queue队列（底层是以管道和锁定的方式实现)
    JoinableQueue()
    :return:
    """
    queue = multiprocessing.Queue()
    # 生产者们:即厨师们
    producer_name = "producer01"
    producer1 = multiprocessing.Process(target=producer, args=(queue, producer_name))

    # 消费者们:即吃货们
    consumer_name = "consumer01"
    consumer1 = multiprocessing.Process(target=consumer, args=(queue, consumer_name))

    # 开始
    producer1.start()
    consumer1.start()


"""
管道
Pipe([duplex]):在进程之间创建一条管道，并返回元组（conn1,conn2）,其中conn1，conn2表示管道两端的连接对象，
强调一点：必须在产生Process对象之前产生管道.
参数介绍：duplex:默认管道是全双工的，如果将duplex射成False，conn1只能用于接收，conn2只能用于发送。
"""


def receiver(pipe, name):
    left, right = pipe
    left.close()
    while True:
        try:
            num = right.recv()
            log.info("{} receive number {}".format(name, num))
        except EOFError:
            right.close()
            break


def sender(pipe):
    left, right = pipe
    right.close()
    for i in range(10):
        time.sleep(random.random())
        left.send(i)
        log.info("Send {} to pipe".format(i))
    else:
        left.close()


"""
注意：生产者和消费者都没有使用管道的某个端点，就应该将其关闭，如在生产者中关闭管道的右端，在消费者中关闭管道的左端。
如果忘记执行这些步骤，程序可能再消费者中的recv()操作上挂起。
管道是由操作系统进行引用计数的,必须在所有进程中关闭管道后才能生产EOFError异常。
因此在生产者中关闭管道不会有任何效果，付费消费者中也关闭了相同的管道端点。
管道可以用于双向通信，利用通常在客户端/服务器中使用的请求／响应模型或远程过程调用，就可以使用管道编写与进程交互的程序
"""


def pipe_usage():
    left, right = multiprocessing.Pipe()

    consumer1 = multiprocessing.Process(target=receiver, args=((left, right), 'consumer1'))
    consumer1.start()

    sender((left, right))

    right.close()
    left.close()

    consumer1.join()


"""
共享数据
展望未来，基于消息传递的并发编程是大势所趋
即便是使用线程，推荐做法也是将程序设计为大量独立的线程集合
通过消息队列交换数据。这样极大地减少了对使用锁定和其他同步手段的需求，
还可以扩展到分布式系统中.
进程间通信应该尽量避免使用本节所讲的共享数据的方式
进程间数据是独立的，可以借助于队列或管道实现通信，二者都是基于消息传递的
虽然进程间数据独立，但可以通过Manager实现数据共享
"""


def work(d, locker):
    with locker:  # 不加锁而操作共享的数据,肯定会出现数据错乱
        d['count'] -= 1


def manager_usage():
    lock = multiprocessing.Lock()
    with multiprocessing.Manager() as mag:
        info = mag.dict({'count': 111})
        process_list = []
        for i in range(100):
            process = multiprocessing.Process(target=work, args=(info, lock))
            process_list.append(process)
            process.start()
            process.join()
        log.info(info)


"""
信号量及事件同线程一样
"""

"""
进程池
在利用Python进行系统管理的时候，特别是同时操作多个文件目录，或者远程控制多台主机，并行操作可以节约大量的时间。
多进程是实现并发的手段之一，需要注意的问题是：
1）很明显需要并发执行的任务通常要远大于核数
2）一个操作系统不可能无限开启进程，通常有几个核就开几个进程
3）进程开启过多，效率反而会下降（开启进程是需要占用系统资源的，而且开启多余核数目的进程也无法做到并行）

例如当被操作对象数目不大时，可以直接利用multiprocessing中的Process动态成生多个进程，十几个还好，
但如果是上百个，上千个。。。手动的去限制进程数量却又太过繁琐，此时可以发挥进程池的功效。
我们就可以通过维护一个进程池来控制进程数目，比如httpd的进程模式，规定最小进程数和最大进程数... 
对于远程过程调用的高级应用程序而言，应该使用进程池，Pool可以提供指定数量的进程，供用户调用。
当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；
但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，就重用进程池中的进程。

创建进程池的类：如果指定numprocess为3，则进程池会从无到有创建三个进程，然后自始至终使用这三个进程去执行所有任务，不会开启其他进程
Pool([numprocess  [,initializer [, initargs]]]):创建进程池
参数介绍：
1. numprocess:要创建的进程数，如果省略，将默认使用cpu_count()的值
2. initializer：是每个工作进程启动时要执行的可调用对象，默认为None
3. initargs：是要传给initializer的参数组
"""


def calc(num, name):
    time.sleep(random.random())
    tmp = num ** 2
    log.info("the square of {} is {}, in Process {} {}".format(num, tmp, name, os.getpid()))
    return tmp


def pool_usage():
    # 进程池中从无到有创建四个进程,以后一直是这四个进程在执行任务
    pool = multiprocessing.Pool(4)
    result_list = []
    # 同步调用，直到本次任务执行完毕拿到res，等待任务work执行的过程中可能有阻塞也可能没有阻塞;
    # 但不管该任务是否存在阻塞，同步调用都会在原地等着，只是等的过程中若是任务发生了阻塞就会被夺走cpu的执行权限
    for i in range(10):
        rv = pool.apply(calc, args=(i, "sync"))
        # 同步执行，即执行完一个拿到结果，再去执行另外一个
        result_list.append(rv)
    log.info(result_list)

    # 异步apply_async用法：如果使用异步提交的任务，主进程需要使用join，等待进程池内任务都处理完，然后可以用get收集结果;
    # 否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了

    result_async = []
    for i in range(10):
        rv = pool.apply_async(calc, args=(i, "async"))  # 同步运行,阻塞、直到本次任务执行完毕拿到res
        result_async.append(rv)
    # 没有后面的join，或get，则程序整体结束，进程池中的任务还没来得及全部执行完也都跟着主进程一起结束了
    # 关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
    pool.close()
    # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    pool.join()
    for res in result_async:
        # 使用get来获取apply_async的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
        log.info("The result is {}".format(res.get()))


"""
回掉函数：
需要回调函数的场景：进程池中任何一个任务一旦处理完了，就立即告知主进程：任务结束，可以处理我的结果了。
主进程则调用一个函数去处理该结果，该函数即回调函数。
我们可以把耗时间（阻塞）的任务放到进程池中，然后指定回调函数（#主进程负责执行#）；
这样主进程在执行回调函数时就省去了I/O的过程，直接拿到的是任务的结果。

如果在主进程中等待进程池中所有任务都执行完毕后，再统一处理结果，则无需回调函数
"""


def get_page(url):
    log.info("Process {} get {}".format(os.getpid(), url))
    response = requests.get(url)
    if response.status_code == 200:
        log.info("Got the result of " + url)
        rv = response.text
    else:
        log.error("Not get the complete web content, the status code of web is {}".format(response.status_code))
        rv = "Not get the web content."
    return {'url': url, 'status_code': response.status_code, 'text': rv}


def parse_page(res):
    log.info("Process {} parse {}".format(os.getpid(), res["url"]))
    parse_res = 'url:<%s> size:[%s]\n' % (res['url'], len(res['text']))
    with open('web_db.txt', 'a') as f:
        f.write(parse_res)


def callback_function_usage():
    urls = [
        'https://www.baidu.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://help.github.com/',
        'http://www.sia.com.cn/'
    ]

    pool = multiprocessing.Pool(4)
    result_list = []
    for url in urls:
        rv = pool.apply_async(get_page, args=(url,), callback=parse_page)
        result_list.append(rv)

    pool.close()
    pool.join()
    # 拿到的是get_page的结果,其实完全没必要拿该结果,该结果已经传给回调函数处理了
    log.info([res.get()["status_code"] for res in result_list])


"""
学习内容来自
https://www.cnblogs.com/jiangfan95/p/11439207.html
"""


def main():
    log.info("Main process starts.")
    callback_function_usage()
    log.info("Main process end.")


if __name__ == '__main__':
    logRecorder()
    main()
