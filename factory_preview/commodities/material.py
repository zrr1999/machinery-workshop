#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/29 19:27
# @Author : 詹荣瑞
# @File : material.py
# @desc : 本代码未经授权禁止商用
from .commodity import CommodityBase


class Material(CommodityBase):
    _type = "Material"

    def __init__(self, name: str = "material", price: int = 0):
        super().__init__(name=name, price=price)

    def apply(self, func=None):
        return self
