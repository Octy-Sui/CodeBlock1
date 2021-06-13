#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/12 12:02 下午
# @Author  : octy
import asyncio
import logging as log
import random
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor

from config.logger import logRecorder

'''
                                      python多线程详解
      什么是线程？
      线程也叫轻量级进程，是操作系统能够进行运算调度的最小单位，它被包涵在进程之中，是进程中的实际运作单位。
      线程自己不拥有系统资源，只拥有一点儿在运行中必不可少的资源，但它可与同属一个进程的其他线程共享进程所
      拥有的全部资源。一个线程可以创建和撤销另一个线程，同一个进程中的多个线程之间可以并发执行
'''

'''
    为什么要使用多线程？
    线程在程序中是独立的、并发的执行流。与分隔的进程相比，进程中线程之间的隔离程度要小，它们共享内存、文件句柄
    和其他进程应有的状态。
    因为线程的划分尺度小于进程，使得多线程程序的并发性高。进程在执行过程之中拥有独立的内存单元，而多个线程共享
    内存，从而极大的提升了程序的运行效率。
    线程比进程具有更高的性能，这是由于同一个进程中的线程都有共性，多个线程共享一个进程的虚拟空间。线程的共享环境
    包括进程代码段、进程的共有数据等，利用这些共享的数据，线程之间很容易实现通信。
    操作系统在创建进程时，必须为改进程分配独立的内存空间，并分配大量的相关资源，但创建线程则简单得多。因此，使用多线程
    来实现并发比使用多进程的性能高得要多。
'''

'''
    总结起来，使用多线程编程具有如下几个优点：
    1.进程之间不能共享内存，但线程之间共享内存非常容易。
    2.操作系统在创建进程时，需要为该进程重新分配系统资源，但创建线程的代价则小得多。
      因此使用多线程来实现多任务并发执行比使用多进程的效率高
    3.python语言内置了多线程功能支持，而不是单纯地作为底层操作系统的调度方式，从而简化了python的多线程编程。
'''
global_num = 100
num = 100


def function_thread(name):
    """
    普通创建方式
    :param name:
    :return:
    """
    log.info('thread name:' + name)
    '''
        多线程共享全局变量
        线程时进程的执行单元，进程时系统分配资源的最小执行单位，所以在同一个进程中的多线程是共享资源的
    '''
    global global_num
    global_num += 1
    log.info("the global_num is {}.".format(global_num))
    time.sleep(1)
    log.info(name + ' first sleep')
    time.sleep(1)
    log.info(name + ' second sleep')


class MyThread(threading.Thread):
    """
    自定义线程：继承threading.Thread来定义线程类，其本质是重构Thread类中的run方法
    """

    def __init__(self, name):
        super(MyThread, self).__init__()  # 重构run函数必须写
        self.name = name
        log.info('thread name:' + self.name)

    def run(self):
        log.info(self.name + " class thread works.")
        time.sleep(1)
        log.info(self.name + ' first sleep')
        time.sleep(1)
        log.info(self.name + ' second sleep')


def thread_usage():
    # 普通创建方式
    normal_thr1 = threading.Thread(target=function_thread, args=('normal_thr1',))
    # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    normal_thr2 = threading.Thread(target=function_thread, args=('normal_thr2',))
    # 线程类创建
    class_thr = MyThread("class_thr")
    # 守护线程
    # protected_thr = threading.Thread(target=function_thread, args=('protected_thr',))
    protected_thr = MyThread("protected_thr")
    """
    守护线程
    下面这个例子，这里使用setDaemon(True)把所有的子线程都变成了主线程的守护线程，
    因此当主线程结束后，子线程也会随之结束，所以当主线程结束后，整个程序就退出了。
    所谓’线程守护’，就是主线程不管该线程的执行情况，只要是其他子线程结束且主线程执行完毕，
    主线程都会关闭。也就是说:主线程不等待该守护线程的执行完再去关闭.
    """
    protected_thr.setDaemon(True)

    # 线程启动
    normal_thr1.start()
    normal_thr2.start()
    class_thr.start()
    time.sleep(3)
    protected_thr.start()

    """
    主线程等待子线程结束
    为了让守护线程执行结束之后，主线程再结束，我们可以使用join方法，让主线程等待子线程执行
    """
    # protected_thr.join()  # 设置主线程等待子线程结束


