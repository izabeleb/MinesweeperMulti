from minesweeper.game import MinesweeperGame
from minesweeper.cell import CellChange

from dataclasses import dataclass

from api.dao import Page


@dataclass(frozen=True)
class PostGameResponse:
    """Response to a crate game request."""
    game_url: str


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
    cell_changes: list[CellChange]


@dataclass(frozen=True)
class GetEventsResponse:
    pass
