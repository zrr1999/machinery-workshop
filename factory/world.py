#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
from typing import Tuple, Union
from .typing import Pos
from .state import MatrixState, VectorState
from .operation import Move, Buy
from .transaction import Material, Market


iron = Material(name="Iron", price=5)  # 铁
screw = Material(name="Screw", price=15)  # 螺丝
materials = [iron, screw]


class World(object):

    def __init__(self, size: Tuple[int, int] = (5, 5), initial=100):
        self.state = {
            "ms": MatrixState(*size, 3),  # Map state
            "ps": VectorState(3),  # Player state
        }
        self.state["ps"][0] = initial
        self.market = Market(*materials)
        self.buy_ops = {m.name: Buy(m, (), self.market) for m in materials}
        # self.controller = Controller().add_sequence(ss=[init]).step(s)

    def step(self):
        return self.state

    def buy(self, material: Union[Material, str, int], position: Pos):
        if isinstance(material, str):
            buy = self.buy_ops.get(material)
        elif isinstance(material, int):
            buy = Buy(materials[material], (), self.market)
        else:
            buy = Buy(material, (), self.market)
        buy.pos = position
        return buy(self.state)

    def move(self, a):
        move = Move((0, 0, 0), (0, 0, a))
        return move(self.state)
