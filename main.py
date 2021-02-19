#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory_preview import World
from factory import Compiler
from factory.extensions.conveyor import Conveyor
import bonegame
import threading


class DemoGame(bonegame.GoBang):
    obj = 0

    def key_event(self, key, action, modifiers):
        if action == "ACTION_PRESS":
            if key == ord('r'):
                world.step()
            elif key == ord(','):
                self.camera.yaw += 1
            elif key == ord('.'):
                self.camera.yaw -= 1
            elif key == ord('['):
                self.camera.pitch -= 5
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
                else:
                    world.place(pos, self.obj)
                    self.obj = None
                self.round += 1


SIZE = (9, 9)

# 编译地图文件（只需要一次）
compiler = Compiler()
compiler.compile(path="./compile_test")

# 初始化游戏读取地图
world = World()
world.load_dict(path="./compile_test")

# 创建传送带并加载
world.add_plugin(Conveyor(
    [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
))

# 显示游戏界面
game = DemoGame(SIZE)
print(world.states["player"])

# 逻辑帧
timer = threading.Timer(1.0, world.step)  # 每隔1s执行一步
timer.start()
while True:
    game.board.map = world.states['map'][0]  # 将逻辑地图复制到五子棋盘
    game.render()
