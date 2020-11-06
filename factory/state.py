#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:26
# @Author : 詹荣瑞
# @File : state.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from typing import List, Iterable


class StateBase(object):

    def __init__(self, state, tag):
        self.state = state
        self.tag = tag

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __str__(self):
        return str(self.state.tolist())

    def __repr__(self):
        return str(self.state.tolist())


class MatrixState(StateBase):

    def __init__(self, width: int = 3, height: int = None, num_layers: int = 1, values=None):
        if height is None:
            height = width
        s = np.zeros((num_layers, height, width))
        if values is not None:
            s[:] = values
        super(MatrixState, self).__init__(np.zeros((num_layers, height, width), np.int), None)


class VectorState(StateBase):

    def __init__(self, n_state: int = 1, tag=None, values=None):
        s = np.zeros(n_state)
        if values is not None:
            s[:] = values
        super().__init__(s, tag)