'''
        由于线程之间是进行随机调度，并且每个线程可能只执行n条执行之后，当多个线程同时修改同一条数据时可能会出现脏数据，
    所以出现了线程锁，即同一时刻允许一个线程执行操作。线程锁用于锁定资源，可以定义多个锁，像下面的代码，当需要独占
    某一个资源时，任何一个锁都可以锁定这个资源，就好比你用不同的锁都可以把这个相同的门锁住一样。
        由于线程之间是进行随机调度的，如果有多个线程同时操作一个对象，如果没有很好地保护该对象，会造成程序结果的不可预期，
    我们因此也称为“线程不安全”。
        为了防止上面情况的发生，就出现了互斥锁（Lock）
'''


def lock_worker(locker, name):
    log.info("thread name " + name)
    global num
    locker.acquire()
    temp = num
    sleep_time = random.random()
    log.info("{}'s sleep time is {}.".format(name, sleep_time))
    time.sleep(sleep_time)
    num = temp - 1
    log.info("{}'s num is {}.".format(name, num))
    locker.release()


def about_lock():
    locker = threading.Lock()  # auto add join() 设置主线程等待子线程结束
    thread_list = []
    for i in range(10, 100):
        name = "threading.Lock{}".format(i)
        p = threading.Thread(target=lock_worker, args=(locker, name))
        thread_list.append(p)
    for thread in thread_list:
        thread.start()
        thread.join()  # auto add lock()?


def about_RLock():
    """
    递归锁：RLcok类的用法和Lock类一模一样，但它支持嵌套，在多个锁没有释放的时候一般会使用RLock类
    :return:
    """
    locker = threading.RLock()
    for i in range(10, 100):
        name = "threading.RLock{}".format(i)
        thread = threading.Thread(target=lock_worker, args=(locker, name))
        thread.start()


'''
    信号量（BoundedSemaphore类）
    互斥锁同时只允许一个线程更改数据，而Semaphore是同时允许一定数量的线程更改数据，比如厕所有3个坑，
    那最多只允许3个人上厕所，后面的人只能等里面有人出来了才能再进去
'''


def about_semaphore():
    semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
    for i in range(21):
        name = "semaphore{}".format(i)
        t = threading.Thread(target=lock_worker, args=(semaphore, name))
        t.start()
    while threading.active_count() != 1:
        pass
    else:
        log.info('----------all threads done-----------')


'''
    python线程的事件用于主线程控制其他线程的执行，事件是一个简单的线程同步对象，其主要提供以下的几个方法：
        clear将flag设置为 False
        set将flag设置为 True
        is_set判断是否设置了flag
        wait会一直监听flag，如果没有检测到flag就一直处于阻塞状态
    事件处理的机制：全局定义了一个Flag，当Flag的值为False，那么event.wait()就会阻塞，当flag值为True，
    那么event.wait()便不再阻塞
'''
event = threading.Event()


def lighter():
    count = 0
    event.set()  # 初始者为绿灯
    while True:
        if 5 < count <= 10:
            event.clear()  # 红灯，清除标志位
            log.info("red light is on...")
        elif count > 10:
            event.set()  # 绿灯，设置标志位
            count = 0
        else:
            log.info('green light is on...')

        time.sleep(random.random())
        count += 1


def car(name):
    st = time.time()
    while True:
        if event.is_set():  # 判断是否设置了标志位
            log.info('[%s] running.....' % name)
            time.sleep(random.random())
        else:
            log.info('[%s] sees red light, stop and wait...' % name)
            event.wait()
            log.info('light turns green, [%s] start going...' % name)
        if time.time() - st > 30:
            break


def car_running():
    start_time = time.time()
    light = threading.Thread(target=lighter, )
    light.setDaemon(True)
    light.start()

    run_car = threading.Thread(target=car, args=('MINT',))
    run_car.start()
    end_time = time.time()
    while not run_car.is_alive():
        break
    log.info('用时：{}'.format(end_time - start_time))


