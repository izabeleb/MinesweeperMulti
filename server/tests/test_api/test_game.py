import app

import unittest

from api.service import MemoryStore

from minesweeper.game import MinesweeperGame


class TestGetGame(unittest.TestCase):
    def setUp(self):
        self._game_0 = MinesweeperGame(10, 10, 10)
        self._game_1 = MinesweeperGame(10, 10, 10)
        self._game_2 = MinesweeperGame(10, 10, 10)
        self._game_3 = MinesweeperGame(10, 10, 10)
        self._game_4 = MinesweeperGame(10, 10, 10)

        self._sorted_games = sorted([
                                        self._game_0,
                                        self._game_1,
                                        self._game_2,
                                        self._game_3,
                                        self._game_4
                                    ],
                                    key=lambda game: game.created_at)

        self._store = MemoryStore()
        self._store.add_game(self._game_0)
        self._store.add_game(self._game_1)
        self._store.add_game(self._game_2)
        self._store.add_game(self._game_3)
        self._store.add_game(self._game_4)

        self._client = app.create_app(self._store).test_client()

    def test_get_game(self):
        response = self._client.get(f"/game/{self._game_0.id}")

        actual = response.json
        expected = {
            'created_at': self._game_0.created_at.timestamp(),
            'url': f'/game/{self._game_0.id}'
        }

        self.assertEqual(expected, actual)

    def test_get_page_size_3(self):
        response = self._client.get(f"/games?page=1&size=3")
        self.assertListEqual(response.json["data"], [i.to_json() for i in [self._game_0, self._game_1, self._game_2]])

        response = self._client.get(f"/games?page=2&size=3")
        print(response.json["data"])
        print([i.to_json() for i in [self._game_3, self._game_4]])
        self.assertListEqual(response.json["data"], [i.to_json() for i in [self._game_3, self._game_4]])
