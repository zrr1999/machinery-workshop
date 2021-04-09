#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 22:14
# @Author : 詹荣瑞
# @File : transaction.py
# @desc : 本代码未经授权禁止商用
import warnings
from .operation_base import OperationSequence
from .atomic import ValueDown, ValueUp, ObjGet
from factory.utils.typing import Pos, ObjId
from factory.parameters import EMPTY
# class Move(OperationSequence):
#     NAME = "Move"
#
#     def __init__(self, start: Pos, end: Pos, target: str = "map"):
#         self.catch = Catch(start, target)
#         self.place = Place(end, EMPTY, target)
#
#         self.target = target
#
#     def __call__(self, states, controller=None, **kwargs):
#         self.place.obj = self.catch(states)
#         return self.place(states)
#
#     def __repr__(self):
#         return f"{self.NAME}({self.catch.pos}->{self.place.pos})"


class Buy(OperationSequence):
    def __init__(self, obj_id: ObjId, world, target="player"):
        price = world.market.prices[obj_id]
        super().__init__(
            ValueDown(0, price, target),
            ObjGet(obj_id, 1)
        )

    # def __call__(self, states, controller=None) -> dict:
    #     super().__call__(states, controller)
    #     ps = states[self.target].state
    #
    #     if ps[0] < self.price:
    #         print(f"货币有{self}个，不足{self.price}个")
    #         return {}
    #     else:
    #         ps[0] -= self.price
    #         return {self.obj: 1}


class Sell(OperationSequence):
    def __init__(self, position: Pos, world, target="player"):
        price = world.market.prices[obj_id]
        super().__init__(
            ValueDown(0, price, target),
            ObjGet(obj_id, 1)
        )
        price = world.market.prices[obj_id]
        price = world.market.prices[obj_id]
        self.pos = position
        self.market = market
        self.coin = coin

        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        ms = states[self.target[0]].state
        ps = states[self.target[1]].state
        goods = self.market[ms[self.pos]]
        if ms[self.pos] == EMPTY:
            warnings.warn("目标位置无物品，无法出售")
            return 0x0003
        else:
            ps[self.coin] += goods.price
            ms[self.pos] = EMPTY
            return 0