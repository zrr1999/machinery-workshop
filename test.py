#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/13 9:36
# @Author : 詹荣瑞
# @File : test.py
# @desc : 本代码未经授权禁止商用
import pyglet
from pyglet.window import Window
from pyglet.shapes import Circle
from pyglet.sprite import Sprite
window = Window(600, 400)
c = Circle(25, 25, 20)


@window.event
def on_draw():
    window.clear()

    c.draw()


pyglet.app.run()

