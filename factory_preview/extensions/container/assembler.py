#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/25 16:47
# @Author : 詹荣瑞
# @File : assembler.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from factory_preview.utils.typing import ObjID
from factory.parameters import EMPTY
from factory_preview.utils.typing import Position, List, Tuple, Dict
from factory_preview.core import StateBase, SimpleFormula, FormulaBase
from factory_preview.extensions.container import Container
from factory.commodity import Commodity
from typing import Union


class Assembler(Container):

    def __init__(self, pos: Union[Position, int], cost_time: int = 1):
        super().__init__(pos)
        self.settings: Tuple[int, bool] = (0, False)
        self.formula: FormulaBase = SimpleFormula([], 0)
        self.cost_time = cost_time
        self.progress = 0

    def get_stock(self, obj_id: ObjID) -> int:
        if obj_id in self.bag:
            return self.bag[obj_id]
        else:
            return -1

    def set(self, objs: dict):
        for obj, num in objs.items():
            if obj in self.formula.product or obj in self.formula.raws:
                self.bag[obj] += num
            else:
                print("制造台只能放置原材料或制造物品")
        return self

    def set_formula(self, formula: FormulaBase):
        self.formula = formula
        self.bag = {**formula.raws, **formula.product}
        for k in self.bag:
            self.bag[k] = 0
        return self

    def set_mode(self, formula: FormulaBase):
        self.formula = formula
        self.bag = {r: 0 for r in [*formula.raws, self.formula.product]}

    def run(self, world):
        if self.progress == self.cost_time:
            self.progress = 0
            product = self.formula.compose(self.bag)
            if product is not None:
                self.set(product)
        else:
            self.progress += 1
