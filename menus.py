# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:47:01 2019

@author: bauzy
"""

import pygame
from mode import Mode
import menuBase, inputBase

pygame.init()

def settingsMenu() -> tuple:
    
    title = "Settings"
    options = [["mode_easy", "Easy"], ["mode_normal", "Normal"], ["mode_hard", "Hard"], ["mode_custom", "Custom"], ["exit", "Return to main menu"]]
    
    keepGoing, target_button = menuBase.main(title, options)
    
    game_mode = Mode.restore_mode()
    
    if target_button == 'mode_easy':
        game_mode = Mode(Mode.MODE_EASY)
    elif target_button == 'mode_normal':
        game_mode = Mode(Mode.MODE_NORMAL)
    elif target_button == 'mode_hard':
        game_mode = Mode(Mode.MODE_HARD)
    elif target_button == 'mode_custom':
        
        height, width, bombs = inputBase.main(["Height", "Width", "Number of Bombs"])
        
        
        # TODO add more robust conversions
        if height == "":
            
            height = 20
            bombs = None
            
        if width == "":
            
            width = 20
            bombs = None
            
        # craps up the gamebar widget and others if the width is tiny
        # TODO find a way to notify the player that the width can't be smaller than 10, maybe restrict height too
        elif int(width) < 10:
            
            width = 10
        
        if bombs is None:
            game_mode = Mode(None, int(height), int(width))
        else:
            game_mode = Mode(None, int(height), int(width), int(bombs))

    return False, game_mode
    
def mainMenu():
    
    title = "Minesweeper"
    buttonList = [["singlePlayer", "Single Player"],["multiPlayer", "Multiplayer"], ["settings", "Settings"]]
    return menuBase.main(title, buttonList)
