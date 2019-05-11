# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:47:01 2019

@author: bauzy
"""

import pygame
from mode import Mode
import menuBase

pygame.init()

def settingsMenu() -> tuple:
    
    title = "Settings"
    options = [["mode_easy", "Easy"], ["mode_normal", "Normal"], ["mode_hard", "Hard"], ["exit", "Return to main menu"]]
    
    keepGoing, target_button = menuBase.main(title, options)
    
    game_mode = Mode.restore_mode()
    
    if target_button == 'mode_easy':
        game_mode = Mode(Mode.MODE_EASY)
    elif target_button == 'mode_normal':
        game_mode = Mode(Mode.MODE_NORMAL)
    elif target_button == 'mode_hard':
        game_mode = Mode(Mode.MODE_HARD)

    return False, game_mode
    
def mainMenu():
    
    title = "Minesweeper"
    buttonList = [["singlePlayer", "Single Player"],["multiPlayer", "Multiplayer"],["settings", "Settings"]]
    return menuBase.main(title, buttonList)
