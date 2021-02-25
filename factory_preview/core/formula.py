#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/25 18:33
# @Author : 詹荣瑞
# @File : formula.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import Position, List, ObjID, Dict


class FormulaBase(object):

    def __init__(self, raws: Dict[int, int], product: ObjID):
        self.raws = raws
        self.product = product

    def compose(self, bag: Dict[int, int]):
        for r, num in self.raws.items():
            if r not in bag or bag[r]<num:
                print(f"原材料<商品{r}>不足")
                return None
        for r, num in self.raws.items():
            bag[r] -= num
        return self.product


class SimpleFormula(FormulaBase):

    def __init__(self, raws: List[int], product: ObjID):
        super().__init__({r: 1 for r in raws}, product)