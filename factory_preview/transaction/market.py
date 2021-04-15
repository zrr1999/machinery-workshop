#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 10:36
# @Author : 詹荣瑞
# @File : market.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import ObjID, Position, Callable
from factory_preview.core.state import VectorState
from factory_preview.commodities import Material, Equipment, CommodityBase
from factory_preview.operations import Buy, ObjPlace, OperationSequence


class Market(object):

    def __init__(self, *commodities: CommodityBase):
        self._state = VectorState(3, values=[1, 1, 1])  # 通货膨胀
        self.ids = {}
        self.names = {}
        self.prices = {}
        self.commodities = {}
        self.materials = []
        self.equipments = []
        for i, m in enumerate(commodities):
            m.id = i + 1
            self.commodities[m.id] = m
            self.prices[m.id] = m.price
            self.names[m.id] = m.name
            self.ids[m.name] = m.id
            if isinstance(m, Equipment):
                self.equipments.append(m.id)
            else:
                self.materials.append(m.id)

    def __len__(self):
        return len(self.commodities)

    def __getitem__(self, id: ObjID):
        return self.commodities[id-1]

    def buy(self, obj_id: ObjID, pos: Position) -> Callable[[dict], dict]:
        return OperationSequence(
            ObjPlace(obj_id, pos),
            Buy(obj_id, self),
        )

    def get_id(self, obj_name: str):
        return self.ids[obj_name]

    @property
    def state(self):
        return self._state.state

    @state.setter
    def state(self, value):
        self._state.state[:] = value
        for m, p in zip(self.commodities, self.prices):
            m.price = value[0] * p
