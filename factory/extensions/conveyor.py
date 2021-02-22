#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/30 11:04
# @Author : 詹荣瑞
# @File : conveyor.py
# @desc : 本代码未经授权禁止商用
import numpy as np
from factory.world import World
from factory.parameters import EMPTY


class Conveyor(object):

    def __init__(self, paths: list):
        self.paths = np.array(paths)

    def run(self):
        def output(world: World):
            world_map = world.states['map'][0]
            caught_obj = world_map[tuple(self.paths[-1])]
            if caught_obj != EMPTY:
                print("传送带尾部已放置物品")
            else:
                world_map[tuple(self.paths[1:].T)] = world_map[tuple(self.paths[:-1].T)]
                world_map[tuple(self.paths[0].T)] = EMPTY
        return output
