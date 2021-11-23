from uuid import UUID

import flask
from flask import Flask

from api.service import MemoryStore, MinesweeperService
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest

from typing import Optional


# # todo: move these definitions into their respective classes
# # todo: keeps returning lists
# class MinesweeperEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, GetGameResponse):
#             return obj.to_json()
#         if isinstance(obj, UUID):
#             return str(obj)
#         elif isinstance(obj, MineField):
#             return obj.cells  # todo: we probably want to change this
#         elif isinstance(obj, Cell):
#             return {
#                 "col": obj.col,
#                 "row": obj.row,
#                 "is_mine": obj.is_mine,
#                 "state": obj.state
#             }
#         elif isinstance(obj, Enum):
#             return str(obj)
#         elif isinstance(obj, MinesweeperGame):
#             return {
#                 "created_at": obj.created_at.timestamp(),
#                 "url": f"/game/{obj.id}"
#             }
#         else:
#             return super().default(obj)


# todo: add health check
def create_app(store: Optional[MemoryStore] = None):
    app = Flask(__name__)

    minesweeper_service = MinesweeperService(store)

    @app.route("/games", methods=["GET"])
    def get_games():
        """Handle GET requests for all games."""
        response = minesweeper_service.get_games()

        return flask.jsonify(response)

    @app.route("/games", methods=["POST"])
    def post_game():
        """Handle POST requests to create a game."""
        body_json = flask.request.json

        if body_json is None:
            flask.abort(400)

        request = PostGameRequest(**body_json)
        response = minesweeper_service.create_game(request)

        return flask.jsonify(response)

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
