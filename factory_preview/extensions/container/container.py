#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/25 20:21
# @Author : 詹荣瑞
# @File : container.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import ObjID, Position, Dict
from factory_preview.extensions.extension import ExtensionBase


class Container(ExtensionBase):

    def __init__(self, pos: Position):
        self.pos = pos
        self.bag: Dict[int, int] = {}

    def set(self, objs: dict):
        for obj, num in objs.items():
            if obj in self.bag.keys():
                self.bag[obj] += num
            else:
                self.bag.update({obj: num})
        return self

    def get_stock(self, obj_id: ObjID) -> int:
        raise NotImplementedError

    def run(self, world):
        raise NotImplementedError
