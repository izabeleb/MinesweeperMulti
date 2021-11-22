from minesweeper.minefield import MineField

import uuid
from uuid import UUID

from responses import PostGameResponse, GetGameIdsResponse, GetGameResponse, PutGameResponse
from requests import PostGameRequest, GetGameRequest, PutGameStateRequest


class MemoryStore:
    def __init__(self):
        self.fields = dict()

    def add_game(self, game_uuid: UUID, field: MineField):
        self.fields[game_uuid] = field

    def get_game(self, game_uuid: UUID) -> MineField:
        return self.fields[game_uuid]

    def get_all_game_ids(self) -> list[UUID]:
        return [i for i in self.fields.keys()]


class MinesweeperService:
    def __init__(self):
        self._store = MemoryStore()

        response = self.create_game(PostGameRequest(width=10, height=10, mine_count=10))
        self._store.add_game(response.game_uuid, response.mine_field)

    def create_game(self, request: PostGameRequest) -> PostGameResponse:
        """Creates a new minefield."""
        game_uuid = uuid.uuid4()
        field = MineField(rows=request.width, cols=request.height, mine_count=request.mine_count)

        self._store.add_game(game_uuid, field)
        response = PostGameResponse(game_uuid, field)

        return response

    def get_games(self) -> GetGameIdsResponse:
        """Retrieve a list of all game uuids."""
        return GetGameIdsResponse(self._store.get_all_game_ids())

    def get_game(self, request: GetGameRequest) -> GetGameResponse:
        """Retrieve the game with the specified uuid."""
        field = self._store.get_game(request.game_uuid)

        response = GetGameResponse(field)

        return response

    def update_game(self, request: PutGameStateRequest) -> PutGameResponse:
        """Update the board state.

        todo: send update events to stream to update all connected clients
        """
        mine_field = self._store.get_game(request.game_uuid)

        row = request.row
        col = request.col

        new_state = request.new_state

        _cell = mine_field.cells[row][col].state = new_state

        return PutGameResponse()
