# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:05:27 2019

@author: bauzy
"""
from mode import Mode
from multiplayer.Client import run_client
import pygame
import minesweeper
import menus
import enterHostnamePort
pygame.init()


def program():
    """
    This program directs the flow of control

    Contains the menu, singleplayer, etc.
    """

    donePlaying = False
    game_mode: Mode = Mode.restore_mode()

    while not donePlaying:

        donePlaying, command = menus.mainMenu()

        if not donePlaying:

            if command == "singlePlayer":
                minesweeper.main(game_mode)
            elif command == "multiPlayer":
                # hostname, port = enterHostnamePort.main()
                hostname = 'localhost'  # '192.168.0.10'
                port = 8080
                run_client(hostname, port, game_mode)
            elif command == "settings":
                donePlaying, game_mode = menus.settingsMenu()

    pygame.quit()
    game_mode.store_mode()


if __name__ == '__main__':
    program()
