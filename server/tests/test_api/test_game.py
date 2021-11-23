import app

import unittest

from api.service import MemoryStore

from minesweeper.game import MinesweeperGame

from uuid import UUID


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


class TestPutGame(unittest.TestCase):
    def setUp(self):
        self._store = MemoryStore()

        self._client = app.create_app(self._store).test_client()

    def test_no_body(self):
        response = self._client.post("/games", data={})

        self.assertEqual(400, response.status_code)

    def test_unrecognized_field(self):
        response = self._client.post("/games", data={
            "unrecognized_field": "unrecognized_value"
        })

        self.assertEqual(400, response.status_code)

    def test_basic_field(self):
        response = self._client.post("/games", json={
            "width": 10,
            "height": 10,
            "mine_count": 10
        })

        response_json = response.json
        game_url = response_json["game_url"]
        game_id = UUID(game_url.split("/")[-1])

        game = self._store.get_game(game_id)

        self.assertEqual(10, game.minefield.rows)
        self.assertEqual(10, game.minefield.cols)
        self.assertEqual(10, game.minefield.mine_count)

    def test_bad_field_dimensions(self):
        response = self._client.post("/games", json={
            "width": 10,
            "height": -1,
            "mine_count": 10
        })

        self.assertEqual(400, response.status_code)
