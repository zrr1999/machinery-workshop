#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/13 9:36
# @Author : 詹荣瑞
# @File : test.py
# @desc : 本代码未经授权禁止商用
import taichi as ti
import tina

ti.init(ti.cpu)

# you may specify the line width for rendering wireframes:
# taa=True turns on Temporal Anti-Aliasing to make lines smoother
scene = tina.Scene(linewidth=2, taa=True)

# load the monkey using `tina.MeshModel` node (`tina.SimpleMesh` works too):
model = tina.MeshModel('assets/monkey.obj')
# convert the mesh to its wireframe using the `tina.MeshToWire` node:
wiremodel = tina.MeshToWire(model)

# add the wireframe model into scene:
scene.add_object(wiremodel)

# add the original model, with a tiny scale:
model = tina.MeshTransform(model, tina.scale(0.9))
scene.add_object(model)

gui = ti.GUI('wireframe')

while gui.running:
    scene.input(gui)
    scene.render()
    gui.set_image(scene.img)
    gui.show()
