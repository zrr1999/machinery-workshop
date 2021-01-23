#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/20 22:09
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from factory import World
from factory import Compiler
import bonegame


class DemoGame(bonegame.GoBang):
    obj = 0

    def key_event(self, key, action, modifiers):
        if action == "ACTION_PRESS":
            if key == ord(','):
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

compiler = Compiler()
world = World()
game = DemoGame(SIZE)
compiler.compile(path="./compile_test")
world.load_dict(path="./compile_test")
print(world.states["player"])
print(world.states['map'][0])
while True:
    game.board.map = world.states['map'][0]
    game.render()
