#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/27 10:07
# @Author : 詹荣瑞
# @File : compiler.py
# @desc : 本代码未经授权禁止商用
import re
from factory.core.state import MatrixState, VectorState
from factory.commodity.material import Material
from factory.utils.typing import Pos, Size
from factory.operation import Buy, Catch, Place, Sell
from factory.transaction import Market


class Compiler(object):

    def __init__(self):
        self.world_dict = {
            "size": (5, 5),
            "num": 3,
            "coin": 100,

            "commodity": [
                ("iron", 5),
                ("screw", 15),
                ("processor", 20)
            ],
        }

    def __call__(self, path):
        region = re.compile(r"% *(.+)")
        command = re.compile(r"(.+): *(.+)")
        self.world_dict["commodity"] = []
        with open(path, 'r', encoding="utf-8") as file:
            for line in file.readlines():
                res = region.search(line)
                if res is None:
                    res = command.search(line)
                    if res is not None:
                        self.compile_line(current, *res.groups())
                else:
                    current = res.group(1)

    def compile_line(self, current, command, args):
        if command == "material":
            name, price = args.split(" ")
            self.world_dict["commodity"].append((name, int(price)))


if __name__ == '__main__':
    player = Compiler()

    region = re.compile(r"% *(.+)")
    command = re.compile(r"(.+): *(.+)")

    current = None
    with open("../../compile_test", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            res = region.search(line)
            if res is None:
                res = command.search(line)
                current(*res.groups())
            else:
                current = eval(res.group(1))




