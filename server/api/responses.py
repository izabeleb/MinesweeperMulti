from minesweeper.game import GameEvent, MinesweeperGame
from minesweeper.cell import CellChange, Cell

from dataclasses import dataclass

from api.dao import Page

from uuid import UUID


@dataclass(frozen=True)
class PostGameResponse:
    """Response to a crate game request."""
    id: UUID


@dataclass(frozen=True)
class GetPageResponse:
    """Response to a resource page request."""
    page: Page


@dataclass(frozen=True)
class GetGameResponse:
    """Response to a field access request."""
    game: MinesweeperGame


@dataclass(frozen=True)
class UpdateGameFieldResponse:
    """Response to a field state update request."""
    is_mine_hit: bool


@dataclass(frozen=True)
class GetGameEventsResponse:
    """A to a game events access request."""
    events: list[GameEvent]


@dataclass(frozen=True)
class GetGameFieldResponse:
    """A response to a game field access request."""
    cells: list[list[Cell]]
