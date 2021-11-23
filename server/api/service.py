from api.responses import PostGameResponse, GetGamesResponse, GetGameResponse, UpdateGameFieldResponse
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest

from minesweeper.game import MinesweeperGame

from api.dao import MemoryStore


class MinesweeperService:
    def __init__(self):
        self._store = MemoryStore()

        game = MinesweeperGame(10, 10, 10)
        self._store.add_game(game)

    def create_game(self, request: PostGameRequest) -> PostGameResponse:
        """Creates a new minefield."""
        game = MinesweeperGame(request.height, request.width, request.mine_count)

        self._store.add_game(game)
        response = PostGameResponse(f"/game/{game.id}")  # todo: add url resolver

        return response

    def get_games(self) -> GetGamesResponse:
        """Retrieve a list of all game uuids."""
        return GetGamesResponse(self._store.get_all_games())

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
