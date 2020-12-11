#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/13 9:36
# @Author : 詹荣瑞
# @File : test.py
# @desc : 本代码未经授权禁止商用
import re
pattern = re.compile(r"([A-z]+): *(.*)")
mov_pattern = re.compile(r"([A-z]+): *(.*)")

op, arg = pattern.search("mov:[[0,1,1],[0,2,1]]").groups()
print(op, eval(arg))
print(pattern.search("mov: [02 1 1], [0 2 1]").groups())

