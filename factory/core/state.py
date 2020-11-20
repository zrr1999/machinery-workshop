#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:26
# @Author : 詹荣瑞
# @File : state.py
# @desc : 本代码未经授权禁止商用
from factory.utils.typing import Size
import numpy as np


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

    def __init__(self, size: Size = 3, num_layers: int = 1, values=None, dtype=None):
        if isinstance(size, int):
            height = width = size
        else:
            height, width = size
        s = np.zeros((num_layers, height, width), dtype)
        if values is not None:
            s[:] = values
        super(MatrixState, self).__init__(np.zeros((num_layers, height, width), np.int), None)


class VectorState(StateBase):

    def __init__(self, n_state: int = 1, tag=None, values=None, dtype=None):
        s = np.zeros(n_state, dtype)
        if values is not None:
            s[:] = values
        super().__init__(s, tag)
