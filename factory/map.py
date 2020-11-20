#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/19 21:38
# @Author : 詹荣瑞
# @File : map.py
# @desc : 本代码未经授权禁止商用
from factory.utils.typing import Pos
from .core import MatrixState
from .commodity import Commodity


class Map(object):

    def __init__(self, height: int = 3, width: int = 3, ):
        """
        地图中的每个格子具有三个属性，放置物品编号、物品类型和物品特殊属性。
        物品类型中，0代表一般物体、1代表可执行物体，2代表地图装饰物（不可改变）。

        :param height: 地图高度
        :param width: 地图宽度
        """
        self.state = MatrixState((height, width), 3)
        self.shape = (height, width, 3)

    def pop(self, index: Pos):
        """

        :param index: 目标索引
        :return: 操作成功返回目标值，操作失败返回0
        """
        s = self.state[index]
        if s[1] == 2:
            return 0
        else:
            self.state[index] = 0
            return s

    def push(self, index: Pos, obj: Commodity):
        """

        :param index: 目标索引
        :param obj: 目标值
        :return: 操作成功返回1，操作失败返回0
        """
        s = self.state[index]
        if s[0] != 0:
            return 0
        else:
            self.state[index] = (obj.id, obj.type, 0)
            return 1
