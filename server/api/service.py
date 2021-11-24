from api.responses import PostGameResponse, GetPageResponse, GetGameResponse, UpdateGameFieldResponse
from api.requests import PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest

from minesweeper.game import MinesweeperGame
from minesweeper.cell import CellState, CellChange

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

        cell_change = request.cell_change

        cell = minefield.cells[cell_change.row][cell_change.col]

        is_mine_hit = False
        cell_changes: list[CellChange] = list()

        if cell_change.state == CellState.Flag:
            if cell.state == CellState.Closed:
                cell.state = cell_change.state
                cell_changes.append(cell_change)

        elif cell_change.state == CellState.Open:
            if cell.state == CellState.Closed:
                if cell.is_mine:
                    is_mine_hit = True
                elif cell.state != CellState.Open:
                    for coordinate in minefield.get_empty_connected(cell_change.row, cell_change.col):
                        empty_cell = minefield.cells[coordinate[0]][coordinate[1]]
                        empty_cell.state = CellState.Open

                        cell_changes.append(CellChange(coordinate[0], coordinate[1], CellState.Open))

        elif cell_change.state == CellState.Closed:
            if cell.state == CellState.Flag:
                cell.state = CellState.Closed

                cell_changes.append(cell_change)
        else:
            raise ValueError(f"unsupported cell state '{cell_change.state}'")

        return UpdateGameFieldResponse(is_mine_hit, cell_changes)
