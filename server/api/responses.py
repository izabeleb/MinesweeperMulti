from minesweeper.game import MinesweeperGame
from api.dao import Page

from typing import NamedTuple


class PostGameResponse(NamedTuple):
    """Response to a crate game request."""
    game_url: str

    def to_json(self):
        return {
            "game_url": self.game_url
        }


class GetPageResponse(NamedTuple):
    """Response to a resource page request."""
    page: Page

    def to_json(self):
        return self.page.to_json()


class GetGameResponse(NamedTuple):
    """Response to a field access request."""
    game: MinesweeperGame

    def to_json(self):
        return self.game.to_json()


class UpdateGameFieldResponse(NamedTuple):
    """Response to a field state update request."""
