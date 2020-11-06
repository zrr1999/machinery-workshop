#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
from typing import Optional
from .state import MatrixState, VectorState
from .operation import Move, Buy
from .controller import Controller
from .material import Material
from .market import Market


iron = Material(name="Iron", price=5)  # 铁
screw = Material(name="Screw", price=15)  # 螺丝
materials = [iron, screw]


class World(object):

    def __init__(self):
        self.state = {
            "ms": MatrixState(),  # Map state
            "ps": VectorState(),  # Player state
        }
        self.market = Market(*materials)
        self.buy_op = {m.name: Buy(m, (), self.market) for m in materials}
        self.controller = Controller().add_sequence(ss=[init]).step(s)

    def buy(self, material: Optional[Material, str, int]):
        self.buy_op




