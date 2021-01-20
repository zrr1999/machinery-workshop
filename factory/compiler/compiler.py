#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/27 10:07
# @Author : 詹荣瑞
# @File : compiler.py
# @desc : 本代码未经授权禁止商用
import re
from typing import List, Tuple
from factory.core.state import MatrixState, VectorState
from factory.commodity.material import Material
from factory.utils.typing import Pos, Size
from factory.operation import Buy, Catch, Place, Sell
from factory.transaction import Market


class Compiler(object):
    """
    完成 material，
    """

    def __init__(self):
        self.world_dict = {
            "size": (5, 5),
            "layer_num": 3,
            "player_state": ["coin", "level"],
            "player_state_value": [100, 0],

            "commodity": [
                ("iron", 5, "material"),
                ("screw", 15, "material"),
                ("processor", 20, "material")
            ],
        }

    def __call__(self, path: str):
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
            self.world_dict["commodity"].append((name, int(price), "material"))
        elif command == "size":
            self.world_dict["size"] = eval(args)
        elif command == "vec":
            if current == "player":
                self.world_dict["player_state"] = args.split(" ")
        elif command == "initial":
            if current == "player":
                self.world_dict["player_state_value"] = args.split(" ")
