# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:05:27 2019

@author: bauzy
The main entry point for the game.
"""
import pygame
from menu.menus import *
from multiplayer.client import run_client
from minesweeper.minesweeper import run_minesweeper

pygame.init()


def program():
    """This program directs the flow of control

    Contains the menu, single player, etc.
    """
    done_playing = False
    game_mode: Mode = Mode.restore_mode()

    while not done_playing:
        done_playing, command = initial()

        if not done_playing:
            if command == "singlePlayer":
                run_minesweeper(game_mode)
            elif command == "multiPlayer":
                hostname, port = build_input_menu("Hostname", "Port")
                run_client(hostname, port, game_mode)
            elif command == "settings":
                done_playing, game_mode = settings()

    pygame.quit()
    game_mode.store_mode()


if __name__ == '__main__':
    program()
