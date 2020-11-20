#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/19 21:20
# @Author : 詹荣瑞
# @File : commodity.py
# @desc : 本代码未经授权禁止商用
class Commodity(object):
    type = 0

    def __init__(self, identity: int = None, name: str = "Material", price: int = 0):
        self.id = identity
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}${self.price}"
