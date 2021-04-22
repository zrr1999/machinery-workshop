#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/27 10:07
# @Author : 詹荣瑞
# @File : parser.py
# @desc : 本代码未经授权禁止商用
import json
from pyparsing import Regex, Word, ZeroOrMore, Group, Suppress, Optional, nums, alphas

word = Regex(r"[\u4E00-\u9FA5A-Za-z0-9_]+")
commodity = word
tuple_parser = word + ZeroOrMore(Suppress(",") + word)
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
formula_parser = sources + Suppress("=") + commodities


def parse_statement(command_lines, world_dict):
    for line in command_lines:
        command, args = line
        if command == "material":
            args = tuple_parser.parseString(args)
            args[1] = int(args[1])
            world_dict["commodities"][args[0]] = [*args[1:], command, []]
        elif command == "equipment":
            args = tuple_parser.parseString(args)
            args[1] = int(args[1])
            world_dict["commodities"][args[0]] = [args[1], f"{command}/{args[2]}", []]
        elif command == "formula":
            s, t = formula_parser.parseString(args)
            world_dict["formulas"].append({
                "source": s,
                "target": t
            })


def parse_player(command_lines, world_dict):
    world_dict["playerState"] = {c[0]: eval(c[1]) for c in command_lines}


def parse_task(command_lines, world_dict):
    world_dict["task"] = [[c[0], task] for c in command_lines for task in eval(c[1])]


def parse_map(command_lines, world_dict):
    for line in command_lines:
        command, args = line
        args = eval(args)
        if command == "size":
            world_dict["mapSize"] = args
        else:
            world_dict["commodities"][command][2].extend(args)


parsers = {
    "statement": parse_statement,
    "player": parse_player,
    "map": parse_map,
    "task": parse_task,
}


class Parser(object):
    def __init__(self):
        self.world_dict = {}

    def parse(self, path: str):
        world_dict = {
            'mapLayer': 3,
            "formulas": [],
            "commodities": {},
            "task": [],
        }

        word = Regex(r"[\u4E00-\u9FA5A-Za-z0-9_]+")
        block_header = Suppress("%") + Word(alphas)
        block_command = Group(word + Suppress(":") + Regex(r".+"))
        block = Group(block_header + Group(ZeroOrMore(block_command)))
        parser = ZeroOrMore(block)
        with open(path, encoding="utf-8") as file:
            blocks = parser.parseString(file.read())

        for block in blocks:
            head, command_lines = block
            if head in parsers:
                parsers[head](command_lines, world_dict)
            else:
                print(head)
                print("")
        self.world_dict = world_dict
        with open(f"{path.replace('.mmap', '')}.json", 'w', encoding='utf-8') as file:
            json.dump(self.world_dict, file, ensure_ascii=False, indent=2)
        return self


def parse(path):
    return Parser().parse(path)


if __name__ == '__main__':
    print(parse("../../maps/task2.mmap").world_dict)
