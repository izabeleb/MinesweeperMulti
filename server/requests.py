from typing import NamedTuple

from uuid import UUID

from minesweeper.cell import CellState


class PostGameRequest(NamedTuple):
    """Request to create a new mine sweeper game."""
    width: int = 10
    height: int = 10
    mine_count: int = 10


class GetGameRequest(NamedTuple):
    """Request for a specific game."""
    game_uuid: UUID


class PutGameStateRequest(NamedTuple):
    """Request to update the state of the board."""
    game_uuid: UUID
    row: int
    col: int
    new_state: CellState
