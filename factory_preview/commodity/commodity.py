#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/19 21:20
# @Author : 詹荣瑞
# @File : commodity.py
# @desc : 本代码未经授权禁止商用
class CommodityBase(object):
    _type = "Commodity"

    def __init__(self, name, price: int = 0, use=()):
        self.name = name
        self.price = price
        self.use = list(use)

    def __str__(self):
        return f"{self._type}: {self.name}${self.price}"
