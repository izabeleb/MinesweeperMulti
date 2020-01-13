"""Provides minesweeper utility functions."""
from typing import List
import pygame
from minesweeper import Cell, MineField
from theme.sprites import Box


def show_mines(box_group: pygame.sprite.Group, field: MineField):
    """Make all mines in the Minefield visible.

    Args:
        box_group (Group): The box group which to make mines visible.
        field (MineField): The field whose mines to make visible.
    """
    for box in box_group:
        cell = field.get_cell_at(*box.coords)
        if cell.is_mine and not cell.is_flag:
            box.set_bomb()
        elif not cell.is_mine and cell.is_flag:
            box.set_incorrectly_flagged()


def get_open_cells(field: MineField, cell: Cell) -> List[Cell]:
    """Get a list of open connected field cell coordinates.

    Args:
        field (MineField): the MineField to search for open and connected cells.
        cell (Cell): The starting cell from which to find open cells.

    Returns:
        (list): a list of all open and connected cells.
    """
    # TODO re-implement iteratively to safe stack space (especially for large boards)
    if cell.is_flag or cell.is_mine or not field.cell_is_safe(cell):
        return [cell]

    open_cells: list = list()
    cell.visited = True
    open_cells.append(cell)

    for cell in field.surrounding_cells(cell):
        open_cells.append(cell)

        if cell.is_flag or cell.visited or not field.cell_is_safe(cell):
            continue

        open_cells += get_open_cells(field, cell)

    return open_cells


def cell_to_box(boxes: list, field: MineField, cell: Cell) -> Box:
    """Get the Box instance corresponding to a cell from a list of boxes.

    Args:
        boxes (list): the list of boxes to pull from.
        field (MineField): the mine field of the cell.
        cell (Cell): the cell to find the corresponding box to.

    Returns:
        (Box): the box corresponding to the passed cell.
    """
    return boxes[field.max_col * cell.row + cell.col]