"""
队列 Queue
Python的queue模块为单独的一个模块，并不在threading里。Queue模拟各种不同的队列，使不同线程之间实现松耦合，并且提高效率，经常使用它。
Python中的queue有三种队列，分别是queue.Queue() queue.LifoQueue() queue.PriorityQueue()
Queue就是FIFO(First In First Out)先入先出队列。
LifoQueue是LIFO(Last In First Out)后入先出队列，对应栈数据结构。
PriorityQueue需要你指定添加进队列的数据的重要性，然后队列根据重要性排序，更小的先出。
官方文档：
最小值先被取出( 最小值条目是由 sorted(list(entries))[0] 返回的条目)。
条目的典型模式是一个以下形式的元组： (priority_number, data) 。
也就是说你向PriorityQueue中添加数据时，推荐采用 (priority_number, data) 格式，
元组的第一个数据代表优先级，数字越小越先（可以是负数），假如优先级相同，会比较第二个数据，假如不可比较会报错。
假如前两个数据都相等，则顺序随机。

Queue是父类，下面介绍Queue的方法：
Queue(maxsize) 实例化Queue类可提供队列最大值的参数。到达最大值之后的put操作会阻塞。
Queue.put(block=True, timeout=None) 向队列中添加一个数据，同样可以设置阻塞等待时长。超时直接抛出queue.Full错误。
Queue.get(block=True, timeout=None) 从队列中获取一个数据，并从中删除这个数据，超时抛出queue.Empty错误。不设置超时会一直堵塞。
Queue.qsize() 返回队列中数据的量，不怎么可靠，因为获取的同时，其他线程可能进行操作。
Queue.join()队列还存在未完成任务时阻塞，等待直到队列无未完成任务。注意是任务完成而不是队列为空，需要与task_done联合使用
Queue.task_done() 每put一个数据就会让未完成任务+1，但是get不会-1，只有task_done才会-1,队列为空时报错ValueError
"""


def producer(iqueue, name):  # 生产者
    menu = ("蒸羊羔", "蒸熊掌", "蒸鹿尾儿", "烧花鸭", "烧雏鸡", "烧子鹅", "卤猪", "卤鸭", "酱鸡",
            "腊肉", "松花", "小肚儿", "晾肉", "香肠", "什锦苏盘",)  # 食物列表
    log.info('[{}]厨师来了'.format(name))
    for i in range(10):  # 上十道菜，每道菜加工0.8s
        food = random.choice(menu)
        log.info('[{}]正在加工{}中.....'.format(name, food))
        time.sleep(random.random())
        log.info('[{}]上菜了...{}'.format(name, food))
        iqueue.put(food)


def consumer(iqueue, name):
    log.info('[{}]客人来了'.format(name))
    while True:  # 每道菜吃0.5s，等上菜的耐心是0.5s
        try:
            food = iqueue.get(timeout=0.5)
            log.info('[{}]正在享用美食:{}'.format(name, food))
            time.sleep(random.random())
        except queue.Empty:  # get不到会抛出Empty
            log.info("没菜吃了，[{}]走了".format(name))
            break


def queue_usage():
    p_queue = queue.Queue()
    for i in range(4):
        name = "Cooker{}".format(i)
        pro_thread = threading.Thread(target=producer, args=(p_queue, name))  # 由于参数是元组，所以末尾加逗号
        pro_thread.start()
    # time.sleep(1)
    for i in range(2):
        name = "Consumer{}".format(i)
        con_thread = threading.Thread(target=consumer, args=(p_queue, name))
        con_thread.start()


"""
线程池 thread pool
虽然线程比进程简单许多，但是系统启动一个新线程的成本依旧很高。
线程池创建时会自动创建一定空闲的线程，我们将一个函数（任务）提交给线程池，线程池就会调用一个空闲的进程来执行它；
当函数结束时，线程不死亡，而是返回到线程池中等待执行下一个函数（任务）。

当程序中需要创建大量生存期短暂的线程时，可考虑线程池；当程序中需要控制并发线程时，可考虑线程池

python中有concurrent.futures模块，线程池的基类是Executor，
其有两个子类，即ThreadPoolExecutor和ProcessPoolExecutor，其中ThreadPoolExecutor 用于创建线程池；
而ProcessPoolExecutor 用于创建进程池。

Executor 提供了如下常用方法：
submit(fn, *args, **kwargs)：
    将fn函数提交给线程池。args代表传给fn函数的参数，kwargs代表以关键字参数的形式为fn函数传入参数。
map(func, *iterables, timeout=None, chunksize=1)：
    该函数类似于全局函数map(func, *iterables)，只是该函数将会启动多个线程，以异步方式立即对 iterables 执行 map 处理。
    超时抛出TimeoutError错误。返回每个函数的结果，注意不是返回future。
shutdown(wait=True)：
    关闭线程池。关闭之后线程池不再接受新任务，但会将之前提交的任务完成。
程序将task函数submit给线程池后，会返回一个Future对象，Future主要用来获取task的返回值。
由于结果不确定，对于当时是的未来的对象，所以取名future。
Future 提供了如下方法：
cancel()：取消该Future代表的线程任务。如果该任务正在执行，不可取消，则该方法返回False；否则，程序会取消该任务，并返回True。
cancelled()：返回Future代表的线程任务是否被成功取消。
running()：如果该Future代表的线程任务正在执行、不可被取消，该方法返回True。
done()：如果该Future代表的线程任务被成功取消或执行完成，则该方法返回True。
result(timeout=None)：获取该Future代表的线程任务最后返回的结果。
    如果Future代表的线程任务还未完成，该方法将会阻塞当前线程，其中timeout 参数指定最多阻塞多少秒。
    超时抛出TimeoutError，取消抛出CancelledError。
exception(timeout=None)：获取该Future代表的线程任务所引发的异常。如果该任务成功完成，没有异常，则该方法返回None。
add_done_callback(fn)：为该Future代表的线程任务注册一个“回调函数”，当该任务成功完成时，程序会自动触发该fn函数，参数是future。

"""


