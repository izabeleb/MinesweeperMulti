from uuid import UUID

import flask
from flask import Flask

from api.service import MemoryStore, MinesweeperService
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest, GetGameEventsRequest

from minesweeper.cell import CellChange

from typing import Optional, Any

import datetime


class MinesweeperEncoder(flask.json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, datetime.datetime):
            return obj.timestamp()

        return super().default(obj)


def create_app(store: Optional[MemoryStore] = None):
    app = Flask(__name__)

    app.json_encoder = MinesweeperEncoder

    minesweeper_service = MinesweeperService(store)

    @app.route("/games", methods=["GET"])
    def get_games():
        """Handle GET requests for all games."""
        page: int = int(flask.request.args.get("page", 0))
        size: int = int(flask.request.args.get("size", 10))

        request = GetPageRequest(page, size)
        response = minesweeper_service.get_game_page(request)

        return flask.jsonify(response)

    @app.route("/games", methods=["POST"])
    def post_game():
        """Handle POST requests to create a game."""
        body_json = flask.request.json

        if body_json is None:
            flask.abort(400)

        request = PostGameRequest(**body_json)

        try:
            response = minesweeper_service.create_game(request)
            return flask.jsonify(response)
        except ValueError:  # todo: make errors types to allow for more specificity
            flask.abort(400)

    @app.route("/game/<game_id>", methods=["GET"])
    def get_game(game_id: str):
        """Handle GET requests to retrieve a game."""
        request = GetGameRequest(UUID(game_id))
        response = minesweeper_service.get_game(request)

        if response is None:
            flask.abort(404)

        return flask.jsonify(response)

    @app.route("/game/<game_id>/field", methods=["PATCH"])
    def patch_game(game_id: str):
        """Handle PUT requests to update the board state."""
        body_json = flask.request.json

        if body_json is None:
            flask.abort(400)

        request = UpdateGameFieldRequest(id=UUID(game_id), cell_change=CellChange(**body_json["cell_change"]))
        response = minesweeper_service.update_game(request)

        if response is None:
            flask.abort(404)

        return flask.jsonify(response)

    @app.route("/game/<game_id>/events")
    def get_events(game_id: str):
        body_json = flask.request.json

        if body_json is not None and "since" in body_json:
            request = GetGameEventsRequest(UUID(game_id), datetime.datetime.fromtimestamp(body_json["since"]))
        else:
            request = GetGameEventsRequest(UUID(game_id))

        response = minesweeper_service.get_game_events(request)

        if response is None:
            flask.abort(404)

        return flask.jsonify(response)

    @app.route("/health", methods=["GET"])
    def get_health():
        return "ok"

    return app
