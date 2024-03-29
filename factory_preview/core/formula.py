#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/25 18:33
# @Author : 詹荣瑞
# @File : formula.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import Position, List, ObjID, Dict


class FormulaBase(object):

    def __init__(self, raws: Dict[ObjID, int], product: Dict[ObjID, int]):
        self.raws = raws
        self.product = product

    def compose(self, bag: Dict[ObjID, int]):
        for r, num in self.raws.items():
            if r not in bag or bag[r]<num:
                print(f"原材料<商品{r}>不足")
                return None
        for r, num in self.raws.items():
            bag[r] -= num
        return self.product

    def format(self, market):
        raws = {}
        product = {}
        for key, value in self.raws.items():
            raws[market.get_id(key)] = value
        for key, value in self.product.items():
            product[market.get_id(key)] = value
        self.raws = raws
        self.product = product
        return self




class SimpleFormula(FormulaBase):

    def __init__(self, raws: List[ObjID], product: ObjID):
        super().__init__({r: 1 for r in raws}, {product: 1})
