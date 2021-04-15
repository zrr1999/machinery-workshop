#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/27 10:07
# @Author : 詹荣瑞
# @File : compiler.py
# @desc : 本代码未经授权禁止商用
import re
import json
from pyparsing import Regex, nums, Word, ZeroOrMore, Group, Suppress, Optional


class Compiler(object):
    """
    完成 material，
    """

    def __init__(self):
        self.world_dict = {
        }

    def compile(self, path: str):
        word = r"[\u4E00-\u9FA5A-Za-z0-9_]"
        region = re.compile(r"%\s*(\S+)")
        command = re.compile(r"(\S+):\s*(.+)")

        self.world_dict["commodities"] = []
        self.world_dict["formulas"] = []
        with open(path, 'r', encoding="utf-8") as file:
            for line in file.readlines():
                res = region.search(line)
                if res is None:
                    res = command.search(line)
                    if res is not None:
                        self.compile_line(current, *res.groups())
                else:
                    current = res.group(1)

        with open(f"{path.replace('.mmap', '')}.json", 'w', encoding='utf-8') as file:
            json.dump(self.world_dict, file, ensure_ascii=False, indent=2)
        return self

    def compile_line(self, current, command, args):
        if current == "player":
            if command == "vec":
                self.world_dict["player_state"] = args.split(" ")
            elif command == "initial":
                self.world_dict["player_state_value"] = list(map(eval, args.split(" ")))
        elif current == "task":
            pass
        else:
            if command == "material":
                name, price = args.split(" ")
                self.world_dict["commodities"].append(
                    (name, int(price), command)
                )
            elif command == "equipment":
                name, price, ep = args.split(" ")
                self.world_dict["commodities"].append(
                    (name, int(price), command, ep)
                )
            elif command == "size":
                self.world_dict["size"] = eval(args)
            elif command == "formula":
                commodity = Regex(r"[\u4E00-\u9FA5A-Za-z0-9_]+")
                commodities = commodity + Optional(Suppress("*") + Word(nums)).addParseAction(
                    lambda res: int(res[0]) if res else 1
                )
                commodities.addParseAction(lambda res: {
                    res[0]: res[1]
                })
                sources = commodities + ZeroOrMore(Suppress("+") + commodities)
                sources.addParseAction(lambda res: {
                    k: v for rd in res for k, v in rd.items()
                })
                parser_formula = sources + Suppress("=") + commodities
                s, t = parser_formula.parseString(args)
                self.world_dict["formulas"].append({
                    "source": s,
                    "target": t
                })
            else:
                self.world_dict.setdefault(command, [])
                self.world_dict[command].extend(eval(args))


def compile(path):
    return Compiler().compile(path)


if __name__ == '__main__':
    print(compile("../../maps/task3.mmap").world_dict)

