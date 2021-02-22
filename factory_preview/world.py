#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/6 17:11
# @Author : 詹荣瑞
# @File : world.py
# @desc : 本代码未经授权禁止商用
import re
import yaml
from typing import Tuple, Union
from factory.core import MatrixState, VectorState
from factory.commodity import Commodity, Material
from factory.compiler import Compiler
from factory.utils.typing import Pos, Size
from factory.operation import Buy, Catch, Place, Sell
from factory.transaction import Market


# iron = Material(name="iron", price=5)  # 铁
# screw = Material(name="screw", price=15)  # 螺丝
# processor = Material(name="processor", price=20)  # 加工器
# materials = [iron, screw, processor]


class World(object):

    def __init__(self, size: Size = 5, coin:int=100):
        """

        """
        self.commodities = []
        self.market = Market()
        self.states = {}
        self.buy_ops = {}
        # self.compiler = Compiler()
        self.world_dict = {
            "player_state_value": [coin],
            "size": size
        }

        self.plugins = []

    def load_dict(self, path=None):
        with open(f"{path}.yaml", "r", encoding='utf-8') as file:
            self.world_dict = yaml.load(file, Loader=yaml.FullLoader)
        world_dict = self.world_dict
        self.commodities = []
        for c in world_dict["commodity"]:
            if c[2] == "material":
                c_obj = Material(name=c[0], price=c[1])
            else:
                c_obj = Material(name=c[0], price=c[1])
            self.commodities.append(c_obj)
        size, num = world_dict["size"], world_dict["layer_num"]
        state, value = world_dict["player_state"], world_dict["player_state_value"]
        self.market = Market(*self.commodities)
        self.states = {
            "map": MatrixState(size, num),  # Map state
            "player": VectorState(len(state), values=value, tag=state),  # Player state
            "market": self.market.state  # Market state
        }
        for c in self.commodities:
            positions = world_dict.get(c.name, ())
            for p in positions:
                self.place(eval(p), c.id)
        self.buy_ops = {m.name: Buy(m, (), self.market) for m in self.commodities}

    def save_dict(self, path):
        world_dict = self.world_dict
        with open(f"{path}.yaml", 'w', encoding='utf-8') as file:
            yaml.dump(world_dict, file, Dumper=yaml.Dumper)
        raise NotImplementedError

    def step(self):
        # print("updates")
        for p in self.plugins:
            p(self)

        return self.states

    def buy(self, commodity: Union[Commodity, str, int], position: Pos):
        if isinstance(commodity, str):
            buy = self.buy_ops.get(commodity)
        elif isinstance(commodity, int):
            buy = Buy(self.commodities[commodity], (), self.market)
        else:
            buy = Buy(commodity, (), self.market)
        buy.pos = position
        return buy(self.states)

    def sell(self, position: Pos):
        op = Sell(position, self.market)
        return op(self.states)

    def catch(self, position: Pos):
        op = Catch(position)
        return op(self.states)

    def place(self, position: Pos, obj: int = None):
        if obj is not None:
            op = Place(position, obj=obj)
            return op(self.states)

    def add_plugin(self, *func):
        self.plugins.extend(func)
