from enum import Enum

import flask
from flask import Flask

import json
from json import JSONEncoder

from minesweeper.minefield import MineField
from minesweeper.cell import Cell

from service import MinesweeperService
from requests import *

app = Flask(__name__)


minesweeper_service = MinesweeperService()


class MinesweeperEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, MineField):
            return obj.cells  # todo: we probably want to change this
        elif isinstance(obj, Cell):
            return {
                "col": obj.col,
                "row": obj.row,
                "is_mine": obj.is_mine,
                "state": obj.state
            }
        elif isinstance(obj, Enum):
            return str(obj)
        else:
            return json.JSONEncoder().default(obj)


@app.route("/games")
def get_games():
    """Handle GET requests for all games."""
    response = minesweeper_service.get_games()

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/game", methods=["POST"])
def post_game():
    """Handle POST requests to create a game."""
    body_json = flask.request.json

    if body_json is None:
        flask.abort(400)

    request = PostGameRequest(**body_json)
    response = minesweeper_service.create_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/game/<game_uuid>", methods=["GET"])
def get_game(game_uuid: str):
    """Handle GET requests to retrieve a game."""
    request = GetGameRequest(UUID(game_uuid))
    response = minesweeper_service.get_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/game/<game_uuid>/state", methods=["PUT"])
def put_game(game_uuid: UUID):
    """Handle PUT requests to update the board state."""
    body_json = flask.request.json

    if body_json is None:
        flask.abort(400)

    request = PutGameStateRequest(game_uuid=game_uuid, **body_json)
    response = minesweeper_service.update_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)
