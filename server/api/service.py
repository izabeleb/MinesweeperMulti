from api.responses import (
    PostGameResponse, GetPageResponse, GetGameResponse, UpdateGameFieldResponse, GetGameEventsResponse,
    GetGameFieldResponse
)
from api.requests import (
    PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest, GetGameEventsRequest, GetGameFieldRequest
)

from minesweeper.game import MinesweeperGame, EventType, GameEvent
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
        response = PostGameResponse(game.id)

        game.events.append(GameEvent(EventType.GameStart, {}))

        return response

    def get_game_page(self, request: GetPageRequest) -> GetPageResponse:
        """Retrieve a list of all game uuids."""
        return GetPageResponse(self._store.get_page(request.page, request.size))

    def get_game(self, request: GetGameRequest) -> Optional[GetGameResponse]:
        """Retrieve the game with the specified uuid."""
        game = self._store.get_game(request.id)

        if game is None:
            return None

        response = GetGameResponse(game)

        return response

    def update_game(self, request: UpdateGameFieldRequest) -> Optional[UpdateGameFieldResponse]:
        """Update the board state.

        todo: send update events to stream to update all connected clients
        """
        response = self.get_game(GetGameRequest(request.id))

        if response is None:
            return None

        game = response.game

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

        for change in cell_changes:
            game.events.append(GameEvent(EventType.CellChange, change))

        if is_mine_hit:
            game.events.append(GameEvent(EventType.GameEnd, {}))

        return UpdateGameFieldResponse(is_mine_hit, cell_changes)

    def get_game_events(self, request: GetGameEventsRequest) -> Optional[GetGameEventsResponse]:
        response = self.get_game(GetGameRequest(request.id))

        if response is None:
            return None

        game = response.game
        since = request.since

        if since is not None:
            events = list(filter(lambda event: event.occurred_at.timestamp() >= since.timestamp(), game.events))
        else:
            events = game.events

        return GetGameEventsResponse(events)

    def get_game_field(self, request: GetGameFieldRequest) -> Optional[GetGameFieldResponse]:
        game = self._store.get_game(request.id)

        if game is None:
            return None

        cells = game.minefield.cells

        return GetGameFieldResponse(cells)
