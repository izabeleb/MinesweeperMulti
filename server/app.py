from enum import Enum

import flask
from flask import Flask

import json
from json import JSONEncoder

from minesweeper.minefield import MineField
from minesweeper.cell import Cell
from minesweeper.game import MinesweeperGame

from api.service import MinesweeperService
from api.requests import *

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
        elif isinstance(obj, MinesweeperGame):
            return {
                "created_at": obj.created_at.timestamp(),
                "url": f"/game/{obj.id}"
            }
        else:
            return json.JSONEncoder().default(obj)


@app.route("/games")
def get_games():
    """Handle GET requests for all games."""
    response = minesweeper_service.get_games()

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/games", methods=["POST"])
def post_game():
    """Handle POST requests to create a game."""
    body_json = flask.request.json

    if body_json is None:
        flask.abort(400)

    request = PostGameRequest(**body_json)
    response = minesweeper_service.create_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/game/<game_id>", methods=["GET"])
def get_game(game_id: str):
    """Handle GET requests to retrieve a game."""
    request = GetGameRequest(UUID(game_id))
    response = minesweeper_service.get_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)


@app.route("/game/<game_id>/field", methods=["UPDATE"])
def put_game(game_id: UUID):
    """Handle PUT requests to update the board state."""
    body_json = flask.request.json

    if body_json is None:
        flask.abort(400)

    request = UpdateGameFieldRequest(game_id=game_id, **body_json)
    response = minesweeper_service.update_game(request)

    return json.dumps(response, cls=MinesweeperEncoder)
