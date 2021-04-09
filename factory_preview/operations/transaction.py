#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 22:14
# @Author : 詹荣瑞
# @File : transaction.py
# @desc : 本代码未经授权禁止商用
import warnings
from factory_preview.operations.operation_base import OperationSequence
from factory_preview.operations.atomic import ValueDown, ValueUp, ObjGet
from factory_preview.utils.typing import Position, ObjID
from factory_preview.parameters import EMPTY
from typing import Dict, Union


# class Move(OperationSequence):
#     NAME = "Move"
#
#     def __init__(self, start: Position, end: Position, target: str = "map"):
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
#         return f"{self.NAME}({self.catch.Position}->{self.place.Position})"


class Buy(OperationSequence):
    def __init__(self, obj_id: ObjID, world):
        price = world.market.prices[obj_id]
        super().__init__(
            ValueDown(0, price),
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


class Sell(ValueUp):
    def __init__(self, objs: Union[Dict[ObjID, int], ObjID], world):
        if isinstance(objs, int):
            price = world.market.prices[objs]
        else:
            price = 0
            for obj_id, num in objs:
                price += num * world.market.prices[obj_id]

        super().__init__(0, price)
