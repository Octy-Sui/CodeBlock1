# File   : timer.py
# Created: 2026-08-17 15:41:30
# Author : octy Sui
"""通用的性能测量装饰器."""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """统计函数执行耗时"""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            func_name = getattr(func, "__name__", func.__class__.__name__)
            logging.info(f"{func_name} executed in {elapsed:.6f}s")

    return wrapper
