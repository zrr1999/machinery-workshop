#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 17:12
# @Author : 詹荣瑞
# @File : server.py
# @desc : 本代码未经授权禁止商用
import code
import os
# from apiflask import APIFlask, Schema, input, output
# from apiflask.fields import String, Number, List, Field
# from apiflask.validators import Length, OneOf
# from flask import request, jsonify
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Dict
from enum import Enum

from factory_preview import create_world_by_mmap
from factory_preview.extensions.conveyor import Conveyor

global_data = {}
app = FastAPI()


class JsonRpc(str, Enum):
    v2 = "2.0"


class Params(BaseModel):
    # method = start or update
    task: int = None
    # method = buy or sell
    x: int = None
    y: int = None
    select: int = None


class Result(BaseModel):
    map: list = None
    player: list = None
    success: bool = False


class JsonRpcIn(BaseModel):
    jsonrpc: str = Body("2.0", regex=r"2[.]0")
    method: str = Body(..., regex=r".*")
    params: Params
    id: int


class JsonRpcOut(BaseModel):
    jsonrpc: JsonRpc = "2.0"
    result: Result
    id: int


@app.get("/get_pid")
def get_pid():
    return {
        "pid": os.getpid()
    }


@app.post("/mw_map_editor", response_model=JsonRpcOut)
def map_editor(data: JsonRpcIn):
    return {
        "id": data.id,
        "jsonrpc": "2.0",
        "result": {
            "map": world.get_map_layer().tolist(),
            "player": world.get_player_all_values().tolist()
        }
    }


@app.post("/mw_debug", response_model=JsonRpcOut)
def debug(data: JsonRpcIn):
    world = global_data.get('world', None)
    if data.method == "start":
        world, _, _ = create_world_by_mmap(path=f"maps/task{data.params.task}.mmap")
        global_data['world'], global_data['facilities'] = world, []
        conveyor = Conveyor([[0, 1], [1, 1], [1, 2]])  # 传送带
        world.add_extension(conveyor)
    elif data.method == "update":
        if world is not None:
            world.update()
    elif "action" in data.method:
        if world is not None:
            x, y, select = data.params.x, data.params.y, data.params.select
            if data.method == "action/buy":
                world.buy(select, (0, y, x))
            else:
                world.sell((0, y, x))

    return {
        "id": data.id,
        "jsonrpc": "2.0",
        "result": {
            "map": world.get_map_layer().tolist(),
            "player": world.get_player_all_values().tolist(),
            "success": world.success
        }
    }


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
    import uvicorn

    uvicorn.run("server:app", port=7474, reload=True, debug=True)
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
