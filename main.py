#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory import World

world = World()

# c = Controller().add_sequence(ss=[init]).step(s)


for i in range(4):
    print(f"第{i + 1}次循环")
    print(world.state)
    world.buy(0, (0, 0, 0))
    print(world.state)
    world.move(i+1)
