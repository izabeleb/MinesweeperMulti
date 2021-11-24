from dataclasses import dataclass

from uuid import UUID

from minesweeper.cell import CellChange


@dataclass(frozen=True)
class PostGameRequest:
    """Request to create a new mine sweeper game."""
    width: int = 10
    height: int = 10
    mine_count: int = 10


@dataclass(frozen=True)
class GetPageRequest:
    """Request for a page of a certain resource."""
    page: int
    size: int


@dataclass(frozen=True)
class GetGameRequest:
    """Request for a specific game."""
    game_id: UUID


@dataclass(frozen=True)
class UpdateGameFieldRequest:
    """Request to update the state of the game field."""
    game_id: UUID
    cell_change: CellChange
