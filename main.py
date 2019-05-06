# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:05:27 2019

@author: bauzy
"""

import pygame
pygame.init()
import minesweeper, menu

def program():
    """
    This program directs the flow of control
    
    Contains the menu, singleplayer, etc. 
    """

    donePlaying = False
    
    while not donePlaying:
        
        donePlaying, command = menu.main()

        if not donePlaying:
            
            print(command)
            
            if command == "singlePlayer":
                minesweeper.main()
                
            elif command == "multiPlayer":
                
                pass
            
            elif command == "settings":
                
                pass

    pygame.quit()
    
program()