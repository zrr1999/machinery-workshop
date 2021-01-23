#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/13 9:36
# @Author : 詹荣瑞
# @File : test.py
# @desc : 本代码未经授权禁止商用
class A(object):

    def __init__(self):
        self.name = "a"


c = r"""
class $NAME$(A):
    
    def __init__(self):
        self.name = "$NAME$"
"""
name = "MyName"
exec(c.replace("$NAME$", name))
print(eval(f"{name}()").name)
