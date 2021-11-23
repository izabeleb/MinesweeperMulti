from minesweeper.game import MinesweeperGame

from typing import NamedTuple


class PostGameResponse(NamedTuple):
    """Response to a crate game request."""
    game_url: str

    def to_json(self):
        return {
            "game_url": self.game_url
        }


class GetGamesResponse(NamedTuple):
    """Response to a field query."""
    games: list[MinesweeperGame]

    def to_json(self):
        return [game.to_json() for game in self.games]


class GetGameResponse(NamedTuple):
    """Response to a field access request."""
    game: MinesweeperGame

    def to_json(self):
        return self.game.to_json()


class UpdateGameFieldResponse(NamedTuple):
    """Response to a field state update request."""
