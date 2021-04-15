#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
import json

import yaml
from factory_preview.core import MatrixState, VectorState, FormulaBase
from factory.commodity import Material, Equipment
from factory.compiler import Compiler
from factory_preview.compiler import Parser
from factory_preview.utils.typing import Position, Size, ObjID, List
from factory_preview.core.state import StateManager
from factory_preview.operations import ObjCatch, ObjPlace, Sell
from factory_preview.extensions import ExtensionBase, Warehouse, Assembler
from factory_preview.transaction import Market


# iron = Material(name="iron", price=5)  # 铁
# screw = Material(name="screw", price=15)  # 螺丝
# processor = Material(name="processor", price=20)  # 加工器
# materials = [iron, screw, processor]

def create_world_by_mmap(path: str):
    """

    :param path: 地图文件路径
    :return:
    """
    return create_world_by_dict(Parser().parse(path).world_dict)


def create_world_by_json(path: str):
    """

    :param path: 地图json文件路径
    :return:
    """
    with open(path, "r", encoding='utf-8') as file:
        world_dict = json.load(file)
    return create_world_by_dict(world_dict)


def create_world_by_dict(world_dict: dict):
    # 读取地图信息
    world = World(world_dict["mapSize"], world_dict["mapLayer"], world_dict["task"])
    # 读取公式信息
    formulas = world_dict["formulas"]
    # 读取商品信息并放置商品
    commodities = []
    materials, equipments = [], []

    for index, (name, args) in enumerate(world_dict["commodities"].items()):
        if args[1] == "material":
            materials.append(index + 1)
            c_obj = Material(name=name, price=args[0])
            commodities.append(c_obj)
            for p in args[2]:
                world.place(index + 1, tuple(p))
        elif "equipment" in args[1]:
            equipments.append(index + 1)
            c_obj = Equipment(name=name, price=args[0])
            commodities.append(c_obj)
            eps = args[2]
            if args[1] == "equipment/warehouse":
                for i in range(0, len(eps), 2):
                    world.add_extension(
                        Warehouse(eps[i]).set(eps[i + 1])
                    )
                    world.place(index + 1, tuple(eps[i]))
            elif args[1] == "equipment/assembler":
                for i in range(0, len(eps), 3):
                    f = formulas[eps[i + 2]]
                    f = FormulaBase(
                        f["source"],
                        f["target"]
                    )
                    formulas[eps[i + 2]] = f
                    world.add_extension(Assembler(eps[i]).set_formula(f).set(eps[i + 1]))
                    world.place(index + 1, tuple(eps[i]))
    # 读取市场信息
    world.market = Market(*commodities)
    for f in formulas:
        if isinstance(f, FormulaBase):
            f.format(world.market)
    # 读取玩家信息
    state = world_dict["playerState"]
    tags, values = list(state.keys()), list(state.values())
    world.state_manager.set_states({
        "player": VectorState(len(tags), values=values, tag=tags),  # Player state
    })

    return world, materials, equipments


def world2dict():
    pass
    # with open(f"{path}.yaml", 'w', encoding='utf-8') as file:
    #     yaml.dump(world_dict, file, Dumper=yaml.Dumper)


class World(object):

    def __init__(self, size: Size, layer_num: int = 3, tasks=None):
        """

        """
        self.commodities = []
        self.market = Market()
        # self.states = {}
        self.state_manager = StateManager().set_states({
            "map": MatrixState(size, layer_num),  # Map state
            "player": VectorState(2, values=[100, 1], tag=["coin", "level"]),  # Player state
            "market": self.market.state,
        })
        self.buy_ops = {}
        self.extensions: List[ExtensionBase] = []
        self.tasks = tasks or []

    def get_map_layer(self, n_layer: int = 0):
        return self.state_manager.get("map")[n_layer]

    def get_map_value(self, pos: Position, n_layer: int = 0):
        return self.get_map_layer(n_layer)[tuple(pos)]

    def get_player_all_values(self):
        return self.state_manager.get("player")[:]

    def get_player_value(self, index: int):
        return self.state_manager.get("player")[index]

    def buy(self, obj_id: ObjID, position: Position):
        return self.state_manager.operate(self.market.buy(obj_id, position))

    def sell(self, position: Position):
        obj = ObjCatch(position)(self.state_manager.states_dict)
        if obj is not None:
            sell = Sell(obj, self.market)
            sell(self.state_manager.states_dict)
        return {}

    def catch(self, position: Position):
        op = ObjCatch(position)
        return op(self.state_manager.states_dict)

    def place(self, obj_id: ObjID, position: Position):
        op = ObjPlace(obj_id, position)
        return op(self.state_manager.states_dict)

    def add_extension(self, *extensions: ExtensionBase):
        self.extensions.extend(extensions)

    def update(self):
        for extension in self.extensions:
            extension.run(self)
        for t in self.tasks:
            target, (index, value) = t
            index = tuple(index)
            if target == "map" and self.state_manager.get(target)[index] != value:
                return False
            if target == "player" and self.state_manager.get(target)[index] != value:
                return False
        return True


if __name__ == '__main__':
    world, mts, eqs = create_world_by_mmap(
        "../maps/task1.mmap"
    )

    print(world, mts, eqs)
    print(world.update())
