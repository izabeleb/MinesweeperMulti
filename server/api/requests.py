from typing import NamedTuple

from uuid import UUID

from minesweeper.cell import CellState


class PostGameRequest(NamedTuple):
    """Request to create a new mine sweeper game."""
    width: int = 10
    height: int = 10
    mine_count: int = 10


class GetPageRequest(NamedTuple):
    """Request for a page of a certain resource."""
    page: int
    size: int


class GetGameRequest(NamedTuple):
    """Request for a specific game."""
    game_id: UUID


class UpdateGameFieldRequest(NamedTuple):
    """Request to update the state of the game field."""
    game_id: UUID
    row: int
    col: int
    new_state: CellState
