#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:39
# @Author : 詹荣瑞
# @File : operation_base.py
# @desc : 本代码未经授权禁止商用
from typing import Iterable, Dict
from factory_preview.core.state import StateBase
from factory.controller import Controller
from factory_preview.utils import sum_dict


class OperationBase(object):
    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, states: Dict[str, StateBase], controller: Controller = None) -> dict:
        raise NotImplementedError


class OperationSequence(OperationBase):
    def __init__(self, *ops: OperationBase):
        self.ops = ops

    def __call__(self, states: Dict[str, StateBase], controller: Controller = None):
        obj_dict = {}
        for op in self.ops:
            out = op(states, controller)
            if out is not None:
                sum_dict(obj_dict, out)
            else:
                break
        return obj_dict
