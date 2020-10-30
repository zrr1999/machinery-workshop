#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:21
# @Author : 詹荣瑞
# @File : controller.py
# @desc : 本代码未经授权禁止商用
from collections.abc import Iterable


class Controller(object):

    def __init__(self):
        self.parallel_sequence = []
        self.serial_sequence = []

    def __str__(self):
        return (f"Parallel Sequence: {str(self.parallel_sequence)}\n"
                f"Serial Sequence: \n{str(self.serial_sequence)}")

    def step(self, states):
        if not isinstance(states, Iterable):
            states = [states]
        if self.serial_sequence:
            op = self.serial_sequence.pop(0)
            op(states, self)
        for operation in self.parallel_sequence:
            operation(states, self)

    def add_sequence(self, ps=None, ss=None):
        if ps:
            self.parallel_sequence += ps
        if ss:
            self.serial_sequence += ss
        return self


if __name__ == '__main__':
    from factory.state import MapState
    from factory.operation import Move
    states = {
        "ms": MapState(),
    }
    m12 = Move((0, 1, 1), (0, 2, 1))
    m21 = Move((0, 2, 1), (0, 1, 1))
