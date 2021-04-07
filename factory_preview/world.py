#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
import re
import yaml
from factory_preview.core import MatrixState, VectorState, FormulaBase, SimpleFormula
from factory.commodity import Commodity, Material, Equipment
from factory_preview.compiler import compiler
from factory_preview.utils.typing import Position, Size, Tuple, Union, ObjID, List
from factory_preview.core.state import StateManager
from factory_preview.operation import Buy, Catch, Place, Sell
from factory_preview.extensions import ExtensionBase, Warehouse, Assembler
from factory.transaction import Market


# iron = Material(name="iron", price=5)  # 铁
# screw = Material(name="screw", price=15)  # 螺丝
# processor = Material(name="processor", price=20)  # 加工器
# materials = [iron, screw, processor]

def create_world_by_file(path: str, need_compile: bool = False):
    """

    :param path: 地图文件路径
    :param need_compile: 是否需要编译地图文件
    :return:
    """
    if need_compile:
        compiler.compile(path)
    with open(f"{path}.yaml", "r", encoding='utf-8') as file:
        world_dict = yaml.load(file, Loader=yaml.FullLoader)
    return create_world_by_dict(world_dict)


def create_world_by_dict(world_dict: dict):
    world_dict.setdefault("layer_num", 3)
    print(world_dict)
    # 读取地图信息
    size, num = world_dict["size"], world_dict["layer_num"]
    world = World(size, num)
    # 读取商品信息并放置商品
    commodities = []
    facilities = []
    for c in world_dict["commodities"]:
        if c[2] == "material":
            c_obj = Material(name=c[0], price=c[1])
        elif c[2] == "equipment":
            c_obj = Equipment(name=c[0], price=c[1])
            eps = world_dict.get(c[0], ())
            if c[3] == "warehouse":
                for i in range(0, len(eps), 2):
                    facilities.append(
                        Warehouse(eps[i]).set(eps[i + 1])
                    )
            elif c[3] == "assembler":
                for i in range(0, len(eps), 3):
                    formula = world_dict["formulas"][eps[i+2]]
                    facilities.append(Assembler(eps[i]).set_formula(
                        FormulaBase(
                            formula["source"],
                            formula["target"]
                        )
                    ).set(eps[i + 1]))

        else:
            c_obj = Material(name=c[0], price=c[1])
        commodities.append(c_obj)
    # 读取玩家信息
    state, value = world_dict["player_state"], world_dict["player_state_value"]
    world.state_manager.set_states({
        "player": VectorState(len(state), values=value, tag=state),  # Player state
    })
    # 读取市场信息
    world.market = Market(*commodities)

    for m in commodities:
        positions = world_dict.get(m.name, ())
        for p in positions:
            if isinstance(p, Tuple):
                world.place(p, m.id)

    return world, facilities


def world2dict():
    pass
    # with open(f"{path}.yaml", 'w', encoding='utf-8') as file:
    #     yaml.dump(world_dict, file, Dumper=yaml.Dumper)


class World(object):

    def __init__(self, size: Size, layer_num: int = 3):
        """

        """
        self.commodities = []
        self.market = Market()
        # self.states = {}
        self.state_manager = StateManager().set_states({
            "map": MatrixState(size, layer_num),  # Map state
            "player": VectorState(2, values=[100, 1], tag=["coin", "level"]),  # Player state
        })
        self.buy_ops = {}
        self.extensions: List[ExtensionBase] = []

    def get_map_layer(self, n_layer: int = 0):
        return self.state_manager.get("map")[n_layer]

    def get_map_value(self, pos: Position, n_layer: int = 0):
        return self.get_map_layer(n_layer)[tuple(pos)]

    def get_player_value(self, index: int):
        return self.state_manager.get("player")[index]

    def buy(self, obj_id: ObjID, position: Position):
        return self.state_manager.operate(self.market.buy(obj_id, position))

    def sell(self, position: Position):
        op = Sell(position, self.market)
        return op(self.state_manager.states_dict)

    def catch(self, position: Position):
        op = Catch(position)
        return op(self.state_manager.states_dict)

    def place(self, position: Position, obj_id: ObjID):
        op = Place(position, obj_id)
        return op(self.state_manager.states_dict)

    def add_extension(self, *extensions: ExtensionBase):
        self.extensions.extend(extensions)

    def update(self):
        for extension in self.extensions:
            extension.run(self)
