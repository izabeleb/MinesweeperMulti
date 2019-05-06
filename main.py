# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:05:27 2019

@author: bauzy
"""
from settings import Mode
import pygame
import minesweeper
import menu
import settings
pygame.init()


def program():
    """
    This program directs the flow of control
    
    Contains the menu, singleplayer, etc. 
    """

    donePlaying = False
    game_mode: Mode = Mode.restore_mode()
    
    while not donePlaying:
        
        donePlaying, command = menu.main()

        if not donePlaying:
            
            print(command)
            
            if command == "singlePlayer":
                minesweeper.main()
                
            elif command == "multiPlayer":
                
                pass
            
            elif command == "settings":
                donePlaying, game_mode = settings.main()
                print(game_mode.mode_to_dict())

    pygame.quit()
    game_mode.store_mode()
    
program()