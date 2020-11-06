#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/29 19:27
# @Author : 詹荣瑞
# @File : material.py
# @desc : 本代码未经授权禁止商用
from .market import Market


class Material(object):

    def __init__(self, material_id: int = None, name: str = "Material", price: int = 0):
        self.id = material_id
        self.name = name
        self.price = price

    def update_price(self, market: Market):
        self.price = market.find_price(self)

    def __str__(self):
        return f"{self.name}${self.price}"
