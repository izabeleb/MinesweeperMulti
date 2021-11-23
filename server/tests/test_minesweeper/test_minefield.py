import itertools

import unittest

from minesweeper.minefield import MineField


class TestMinefieldInit(unittest.TestCase):
    @staticmethod
    def _count_mines(mine_field: MineField) -> int:
        mine_count = 0

        for row in mine_field.cells:
            for cell in row:
                if cell.is_mine:
                    mine_count += 1

        return mine_count

    def test_correct_initialization(self):
        rows = 10
        cols = 10
        mine_count = 25

        mine_field = MineField(rows=rows, cols=cols, mine_count=mine_count)

        actual = self._count_mines(mine_field)
        expected = mine_count

        self.assertEqual(expected, actual)

    def test_test_small_full_mine_field(self):
        rows = 10
        cols = 10
        mine_count = rows * cols

        mine_field = MineField(rows=rows, cols=cols, mine_count=mine_count)

        actual = self._count_mines(mine_field)
        expected = mine_count

        self.assertEqual(expected, actual)

    def test_too_many_mines(self):
        rows = 10
        cols = 10
        mine_count = rows * cols + 1

        self.assertRaises(ValueError, MineField, rows=rows, cols=cols, mine_count=mine_count)

    def test_invalid_dimensions(self):
        rows = -1
        cols = -1
        mine_count = 5  # arbitrary value

        self.assertRaises(ValueError, MineField, rows=rows, cols=cols, mine_count=mine_count)


class TestMineField(unittest.TestCase):
    def setUp(self):
        self.rows = 4
        self.cols = 4
        self.mine_count = 0

        self.mine_field = MineField(rows=self.rows, cols=self.cols, mine_count=self.mine_count)

        self.maxDiff = None

    def test_get_empty_connected_all(self):
        #     0 1 2 3
        #   ┌─────────┐
        # 0 │ - - - - │
        # 1 │ - - - - │
        # 2 │ - - - - │
        # 3 │ - - - - │
        #   └─────────┘

        actual = sorted(self.mine_field.get_empty_connected(0, 0))
        expected = sorted(list(itertools.chain(*[[(i, j) for j in range(self.cols)] for i in range(self.rows)])))

        self.assertListEqual(expected, actual)

    def test_get_empty_connected_blocked(self):
        #     0 1 2 3
        #   ┌─────────┐
        # 0 │ - - - 1 │
        # 1 │ - - - 1 │
        # 2 │ - 1 1 1 │
        # 3 │ 1 1 - - │
        #   └─────────┘

        self.mine_field.cells[0][3].adjacent_mines = 1

        self.mine_field.cells[1][3].adjacent_mines = 1

        self.mine_field.cells[2][1].adjacent_mines = 1
        self.mine_field.cells[2][2].adjacent_mines = 1
        self.mine_field.cells[2][3].adjacent_mines = 1

        self.mine_field.cells[3][0].adjacent_mines = 1
        self.mine_field.cells[3][1].adjacent_mines = 1

        actual = sorted(self.mine_field.get_empty_connected(0, 0))
        expected = sorted([
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0)
        ])

        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
