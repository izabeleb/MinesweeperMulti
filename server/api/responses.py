from minesweeper.game import MinesweeperGame
from minesweeper.cell import CellChange

from dataclasses import dataclass

from api.dao import Page


@dataclass(frozen=True)
class PostGameResponse:
    """Response to a crate game request."""
    game_url: str

    def to_json(self):
        return {
            "game_url": self.game_url
        }


@dataclass(frozen=True)
class GetPageResponse:
    """Response to a resource page request."""
    page: Page

    def to_json(self):
        return self.page.to_json()


@dataclass(frozen=True)
class GetGameResponse:
    """Response to a field access request."""
    game: MinesweeperGame

    def to_json(self):
        return self.game.to_json()


@dataclass(frozen=True)
class UpdateGameFieldResponse:
    """Response to a field state update request."""
    is_mine_hit: bool
    cell_changes: list[CellChange]

    def to_json(self):
        return {
            "is_mine_hit": self.is_mine_hit,
            "cell_changes": [i.to_json() for i in self.cell_changes]
        }