def worker(numb, name="default"):
    tmp = 1
    log.info(name + " PoolExecutor: " + threading.current_thread().name)
    for i in range(1, numb):
        tmp *= i
        # tmp = tmp + i ** 2
    log.info("{} calculation result is {}".format(name, tmp))
    return name, tmp


def thread_pool_usage():
    # ThreadPool实现原理，起多个线程；根据任务分配单线程或多线程执行？？
    # 注意查看线程号和threading.current_thread().name
    pool = ThreadPoolExecutor(max_workers=3)
    pool_list = []
    for i in range(21):
        name = "Thread{}".format(i)
        random_int = random.randint(21, 100)
        future = pool.submit(worker, random_int, name)
        pool_list.append(future)
    for ft in pool_list:
        while ft.done() is False:
            time.sleep(random.random())
        rv = ft.result()
        log.info("{}'s result is {}".format(rv[0], rv[1]))
    # 关闭线程池
    pool.shutdown()

    log.info("=======================")
    # 线程池支持上下文管理协议，用with可以避免忘记写shutdown
    with ThreadPoolExecutor(max_workers=2) as map_pool:
        # 使用线程执行map计算
        # 后面元组有几个元素，因此程序启动几次线程来执行action函数
        results = map_pool.map(worker, (12, 21, 52, 72, 88, 98))  # map接口做不到传多参数，iterables导致
        for result in results:
            log.info("{}'s result is {}".format(result[0], result[1]))
    """
    使用map()方法来启动线程，并收集线程的执行结果，不仅具有代码简单的优点，而且虽然程序会以并发方式来执行worker()函数.
    但最后收集的worker()函数的执行结果，依然与传入参数的结果保持一致。
    """


