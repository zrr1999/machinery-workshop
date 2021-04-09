#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 21:54
# @Author : 詹荣瑞
# @File : operation_base.py
# @desc : 本代码未经授权禁止商用
def sum_dict(dict1: dict, dict2: dict):
    for obj, num in dict2.items():
        if obj in dict1.keys():
            dict1[obj] += num
        else:
            dict1[obj] = num
    return dict1
