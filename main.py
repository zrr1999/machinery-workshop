#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory_preview import create_world_by_file
from factory_preview.extensions.conveyor import Conveyor
from factory_preview.extensions.container import Warehouse, Assembler
from factory_preview.extensions.sorter import Sorter
from factory_preview.core import SimpleFormula
import threading

# 初始化游戏读取地图
world, facilities = create_world_by_file(path="maps/task2.mmap", need_compile=True)

# 创建工作台并加载
warehouse = Warehouse((0, 0)).set({1: 100})  # 装入商品的仓库
assembler = Assembler((2, 2)).set_formula(SimpleFormula([1], 2))  # 制造台

sorter1 = Sorter(warehouse, (0, 1), 1)
sorter2 = Sorter((1, 2), assembler,  1)

conveyor = Conveyor([[0, 1], [1, 1], [1, 2]])  # 传送带


# 逻辑帧
def update():
    timer = threading.Timer(1.0, update)  # 每隔1s执行一步
    timer.start()
    # sorter2.run(world)  # 执行放入商品的分拣器
    # conveyor.run(world)  # 执行传送带
    # sorter1.run(world)  # 先执行取出商品的分拣器
    # assembler.run(world)
    print(world.get_map_layer())


update()
