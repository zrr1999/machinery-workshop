#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 10:36
# @Author : 詹荣瑞
# @File : market.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import ObjID, Position, Callable
from factory.core.state import VectorState
from factory.commodity.material import Material
from factory_preview.operation import Buy


class Market(object):

    def __init__(self, *materials: Material):
        self._state = VectorState(3, values=[1, 1, 1])  # 通货膨胀、、
        self.commodities = list(materials)
        names = []
        prices = []
        for i, m in enumerate(materials):
            m.id = i + 1
            names.append(m.name)
            prices.append(m.price)
        self.names = names
        self.prices = VectorState(len(self), values=prices)

    def __len__(self):
        return len(self.commodities)

    def __getitem__(self, id: ObjID):
        return self.commodities[id-1]

    def buy(self, obj_id: ObjID, pos: Position) -> Callable[[dict], None]:
        return Buy(self.commodities[obj_id], pos)

    @property
    def state(self):
        return self._state.state

    @state.setter
    def state(self, value):
        self._state.state[:] = value
        for m, p in zip(self.commodities, self.prices):
            m.price = value[0] * p
