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

global_data = {}
app = APIFlask(__name__)


class JsonRpcInSchema(Schema):
    jsonrpc = String(required=True, validate=OneOf(["2.0"]))
    method = String(required=True)
    params = List(Field, required=True)
    id = Number(required=True)


class JsonRpcOutSchema(Schema):
    jsonrpc = String(required=True, validate=OneOf(["2.0"]))
    result = Field(required=True)
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
        world.add_extension(*facilities)
    elif data["method"] == "update":
        if world is not None:
            world.update()
    elif data["method"] == "action":
        x, y = data["params"]
        world.buy(1, (0, y, x))
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
    app.run(port=6954)
