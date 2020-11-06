#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 10:36
# @Author : 詹荣瑞
# @File : market.py
# @desc : 本代码未经授权禁止商用
class Market(object):

    def __init__(self, materials):
        self.names = []
        self.prices = []
        for m in materials:
            self.names.append(m.name)
            self.prices.append(m.price)

    # def find_price(self):


