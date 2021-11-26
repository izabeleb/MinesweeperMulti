from api.responses import (
    PostGameResponse, GetPageResponse, GetGameResponse, UpdateGameFieldResponse, GetGameEventsResponse,
    GetGameFieldResponse
)
from api.requests import (
    PostGameRequest, GetGameRequest, UpdateGameFieldRequest, GetPageRequest, GetGameEventsRequest, GetGameFieldRequest
)

from minesweeper.game import MinesweeperGame, EventType, GameEvent
from minesweeper.cell import CellStatus, CellChange

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
        """Update the board state."""
        cell_change = request.cell_change

        is_mine_hit = self._store.set_cell_state(request.id, cell_change.row, cell_change.col, cell_change.state)

        if is_mine_hit is None:
            return None

        return UpdateGameFieldResponse(is_mine_hit)

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
