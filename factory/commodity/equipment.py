#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/19 21:21
# @Author : 詹荣瑞
# @File : equipment.py
# @desc : 本代码未经授权禁止商用
from . import Commodity


class Equipment(Commodity):

    def __init__(self, name: str = "Material", price: int = 0, size=(2, 2)):
        super().__init__(name=name, price=price)
        self.size = size
        self.objs = []

    def put(self, obj: Commodity):
        self.objs += obj
