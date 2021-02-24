#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/2/22 12:23
# @Author : 詹荣瑞
# @File : warehouse.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from factory_preview.world import World
from factory.parameters import EMPTY
from factory.utils.typing import Pos
from factory.commodity import Commodity
from typing import Union


class Warehouse(object):

    def __init__(self, pos: Pos):
        self.pos = tuple(pos)
        self.bag = {}

    def set(self, objs: dict):
        for obj, num in objs.items():
            if obj in self.bag.keys():
                self.bag[obj] += num
            else:
                self.bag.update({obj: num})
        return self

    def run(self, obj, get: bool = False):
        if get:
            def output(world: World):
                print(self.bag)
                world_map = world.get_map_layer(0)
                obj_target = world_map[self.pos]
                if world_map[self.pos] == EMPTY:
                    print("仓库无法收取物品（不存在物品）")
                else:
                    if obj == 0 or obj == obj_target:
                        world_map[self.pos] = EMPTY
                        if obj_target in self.bag.keys():
                            self.bag[obj_target] += 1
                        else:
                            self.bag[obj_target] = 1
                    else:
                        print("仓库无法放置物品（存在非目标物品）")
        else:
            def output(world: World):
                print(self.bag)
                if obj in self.bag.keys() and self.bag[obj] > 0:
                    world_map = world.get_map_layer(0)
                    if world_map[self.pos] != EMPTY:
                        print("仓库无法放置物品（已存在物品）")
                    else:
                        world_map[self.pos] = obj
                        self.bag[obj] -= 1
                else:
                    print(f"仓库空或无{obj}")

        return output
