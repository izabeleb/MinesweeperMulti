from uuid import UUID

import flask
from flask import Flask

from api.service import MemoryStore, MinesweeperService
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest

from typing import Optional


# todo: add health check
def create_app(store: Optional[MemoryStore] = None):
    app = Flask(__name__)

    minesweeper_service = MinesweeperService(store)

    @app.route("/games", methods=["GET"])
    def get_games():
        """Handle GET requests for all games."""
        page: int = int(flask.request.args.get("page", 0))
        size: int = int(flask.request.args.get("size", 10))

        request = GetPageRequest(page, size)
        response = minesweeper_service.get_game_page(request)

        return flask.jsonify(response.to_json())

    @app.route("/games", methods=["POST"])
    def post_game():
        """Handle POST requests to create a game."""
        body_json = flask.request.json

        if body_json is None:
            flask.abort(400)

        request = PostGameRequest(**body_json)
        response = minesweeper_service.create_game(request)

        return flask.jsonify(response.to_json())

    @app.route("/game/<game_id>", methods=["GET"])
    def get_game(game_id: str):
        """Handle GET requests to retrieve a game."""
        request = GetGameRequest(UUID(game_id))
        response = minesweeper_service.get_game(request)

        return flask.jsonify(response.to_json())

    @app.route("/game/<game_id>/field", methods=["UPDATE"])
    def put_game(game_id: UUID):
        """Handle PUT requests to update the board state."""
        body_json = flask.request.json

        if body_json is None:
            flask.abort(400)

        request = UpdateGameFieldRequest(game_id=game_id, **body_json)
        response = minesweeper_service.update_game(request)

        return flask.jsonify(response)

    @app.route("/health", methods=["GET"])
    def get_health():
        return "ok"

    return app
