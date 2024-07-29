#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    :2023/12/1 21:49
# @Author  : octy

import numpy
import torch


class NumpyLearn(object):
    def __init__(self):
        pass

    def learn_numpy(self):
        np = numpy.array([1, 2, 3, 4])
        print(np)

        np = numpy.array([1, 2, 3, 4], dtype=numpy.int32)
        print(np)

    def convert_to_torch(self):
        a = numpy.array([1, 2, 3, 4])
        b = torch.from_numpy(a)
        print(b)


if __name__ == '__main__':
    np = NumpyLearn()
    np.learn_numpy()
    np.convert_to_torch()
