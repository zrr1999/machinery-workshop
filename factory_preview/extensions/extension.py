#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/7 22:00
# @Author : 詹荣瑞
# @File : extension.py
# @desc : 本代码未经授权禁止商用
class ExtensionBase(object):
    def run(self, world):
        raise NotImplementedError
