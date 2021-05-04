# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:47:01 2019

@author: bauzy
Generate menus for user interaction.
"""
from __future__ import annotations
from typing import Tuple
from typing import TYPE_CHECKING
import sys
from menu import build_input_menu
from menu import build_simple_menu
from minesweeper import Mode

if TYPE_CHECKING:
    from minesweeper import Mode


def settings() -> Tuple[bool, Mode]:
    """Create settings menu, and control settings workflow."""
    title = "Settings"
    options = [["mode_easy", "Easy"],
               ["mode_normal", "Normal"],
               ["mode_hard", "Hard"],
               ["mode_custom", "Custom"],
               ["email", "Email"],
               ["exit", "Return to main menu"]]

    _, target_button = build_simple_menu(title, options)

    game_mode = Mode.restore_mode()

    if target_button == 'mode_easy':
        game_mode = Mode(Mode.EASY)
    elif target_button == 'mode_normal':
        game_mode = Mode(Mode.NORMAL)
    elif target_button == 'mode_hard':
        game_mode = Mode(Mode.HARD)
    elif target_button == 'mode_custom':
        height, width, bombs = build_input_menu("Height", "Width", "Number of Bombs")

        # TODO add more robust conversions
        if height == "":
            height = 20
            bombs = None

        if width == "":
            width = 20
            bombs = None

        # craps up the gamebar widget and others if the width is tiny
        # TODO find a way to notify the player that the width can't be smaller than 10, maybe
        #  restrict height too
        elif int(width) < 10:
            width = 10

        if bombs is None:
            game_mode = Mode.build(height, width, 10, None)
        else:
            game_mode = Mode.build(height, width, bombs, None)
    elif target_button == 'email':
        email = build_input_menu("Email")[0]
        game_mode = Mode.build(game_mode.height(), game_mode.width(), game_mode.bomb_count(), email)
    else:
        print(f"Unknown item selected: {target_button}", file=sys.stderr)

    return False, game_mode


def initial():
    """Create the initial user menu."""
    title = "Minesweeper"
    button_list = [["singlePlayer", "Single Player"],
                   ["multiPlayer", "Multiplayer"],
                   ["settings", "Settings"]]
    return build_simple_menu(title, button_list)
