#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 10:36
# @Author : 詹荣瑞
# @File : market.py
# @desc : 本代码未经授权禁止商用
from factory.utils.typing import Id
from factory.core.state import VectorState
from factory.commodity.material import Material


class Market(object):

    def __init__(self, *materials: Material):
        self.state = VectorState(3, values=[1, 1, 1])  # 通货膨胀、、
        self.materials = list(materials)
        names = []
        prices = []
        for i, m in enumerate(materials):
            m.id = i + 1
            names.append(m.name)
            prices.append(m.price)
        self.names = names
        self.price = VectorState(len(self), values=prices)

    def __len__(self):
        return len(self.materials)

    def __getitem__(self, id: Id):
        return self.materials[id - 1]

    def update_price(self, id: Id):
        i = id - 1
        self.materials[i].price = self.state[0] * self.state[i]
