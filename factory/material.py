#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/29 19:27
# @Author : 詹荣瑞
# @File : material.py
# @desc : 本代码未经授权禁止商用
class Object(object):

    def __init__(self, identity: int = None, name: str = "Material", price: int = 0):
        self.id = identity
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}${self.price}"


Material = Object


class Equipment(Object):

    def __init__(self, name: str = "Material", price: int = 0, size=(2, 2)):
        super().__init__(name=name, price=price)
        self.size = size
        self.objs = []

    def put(self, obj: Object):
        self.objs += obj
