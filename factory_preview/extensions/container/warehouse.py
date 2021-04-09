#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/22 12:23
# @Author : 詹荣瑞
# @File : warehouse.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from factory_preview.utils.typing import ObjID
from factory.parameters import EMPTY
from factory_preview.utils.typing import Position, List,Tuple
from factory_preview.extensions.container import Container
from factory.commodity import Commodity
from typing import Union


class Warehouse(Container):

    def __init__(self, pos: Position):
        super().__init__(pos)
        self.settings: Tuple[int, bool] = (0, False)

    def get_stock(self, obj_id: ObjID) -> int:
        if obj_id in self.bag:
            return self.bag[obj_id]
        else:
            return 0

    def set_mode(self, obj_id: ObjID, get: bool):
        self.settings = (obj_id, get)

    def run(self, world):
        obj_id, get = self.settings
        # print(self.bag)
        # if get:
        #     world_map = world.get_map_layer(0)
        #     obj_target = world_map[self.pos]
        #     if world_map[self.pos] == EMPTY:
        #         print("仓库无法收取物品（不存在物品）")
        #     else:
        #         if obj_id == 0 or obj_id == obj_target:
        #             world_map[self.pos] = EMPTY
        #             if obj_target in self.bag.keys():
        #                 self.bag[obj_target] += 1
        #             else:
        #                 self.bag[obj_target] = 1
        #         else:
        #             print(f"仓库期望回收<物品{obj_id}>，但目标位置存在<物品{obj_target}>")
        # elif obj_id in self.bag.keys() and self.bag[obj_id] > 0:
        #     world_map = world.get_map_layer(0)
        #     if world_map[self.pos] != EMPTY:
        #         print("仓库无法放置物品（已存在物品）")
        #     else:
        #         world_map[self.pos] = obj_id
        #         self.bag[obj_id] -= 1
        # else:
        #     print(f"仓库空或无<商品{obj_id}>")