"""
条件变量 Condition
下面介绍我理解的某种条件下使用条件变量的方法。
Condition和某种锁相关联，但是他可以自动创建锁，服从上下文管理协议，用with方便，
acquire()和release()用来请求底层锁，像我这种不懂的就不要用了
wait(timeout=None)：等待直到被通知(notify)，超时返回False。
wait_for(predicate, timeout=None)：等待直到条件为真。predicate是一个可调用对象且返回值是布尔类型。这个方法会重复调用wait()直到满足判断。超时返回False
notify(n=1)：唤醒处于wait状态（等待这个条件）的n个线程
notify_all()：唤醒处于wait状态（等待这个条件）的所有线程
使用条件变量的典型情况是将锁用于同步某些共享状态的权限，那些对某些状态的特定改变感兴趣的线程，它们应该重复调用wait()，直到看到所期望的改变发生；而对于修改某个状态的线程，修改完后调用notify()。
"""
"""
定时器 Timer
是Thread的子类，像一个自定义线程一样。
定时器的函数介绍：
Timer(interval, function, args, kwargs)：指定延时的事件和要执行的函数和参数。
Timer.start()：开启定时器，经过一定事件后执行。
Timer.cancel()：取消定时器。
"""
"""
栅栏 Barrier
与其叫栅栏，不如叫开车对象。这个类的功能是等人齐就发车。并且一趟车走之后自动开启下一趟车，
翻车条件：超时、强行abort。
抛出错误条件：wait的时候翻车，wait的时候发新车。
下面介绍Barrier的函数和属性：
Barrier(parties, action=None, timeout=None)：parties是数量，当阻塞的线程到达这个数量是就放行（当乘客到达这个数字时就发车）。
    action是随机抽取一个幸运线程，发车时让这个线程先执行action函数再干自己的事。超时后翻车。
wait(timeout=None)：线程上车，等开车，这里的timeout会覆盖Barrier的timeout，超时会强行发车。
    返回一个范围在0到parties-1的整数，每个线程都不同，可用于从所有线程中选择唯一的一个线程执行一些特别的工作。
    如果车翻了抛出BrokenBarrierError错误。
reset()：重置Barrier的状态，即再发一辆新车。假如有人上了旧车，那些人会抛出BrokenBarrierError错误
abort()：一般用来防止死锁，强行翻车。通常给Barrier设置超时时间而不用这个。
parties：发车需要的人数量。
n_waiting：正在车上的人的数量。
broken：布尔值，栅栏有没有烂，即车有没有翻。
"""
'''
                          GIL  全局解释器
        在非python环境中，单核情况下，同时只能有一个任务执行。多核时可以支持多个线程同时执行。但是在python中，无论有多少个核
        同时只能执行一个线程。究其原因，这就是由于GIL的存在导致的。
        GIL的全程是全局解释器，来源是python设计之初的考虑，为了数据安全所做的决定。某个线程想要执行，必须先拿到GIL，我们可以
        把GIL看做是“通行证”，并且在一个python进程之中，GIL只有一个。拿不到线程的通行证，并且在一个python进程中，GIL只有一个，
        拿不到通行证的线程，就不允许进入CPU执行。GIL只在cpython中才有，因为cpython调用的是c语言的原生线程，所以他不能直接操
        作cpu，而只能利用GIL保证同一时间只能有一个线程拿到数据。而在pypy和jpython中是没有GIL的
        python在使用多线程的时候，调用的是c语言的原生过程。
'''
'''
                          python针对不同类型的代码执行效率是不同的
        1、CPU密集型代码（各种循环处理、计算等），在这种情况下，由于计算工作多，ticks技术很快就会达到阀值，然后触发GIL的
        释放与再竞争（多个线程来回切换当然是需要消耗资源的），所以python下的多线程对CPU密集型代码并不友好。
        2、IO密集型代码（文件处理、网络爬虫等涉及文件读写操作），多线程能够有效提升效率（单线程下有IO操作会进行IO等待，
        造成不必要的时间浪费，而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序的执行
        效率）。所以python的多线程对IO密集型代码比较友好。
'''
'''
    主要要看任务的类型，我们把任务分为I/O密集型和计算密集型，而多线程切换又分为I/O切换和时间切换。
    如果任务是I/O密集型，若不采用多线程，我们在进行I/O操作时，势必要等待前面I/O任务完成后面的I/O任务才能进行，此时CPU处于等待状态，
    这时如果采用多线程的话，刚好可以切换到另一个I/O任务。这样就刚好可以充分利用CPU，避免CPU处于闲置状态，提高效率。
    但是如果任务是计算型，CPU会一直在进行工作，直到一定的时间后采取多线程时间切换的方式进行切换线程，此时CPU一直处于工作状态，
    此种情况下并不能提高性能，相反在切换多线程任务时，可能还会造成时间和资源的浪费，导致效能下降。
    这是造成上面两种多线程结果不同的解释，结论:
    I/O密集型任务，建议采取多线程，还可以采用多进程+协程的方式(例如:爬虫多采用多线程处理爬取的数据)；
    计算密集型任务，python此时就不适用了。
'''
"""
学习内容主要来自以下：
https://blog.kamino.link/2021/03/01/Python-Multithreading-in-detail/
https://blog.csdn.net/weixin_40481076/article/details/101594705
"""

"""
协程
又称为微线程，在一个线程中执行，执行函数时可以随时中断，由程序（用户）自身控制，执行效率极高。
与多线程比较，没有切换线程的开销和多线程锁机制。
协程的主要使用场景
协程的主要应用场景是IO密集型任务，总结几个常见的使用场景：
网络请求，比如爬虫，大量使用 aiohttp
文件读取， aiofile
web框架， aiohttp， fastapi
数据库查询， asyncpg, databases
"""


async def do_something(n, content):
    log.info("Hello " + content)
    await asyncio.sleep(n)
    log.info(content)


async def main():
    await do_something(1, "QingDao")
    task1 = asyncio.create_task(do_something(2, "Starbucks"))
    task2 = asyncio.create_task(do_something(3, "FamilyMart"))

    await task1
    await task2


if __name__ == "__main__":
    logRecorder()
    log.info("main thread start.")
    asyncio.run(main())
    log.info('main thread end.')
