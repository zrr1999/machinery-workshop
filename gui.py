#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/30 12:53
# @Author : 詹荣瑞
# @File : gui.py
# @desc : 本代码未经授权禁止商用
import PySimpleGUI as sg
# from factory import World
sg.theme('DarkAmber')  # 界面主题

operation = sg.InputText()
last_op = sg.Text(size=(18, 1))
layout = [[sg.Text('地图调试', font=('Helvetica', 15))],
          [sg.Text('上一个操作'), last_op],
          [sg.Text('输入命令'), operation],
          [sg.Button('确定')]]  # 窗口布局

window = sg.Window('机械工坊功能调试器', layout, return_keyboard_events=True)  # 创建窗口
# world = World(6)
while True:
    event, values = window.read()
    # print(event)
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    elif event == '确定' or event == "\r":  # if user closes window or clicks cancel
        operation.update('')
        last_op.update(values[0])
        # try:
            # op, arg = world.analyze(values[0])
            # print(op, arg)
        # except AttributeError:
        #     pass
    elif event == "Up:38":
        operation.update(last_op.get())

window.close()
