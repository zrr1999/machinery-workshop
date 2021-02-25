#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:26
# @Author : 詹荣瑞
# @File : state.py
# @desc : 本代码未经授权禁止商用
from factory_preview.utils.typing import Union, Size, Dict, Any, Callable
import numpy as np


class StateBase(object):

    def __init__(self, state, tag):
        self.state = state
        self.tag = tag

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __str__(self):
        return str(self.state.tolist())

    def __repr__(self):
        return str(self)


class MatrixState(StateBase):
    """
    矩阵状态是一个状态类，具有状态和标签两个属性，
    状态是一个尺寸为 n * h * w 的张量，
    其中 n 为层数，分别为状态的高度和宽度。
    """

    def __init__(self, size: Size = 3, num_layers: int = 1, values=None, dtype=np.int, tag=None):
        """

        :param size: 状态的尺寸，即 (h, w)
        :param num_layers: 状态的层数，即 n
        :param values: 状态初始值
        :param dtype: 状态数据类型
        :param tag: 暂时仅作标注
        """
        if isinstance(size, int):
            height = width = size
        else:
            height, width = size
        s = np.zeros((num_layers, height, width), dtype)
        if values is not None:
            s[:] = values
        super(MatrixState, self).__init__(np.zeros((num_layers, height, width), dtype), None)


class VectorState(StateBase):

    def __init__(self, n_state: int = 1, values=None, dtype=None, tag: list = None):
        """

        :param n_state: 状态个数
        :param values: 状态初始值
        :param dtype: 状态数据类型
        :param tag: 仅作标注
        """
        s = np.zeros(n_state, dtype)
        if values is not None:
            s[:] = values
        super().__init__(s, tag)

    def __str__(self):
        if self.tag is None:
            self.tag = []
        self.tag += ["undefined"]*(len(self.state) - len(self.tag))
        out = "["
        out += ", ".join(f"{t}({s})" for s, t in zip(self.state, self.tag))
        out += "]"
        return out


class ManagerBase(object):
    Type = Any

    def __init__(self):
        self.states_dict = {}
        self.states_list = []

    def set(self, state: Type, target: str = None):
        if target is not None:
            self.states_dict.update({target: state})
            self.states_list.append(state)
        return self

    def set_states(self, states: Dict[Any, Type]) -> "ManagerBase":
        self.states_dict.update(states)
        self.states_list.extend(list(states.values()))
        return self

    def get(self, target: Union[str, int]):
        if isinstance(target, str):
            return self.states_dict[target]
        else:
            return self.states_list[target]


class StateManager(ManagerBase):
    Type = StateBase

    def operate(self, func: Callable[[dict], Any]):
        return func(self.states_dict)
