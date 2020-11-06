#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory.state import MatrixState, VectorState
from factory.operation import Move, Buy
from factory.controller import Controller
from factory.material import Material, iron
from factory.market import Market


def init(states, controller):
    ps = states["ps"].state
    ps[0] = 100

    m12 = Move((0, 1, 1), (0, 2, 1))
    m21 = Move((0, 2, 1), (0, 1, 1))
    m = Market(iron)
    b1 = Buy(iron, (0, 1, 1), market=m)
    controller.add_sequence(ps=[m12], ss=[b1, m21, m21, m21, m21, m21, m21, m21])


s = {
    "ms": MatrixState(),  # Map state
    "ps": VectorState(),  # Player state
}
c = Controller().add_sequence(ss=[init]).step(s)

for i in range(5):
    print(f"第{i+1}次循环")
    print(s)
    # print(c)
    c.step(s)

