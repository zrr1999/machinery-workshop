#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/30 11:04
# @Author : 詹荣瑞
# @File : conveyor.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from factory_preview.world import World
from factory.parameters import EMPTY


class Conveyor(object):

    def __init__(self, paths: list):
        self.paths = np.array(paths)

    def run(self, world: World):
        world_map = world.get_map_layer(0)

        for i in range(self.paths.shape[0] - 1, -1, -1):
            caught_obj = world_map[tuple(self.paths[i])]
            if caught_obj == EMPTY:
                world_map[tuple(self.paths[1:i + 1].T)] = world_map[tuple(self.paths[:i].T)]
                world_map[tuple(self.paths[0].T)] = EMPTY
                break
