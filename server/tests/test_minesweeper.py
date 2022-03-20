import itertools
import unittest
import time

from minesweeper.minefield import MineField
from minesweeper.cell import Cell, Coordinate


class TestMinefieldInit(unittest.TestCase):
    @staticmethod
    def _count_mines(mine_field: MineField) -> int:
        mine_count = 0

        for row in mine_field.cells:
            for cell in row:
                if cell.is_mine:
                    mine_count += 1

        return mine_count

    def _assert_cell(self, cell: Cell, is_mine: bool, adjacent_mines: int):
        self.assertEqual(is_mine, cell.is_mine)
        self.assertEqual(adjacent_mines, cell.adjacent_mines)

    def test_correct_initialization(self):
        rows = 10
        cols = 10
        mine_count = 10

        mine_field = MineField(rows=rows, cols=cols, mine_count=mine_count)

        actual = self._count_mines(mine_field)
        expected = mine_count

        self.assertEqual(expected, actual)

    def test_large_initialization(self):
        rows = 999
        cols = 999
        mine_count = rows * cols

        start = time.time()
        mine_field = MineField(rows=rows, cols=cols, mine_count=mine_count)
        delta = time.time() - start

        actual = self._count_mines(mine_field)
        expected = mine_count

        self.assertEqual(expected, actual)
        self.assertLess(delta, 2.5,
                        msg="This may fail if there was no '__pycache__' so if it fails on the first attempt run again")

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

    def test_correct_numbers(self):
        #     0 1 2 3
        #   ┌─────────┐
        # 0 │ 1 * 1 0 │
        # 1 │ 1 2 2 1 │
        # 2 │ 1 2 * 1 │
        # 3 │ * 2 1 1 │
        #   └─────────┘

        rows = 4
        cols = 4
        mine_count = 0

        mine_field = MineField(rows=rows, cols=cols, mine_count=mine_count)

        mine_field.set_mine(Coordinate(0, 1))
        mine_field.set_mine(Coordinate(2, 2))
        mine_field.set_mine(Coordinate(3, 0))

        self._assert_cell(mine_field.cells[0][0], False, 1)
        self._assert_cell(mine_field.cells[0][1], True, 0)
        self._assert_cell(mine_field.cells[0][2], False, 1)
        self._assert_cell(mine_field.cells[0][3], False, 0)

        self._assert_cell(mine_field.cells[1][0], False, 1)
        self._assert_cell(mine_field.cells[1][1], False, 2)
        self._assert_cell(mine_field.cells[1][2], False, 2)
        self._assert_cell(mine_field.cells[1][3], False, 1)

        self._assert_cell(mine_field.cells[2][0], False, 1)
        self._assert_cell(mine_field.cells[2][1], False, 2)
        self._assert_cell(mine_field.cells[2][2], True, 0)
        self._assert_cell(mine_field.cells[2][3], False, 1)

        self._assert_cell(mine_field.cells[3][0], True, 0)
        self._assert_cell(mine_field.cells[3][1], False, 2)
        self._assert_cell(mine_field.cells[3][2], False, 1)
        self._assert_cell(mine_field.cells[3][3], False, 1)


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

        actual = sorted(self.mine_field.get_empty_connected(Coordinate(0, 0)))
        expected = sorted(list(itertools.chain(*[[(i, j) for j in range(self.cols)] for i in range(self.rows)])))

        self.assertListEqual(expected, actual)

    def test_get_empty_connected_blocked(self):
        #     0 1 2 3
        #   ┌─────────┐
        # 0 │ 1 1 1 - │
        # 1 │ 2 * 2 - │
        # 2 │ 2 * 2 - │
        # 3 │ 1 1 1 - │
        #   └─────────┘

        self.mine_field.set_mine(Coordinate(1, 1))
        self.mine_field.set_mine(Coordinate(2, 1))

        actual = sorted(self.mine_field.get_empty_connected(Coordinate(0, 0)))
        expected = sorted([
            (0, 0),
        ])

        self.assertListEqual(expected, actual)

        actual = sorted(self.mine_field.get_empty_connected(Coordinate(0, 3)))
        expected = sorted([
            (0, 2), (0, 3),
            (1, 2), (1, 3),
            (2, 2), (2, 3),
            (3, 2), (3, 3),
        ])

        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
