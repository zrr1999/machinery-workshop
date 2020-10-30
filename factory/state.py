#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:26
# @Author : 詹荣瑞
# @File : state.py
# @desc : 本代码未经授权禁止商用
import numpy as np


class StateBase(object):

    def __init__(self, state, tag):
        self.state = state
        self.tag = tag

    def __str__(self):
        return str(self.state.tolist())

    def __repr__(self):
        return str(self.state.tolist())


class MapState(StateBase):

    def __init__(self, width=3, height=None, num_layers=1):
        if height is None:
            height = width
        super(MapState, self).__init__(np.zeros((num_layers, height, width), np.int), None)


class PlayerState(StateBase):

    def __init__(self, n_state=1, tag=None):
        super().__init__(np.zeros(n_state), tag)
