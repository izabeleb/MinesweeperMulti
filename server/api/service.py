from api.responses import PostGameResponse, GetPageResponse, GetGameResponse, UpdateGameFieldResponse
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest

from minesweeper.game import MinesweeperGame

from api.dao import MemoryStore

from typing import Optional


class MinesweeperService:
    def __init__(self, store: Optional[MemoryStore]):
        self._store = MemoryStore() if store is None else store

    def create_game(self, request: PostGameRequest) -> PostGameResponse:
        """Creates a new minefield."""
        game = MinesweeperGame(request.height, request.width, request.mine_count)

        self._store.add_game(game)
        response = PostGameResponse(f"/game/{game.id}")  # todo: add url resolver

        return response

    def get_game_page(self, request: GetPageRequest) -> GetPageResponse:
        """Retrieve a list of all game uuids."""
        return GetPageResponse(self._store.get_page(request.page, request.size))

    def get_game(self, request: GetGameRequest) -> GetGameResponse:
        """Retrieve the game with the specified uuid."""
        game = self._store.get_game(request.game_id)

        response = GetGameResponse(game)

        return response

    def update_game(self, request: UpdateGameFieldRequest) -> UpdateGameFieldResponse:
        """Update the board state.

        todo: send update events to stream to update all connected clients
        """
        game = self._store.get_game(request.game_id)
        minefield = game.minefield

        row = request.row
        col = request.col

        new_state = request.new_state

        _cell = minefield.cells[row][col].state = new_state

        return UpdateGameFieldResponse()
