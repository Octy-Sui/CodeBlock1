#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2021/6/12 12:16 下午
# @Author  : octy

import logging
import os

from config.path import BlockPath


def logRecorder():
    log_format = '%(asctime)s [%(levelname)-8s] (%(process)d:%(thread)d) %(filename)s %(funcName)s ' \
                 'line:%(lineno)-4d %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(filename=os.path.join(BlockPath.LogPath, "log.txt"), encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console)


logRecorder()
