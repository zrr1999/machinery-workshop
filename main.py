#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory.state import MapState, PlayerState
from factory.operation import Move, Buy
from factory.controller import Controller
from factory.material import Material, iron


def init(states, controller):
    ps = states["ps"].state
    ps[0] = 100

    m12 = Move((0, 1, 1), (0, 2, 1))
    m21 = Move((0, 2, 1), (0, 1, 1))
    b1 = Buy(38, 5, (0, 1, 1))
    controller.add_sequence(ps=[m12], ss=[b1, m21, m21, m21, m21, m21, m21, m21])


s = {
    "ms": MapState(),
    "ps": PlayerState(),
}
c = Controller().add_sequence(ss=[init])

for i in range(5):
    print(f"第{i}次循环")
    print(s)
    # print(c)
    c.step(s)

