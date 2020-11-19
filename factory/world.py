#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
from typing import Tuple, Union
from .utils.typing import Pos
from factory.core.state import MatrixState, VectorState
from .operation import Buy, Catch, Place, Sell
from .transaction import Market
from factory.commodity.material import Material

iron = Material(name="iron", price=5)  # 铁
screw = Material(name="screw", price=15)  # 螺丝
processor = Material(name="processor", price=20)  # 加工器
materials = [iron, screw, processor]


class World(object):

    def __init__(self, size: Tuple[int, int] = (5, 5), initial=100):
        self.market = Market(*materials)
        self.states = {
            "map": MatrixState(*size, 3),  # Map state
            "player": VectorState(3),  # Player state
            "market": self.market.state  # Market state
        }
        self.states["player"][0] = initial
        self.buy_ops = {m.name: Buy(m, (), self.market) for m in materials}
        # self.controller = Controller().add_sequence(ss=[init]).step(s)

    def step(self):
        return self.states

    def buy(self, material: Union[Material, str, int], position: Pos):
        if isinstance(material, str):
            buy = self.buy_ops.get(material)
        elif isinstance(material, int):
            buy = Buy(materials[material], (), self.market)
        else:
            buy = Buy(material, (), self.market)
        buy.pos = position
        return buy(self.states)

    def sell(self, position: Pos):
        op = Sell(position, self.market)
        return op(self.states)

    def catch(self, position: Pos):
        op = Catch(position)
        return op(self.states)

    def place(self, position: Pos, obj: int):
        op = Place(position, obj=obj)
        return op(self.states)
