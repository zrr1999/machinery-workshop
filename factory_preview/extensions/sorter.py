#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/25 20:19
# @Author : 詹荣瑞
# @File : sorter.py
# @desc : 本代码未经授权禁止商用
from factory_preview import World
from factory_preview.extensions.container import Container
from factory_preview.extensions.extension import ExtensionBase
from factory_preview.utils.typing import Union, Tuple, Position, Site, ObjID
from factory_preview.core import StateBase, SimpleFormula, FormulaBase
from factory_preview.parameters import EMPTY


class Sorter(ExtensionBase):

    def __init__(self, site_source: Union[Container, Position],
                 site_target: Union[Container, Position], filtrate: ObjID):
        self.site_source = site_source
        self.site_target = site_target
        self.filtrate = filtrate

    def run(self, world: World):
        flag = [False, False]
        world_map = world.get_map_layer(0)
        if isinstance(self.site_target, Container):
            flag[0] = True
            if self.site_target.get_stock(self.filtrate) == -1:
                print(f"目标位置不可输入<商品{self.filtrate}>")
                return
        else:
            if world_map[self.site_target] != EMPTY:
                print("目标位置不为空")
                return

        if isinstance(self.site_source, Container):
            flag[1] = True
            if self.site_source.get_stock(self.filtrate) <= 0:
                print(f"商品源无<商品{self.filtrate}>")
                return
        else:
            if self.filtrate != world_map[self.site_source]:
                print(f"目标位置无<商品{self.filtrate}>")
                return

        if flag[0]:
            self.site_target.set({self.filtrate: 1})
        else:
            world_map[self.site_target] = self.filtrate
        if flag[1]:
            self.site_source.bag[self.filtrate] -= 1
        else:
            world_map[self.site_source] = EMPTY
