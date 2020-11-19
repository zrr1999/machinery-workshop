#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:39
# @Author : 詹荣瑞
# @File : operation.py
# @desc : 本代码未经授权禁止商用
import warnings
from typing import Iterable, Dict
from .utils.typing import Pos
from factory.core.state import StateBase
from .controller import Controller
from .transaction import Market
from factory.commodity.material import Material


class OperationBase(object):
    NAME = "OperationBase"

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return self.NAME

    def __call__(self, states: Dict[str, StateBase], controller: Controller = None, **kwargs):
        raise NotImplementedError


class Catch(OperationBase):
    NAME = "Catch"

    def __init__(self, position: Pos, empty: int = 0, target: str = "map"):
        self.pos = position

        self.empty = empty
        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        state = states[self.target].state
        if state[self.pos] == self.empty:
            warnings.warn("你正在试图抬起一个空物体，错误代码0x0001")
            return 0x0001
        else:
            obj = state[self.pos]
            state[self.pos] = self.empty
            return obj


class Place(OperationBase):
    NAME = "Place"

    def __init__(self, position: Pos, obj: int = 0, empty: int = 0, target: str = "map"):
        self.pos = position

        self.empty = empty
        self.obj = obj
        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        state = states[self.target].state
        if state[self.pos] != self.empty:
            warnings.warn("你正在将一个物体放置到非空位置，错误代码0x0002")
            return 0x0002
        else:
            state[self.pos] = self.obj
            return 0


class Move(OperationBase):
    NAME = "Move"

    def __init__(self, start: Pos, end: Pos, empty: int = 0, target: str = "map"):
        self.catch = Catch(start, empty, target)
        self.place = Place(end, empty, empty, target)

        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        self.place.obj = self.catch(states)
        return self.place(states)

    def __repr__(self):
        return f"{self.NAME}({self.catch.pos}->{self.place.pos})"


class Buy(OperationBase):
    NAME = "Buy"

    def __init__(self, goods: Material, position: Pos, market: Market,
                 coin=0, empty=0, target=("map", "player")):
        self.goods = goods
        self.pos = position
        self.market = market
        self.coin = coin

        self.empty = empty
        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        ms = states[self.target[0]].state
        ps = states[self.target[1]].state
        self.market.update_price(self.goods)
        if ps[self.coin] < self.goods.price:
            warnings.warn("货币不足，错误代码0x0011")
            return 0x0011
        elif ms[self.pos] != self.empty:
            warnings.warn("你正在将一个物体放置到非空位置，错误代码0x0002")
            return 0x0002
        else:
            ps[self.coin] -= self.goods.price
            ms[self.pos] = self.goods.id
            return 0


class Sell(OperationBase):
    NAME = "Sell"

    def __init__(self, position: Pos, market: Market, coin=0, empty=0, target=("map", "player", "market")):
        self.pos = position
        self.market = market
        self.coin = coin

        self.empty = empty
        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        ms = states[self.target[0]].state
        ps = states[self.target[1]].state
        goods = self.market[ms[self.pos]]
        self.market.update_price(goods)
        if ms[self.pos] == self.empty:
            warnings.warn("目标位置无物品，无法出售，错误代码0x0003")
            return 0x0003
        else:
            ps[self.coin] += goods.price
            ms[self.pos] = self.empty
            return 0


class SetState(OperationBase):
    NAME = "SetState"

    def __init__(self, states: Dict[str, StateBase], target: Iterable[str] = ("ms", "ps")):
        self.states = states
        self.target = target

    def __call__(self, states, controller=None, **kwargs):
        for t in self.target:
            states[t].state = states[t]
