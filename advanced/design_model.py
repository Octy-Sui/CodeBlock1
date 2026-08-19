# @Time    :2021/7/24 2:44 下午
# @Author  : octy
import threading


class Singleton:
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance
