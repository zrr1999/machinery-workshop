#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/7 10:22
# @Author : 詹荣瑞
# @File : typing.py
# @desc : 本代码未经授权禁止商用
from typing import *
Position = NewType("Position", Tuple)

ObjID = TypeVar('ObjID', int, float)
Size = TypeVar("Size", Tuple[int, int], int)
Site = TypeVar("Site", Container, Position)
