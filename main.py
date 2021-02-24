#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory_preview import World, create_world_by_file
from factory import Compiler
from factory.extensions.conveyor import Conveyor
from factory.extensions.warehouse import Warehouse
import bonegame
import threading

get = True


class DemoGame(bonegame.GoBang):
    obj = 0

    def key_event(self, key, action, modifiers):
        global get
        if action == "ACTION_PRESS":
            if key == ord('r'):
                world.step()
            elif key == ord('z'):
                get = not get
            elif key == ord('w'):
                self.select_pos[1] += 1
            elif key == ord('a'):
                self.select_pos[0] -= 1
            elif key == ord('s'):
                self.select_pos[1] -= 1
            elif key == ord('d'):
                self.select_pos[0] += 1
            elif key == ord('b'):
                pos = (0, self.board.w // 2 - self.select_pos[1],
                       -self.board.h // 2 + self.select_pos[0])
                world.buy(0, pos)
            elif key == ord('q'):
                pos = (0, self.board.w // 2 - self.select_pos[1],
                       -self.board.h // 2 + self.select_pos[0])
                world.sell(pos)
            elif key == ord(' '):
                pos = (0, self.board.w // 2 - self.select_pos[1],
                       -self.board.h // 2 + self.select_pos[0])
                if self.round % 2 == 0:
                    self.obj = world.catch(pos)
                    if self.obj:
                        self.round += 1
                else:
                    world.place(pos, self.obj)
                    self.obj = None
                    self.round += 1


SIZE = (9, 9)

# 初始化游戏读取地图
world = create_world_by_file(path="maps/compile_test", need_compile=True)

# 创建工作台并加载
warehouse1 = Warehouse((0, 0)).set({1: 100})  # 仓库
conveyor = Conveyor([[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]])  # 传送带
warehouse2 = Warehouse((2, 2))


# 逻辑帧
def update():
    timer = threading.Timer(1.0, update)  # 每隔1s执行一步
    timer.start()
    if not get:
        warehouse1.run(1)(world)
    conveyor.run()(world)
    if get:
        warehouse2.run(1, True)(world)


update()

# 显示游戏界面
game = DemoGame(SIZE)
print(world.state_manager.states_dict["player"])
while True:
    game.board.map = world.get_map_layer(0)  # 将逻辑地图复制到五子棋盘
    game.render()
