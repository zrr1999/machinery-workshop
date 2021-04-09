#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 22:02
# @Author : 詹荣瑞
# @File : atomic.py
# @desc : 本代码未经授权禁止商用
import warnings
from .operation_base import OperationBase
from factory.utils.typing import Pos, ObjId
from factory.parameters import EMPTY


class ObjPlace(OperationBase):
    def __init__(self, position: Pos, obj_id: ObjId):
        self.pos = position
        self.obj = obj_id

    def __call__(self, states, controller=None, **kwargs):
        state = states["map"].state
        if state[self.pos] != EMPTY:
            warnings.warn(f"你正在将一个物体放置到非空位置{self.pos}")
        else:
            state[self.pos] = self.obj
            return {}


class ObjCatch(OperationBase):
    def __init__(self, position: Pos):
        self.pos = position

    def __call__(self, states, controller=None):
        state = states["map"].state
        if state[self.pos] == EMPTY:
            print(f"你正在试图抬起位置{self.pos}的一个空物体")
        else:
            obj = state[self.pos]
            state[self.pos] = EMPTY
            return {obj: 1}


class ObjGet(OperationBase):
    def __init__(self, obj_id: ObjId, amount: int):
        self.obj = obj_id
        self.amount = amount

    def __call__(self, states, controller=None):
        return {self.obj: self.amount}


class ValueUp(OperationBase):
    def __init__(self, index: int, amount: int):
        self.index = index
        self.amount = amount

    def __call__(self, states, controller=None, **kwargs):
        state = states["player"].state
        state[self.index] += self.amount
        return {}


class ValueDown(OperationBase):
    def __init__(self, index: int, amount: int):
        self.index = index
        self.amount = amount

    def __call__(self, states, controller=None, **kwargs):
        state = states["player"].state
        state[self.index] -= self.amount
        return {}
