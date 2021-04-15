#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 17:12
# @Author : 詹荣瑞
# @File : server.py
# @desc : 本代码未经授权禁止商用
import code
import os
from apiflask import APIFlask, Schema, input, output
from apiflask.fields import String, Number, List, Field
from apiflask.validators import Length, OneOf
from flask import request, jsonify

from factory_preview import create_world_by_file
from factory_preview.extensions.conveyor import Conveyor

global_data = {}
app = APIFlask(__name__)


class JsonRpcInSchema(Schema):
    jsonrpc = String(required=True, validate=OneOf(["2.0"]))
    method = String(required=True)
    params = List(Field, required=True)
    id = Number(required=True)


class JsonRpcOutSchema(Schema):
    jsonrpc = String(required=True, validate=OneOf(["2.0"]))
    result = List(Field, required=True)
    id = Number(required=True)


@app.get("/get_pid")
def get_pid():
    return jsonify({
        "pid": os.getpid()
    })


@app.post("/mw_map_editor")
@input(JsonRpcInSchema)
def map_editor(data):
    return jsonify({"1": 1})


@app.post("/mw_debug")
@input(JsonRpcInSchema)
def debug(data):
    response = {
        "jsonrpc": "2.0",
        "id": data['id'],
        "result": []
    }
    world = global_data.get('world', None)
    if data["method"] == "start":
        world, facilities = create_world_by_file(path="maps/task3.mmap", need_compile=True)
        global_data['world'], global_data['facilities'] = world, facilities
        conveyor = Conveyor([[0, 1], [1, 1], [1, 2]])  # 传送带
        world.add_extension(*facilities, conveyor)
    elif data["method"] == "update":
        if world is not None:
            world.update()
    elif "action" in data["method"]:
        if world is not None:
            x, y = data["params"]
            if data["method"] == "action/buy":
                world.buy(1, (0, y, x))
            else:
                world.sell((0, y, x))

    response["result"] = [
        world.get_map_layer().tolist(),
        world.get_player_all_values().tolist()
    ]
    return jsonify(response)


@app.route('/open_file', methods=["POST"])
def open_file():
    (filepath, filename_ex) = os.path.split(data['path'])
    (filename, extension) = os.path.splitext(filename_ex)
    os.chdir(filepath)
    print(os.path.join(filepath, filename))
    interpreter.runcode(
        f"_compiler = Compiler(_doc, r'{os.path.join(filepath, filename)}', "
        f"compilers='xelatex')"
    )
    return jsonify({
        "success": True
    })


@app.route('/save', methods=['POST'])
def save():
    success = True
    try:
        with open(data["dir"], mode="w", encoding="utf-8") as file:
            file.write(data["code"].replace("\r\n", "\n"))
    except FileNotFoundError:
        success = False

    return jsonify({
        "success": success
    })


if __name__ == '__main__':
    app.run(port=7474)
    test_dict = {
        'mapSize': [13, 13],
        'mapLayer': 3,

        'formulas': [],
        'commodities': [
            ['铁', 5, 'material', [[0, 0, 3], [0, 0, 4], [0, 1, 3]]],
            ['铁棍', 8, 'material', [[0, 1, 4]]],
            ['仓库', 100, 'equipment/warehouse', [[0, 0, 0], {}]]
        ],

        'playerState': [['金币数', 100], ['等级', 1]],

        "target": [
            ["map", [1, [0, 0, 3]]],
            ["player", [1, 200]],
        ]
    }
