#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 10:36
# @Author : 詹荣瑞
# @File : market.py
# @desc : 本代码未经授权禁止商用
from .state import VectorState
from .material import Material


class Market(object):

    def __init__(self, *materials: Material):
        values = [1, 1, 1]
        self.names = []
        for i, m in enumerate(materials):
            self.names.append(m.name)
            values.append(m.price)
            m.id = i + 1
        self.len = len(materials)
        self.state = VectorState(self.len + 3, values=values)

    def find_price(self, material: Material):
        return self.state[0] * self.state[material.id + 2]
