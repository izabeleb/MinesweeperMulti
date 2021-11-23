from uuid import UUID

from minesweeper.game import MinesweeperGame


class MemoryStore:
    def __init__(self):
        self.games = dict()

    def add_game(self, game: MinesweeperGame):
        self.games[game.id] = game

    def get_game(self, game_id: UUID) -> MinesweeperGame:
        return self.games[game_id]

    # todo: return page rather than all ids
    def get_all_games(self) -> list[MinesweeperGame]:
        return list(self.games.values())
