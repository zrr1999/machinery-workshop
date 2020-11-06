#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:39
# @Author : 詹荣瑞
# @File : operation.py
# @desc : 本代码未经授权禁止商用
import warnings


class OperationBase(object):
    NAME = "OperationBase"

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return self.NAME

    def __call__(self, states, controller):
        raise NotImplementedError


class Move(OperationBase):
    NAME = "Move"

    def __init__(self, start, end, empty=0, target="ms"):
        self.a = start
        self.b = end

        self.empty = empty
        self.target = target

    def __call__(self, states, controller=None):
        state = states[self.target].state
        if state[self.a] == self.empty:
            warnings.warn("你正在试图移动一个空物体，错误代码0x0001")
            return 0x0001
        elif state[self.b] != self.empty:
            warnings.warn("你正在将一个物体放置到非空位置，错误代码0x0002")
            return 0x0002
        else:
            obj = state[self.a]
            state[self.a] = self.empty
            state[self.b] = obj
            return 0

    def __repr__(self):
        return f"{self.NAME}({self.a}->{self.b})"


class Buy(OperationBase):
    NAME = "Buy"

    def __init__(self, goods, position, coin=0, empty=0, target=("ms", "ps")):
        self.goods = goods
        self.pos = position
        self.coin = coin

        self.empty = empty
        self.target = target

    def __call__(self, states, controller=None, market=None):
        ms = states[self.target[0]].state
        ps = states[self.target[1]].state
        self.goods.update()
        if ps[self.coin] < self.goods.price:
            warnings.warn("货币不足，错误代码0x0011")
            return 0x0011
        elif ms[self.pos] != self.empty:
            warnings.warn("你正在将一个物体放置到非空位置，错误代码0x0002")
            return 0x0002
        else:
            ps[self.coin] -= self.goods.price
            ms[self.pos] = self.goods.id


class SetState(OperationBase):
    NAME = "SetState"

    def __init__(self, states, target=("ms", "ps")):
        self.states = states
        self.target = target

    def __call__(self, states, controller=None):
        for t in self.target:
            states[t].state = states[t]
