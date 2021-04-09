#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/19 21:21
# @Author : 詹荣瑞
# @File : equipment.py
# @desc : 本代码未经授权禁止商用
from .commodity import CommodityBase


class Equipment(CommodityBase):
    _type = "Equipment"

    def __init__(self, name: str = "equipment", price: int = 0, size=(2, 2)):
        super().__init__(name=name, price=price, use=[])
        self.size = size
        self.objs = []

    def apply(self, func=None, args=None):
        if func == "put":
            self.objs += args


