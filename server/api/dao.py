from dataclasses import dataclass

from uuid import UUID

from minesweeper.game import MinesweeperGame

from typing import Any


@dataclass
class Page:
    page: int

    size: int

    data: list[Any]

    def to_json(self):
        return {
            "page": self.page,
            "size": self.size,
            "data": [i.to_json() for i in self.data]
        }


# todo: we probably want some base class so we can implement multiple wrappers around storage mechanisms
class MemoryStore:
    def __init__(self):
        self.games = dict()

    def add_game(self, game: MinesweeperGame):
        self.games[game.id] = game

    def get_game(self, game_id: UUID) -> MinesweeperGame:
        return self.games[game_id]

    def get_page(self, page: int, size: int) -> Page:
        games = sorted(self.games.values(),
                       key=lambda game: game.created_at)[size * (page - 1): size * (page - 1) + size]

        return Page(page, size, games)
