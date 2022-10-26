import random

from minesweeper.cell import Cell, CellStatus, Coordinate


class MineField:
    def __init__(self, rows: int, cols: int, mine_count: int):
        """Representation of a minesweeper field."""

        if mine_count > rows * cols:
            raise ValueError("mine_count may not be greater than the amount of cells")

        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count

        self.cells = [
            [Cell(Coordinate(i, j)) for j in range(self.cols)]
            for i in range(self.rows)
        ]

        self._establish_mines()

    def _establish_mines(self):
        rand_range = random.sample(range(self.cols * self.rows), k=self.mine_count)

        for flat_coordinate in rand_range:
            row = flat_coordinate // self.rows
            col = flat_coordinate % self.cols

            self.set_mine(Coordinate(row, col))

    def _get_adjacent_cells(self, coordinate: Coordinate) -> list[Cell]:
        cells = list()

        for i in range(-1, 2):
            if not (0 <= coordinate.row + i < self.rows):
                continue

            for j in range(-1, 2):
                if i == j == 0 or not (0 <= coordinate.col + j < self.cols):
                    continue

                cells.append(self.cells[coordinate.row + i][coordinate.col + j])

        return cells

    def get_empty_connected(self, coordinate: Coordinate) -> list[Coordinate]:
        """Retrieves a list of coordinates of cells which are empty, including the starting coordinate."""
        safe_coordinates: list[Coordinate] = list()
        next_cells: set[Cell] = {self.cells[coordinate.row][coordinate.col]}
        visited_cells = set()

        while next_cells:
            cell = next_cells.pop()

            if not cell.is_mine:
                safe_coordinates.append(cell.coordinate)

                if cell.adjacent_mines == 0:
                    next_cells |= {adjacent_cell for adjacent_cell in self._get_adjacent_cells(cell.coordinate)
                                   if adjacent_cell not in visited_cells}

            visited_cells.add(cell)

        return safe_coordinates

    def set_mine(self, coordinate: Coordinate):
        if not self.cells[coordinate.row][coordinate.col].is_mine:
            self.cells[coordinate.row][coordinate.col].is_mine = True

            for cell in self._get_adjacent_cells(coordinate):
                cell.adjacent_mines += 1

    def get_closed_mines(self) -> list[Coordinate]:
        """Get a list of the locations any closed cells which are mines."""
        locations: list[Coordinate] = list()

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]

                if cell.is_mine:
                    locations.append(cell.coordinate)

        return locations

    def is_field_clear(self) -> bool:
        """Determine if the MineField is clear (all non-mine cells are opened)."""
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                if not cell.is_mine and cell.status != CellStatus.Opened:
                    return False
        return True

    def get_cell(self, coordinate: Coordinate) -> Cell:
        return self.cells[coordinate.row][coordinate.col]
