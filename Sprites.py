# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:58:58 2019

@author: bauzy
"""

import pygame
pygame.init()
import time
import random
from ColorTheme import ColorTheme

# image directories
cellImageDir = ""
widgetImageDir = ""

# methods for setting the image asset directories for all sprites
def setCellImageDir(imgDir):
    
    global cellImageDir
    cellImageDir = imgDir

def setWidgetImageDir(imgDir):
    
    global widgetImageDir
    widgetImageDir = imgDir  


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        super().__init__()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        
class Box(pygame.sprite.Sprite):

    def __init__(self, size: int, coords: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.size = size

        self.defaultImg = f"{cellImageDir}/defaultBox.png"
        self.bombImg = f"{cellImageDir}/bomb.png"
        self.flagImg = f"{cellImageDir}/flagged.png"
        self.incorrectlyFlaggedImg = f"{cellImageDir}/incorrectlyFlagged.png"

        self.image = pygame.transform.scale(pygame.image.load(self.defaultImg), (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.coords: tuple = coords
        super().__init__()

    def setDefault(self):

        self.image = pygame.transform.scale(pygame.image.load(self.defaultImg), (self.size, self.size)).convert_alpha()

    def setBomb(self):

        self.image = pygame.transform.scale(pygame.image.load(self.bombImg), (self.size, self.size)).convert_alpha()

    def setFlagged(self):

        self.image = pygame.transform.scale(pygame.image.load(self.flagImg), (self.size, self.size)).convert_alpha()

    def setNum(self, num: int):

        self.image = pygame.transform.scale(pygame.image.load(f"{cellImageDir}/{num}.png"), (self.size, self.size)).convert_alpha()
        
    def setIncorrectlyFlagged(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.incorrectlyFlaggedImg), (self.size, self.size)).convert_alpha()

class GameBar(pygame.sprite.Sprite):

    def __init__(self, screen, gameBarHeight: int) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((screen.get_width(), gameBarHeight))
        self.image.fill(ColorTheme.GAMEBAR)
        self.rect = self.image.get_rect()

class Digit(pygame.sprite.Sprite):
    """
    Sprite class used for the Timer and BombCounter widget sprites
    """

    def __init__(self, w: int, h: int, left: int, top : int, value : int):

        pygame.sprite.Sprite.__init__(self)

        self.width = w
        self.height = h

        self.image = self.image = pygame.transform.scale(pygame.image.load(f"{widgetImageDir}/{value}.png"), (self.width, self.height)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        self.value = value

    def changeDigit(self, value: int):

        self.value = value
        self.image = pygame.transform.scale(pygame.image.load(f"{widgetImageDir}/{self.value}.png"), (self.width, self.height)).convert_alpha()

class BombCounter(pygame.sprite.Sprite):
    """
    Keeps track of the amount of bombs
    """

    def __init__(self, w, h, digit1: Digit, digit2: Digit, digit3: Digit, bombNum) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((w, h))
        self.image.fill(ColorTheme.BOMB_COUNTER)
        self.rect = self.image.get_rect()

        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3

        self.initialized = False
        self.bombNum = bombNum

    def init(self):

        self.initialized = True

        self.digit1.changeDigit(0)
        self.digit2.changeDigit(0)
        self.digit3.changeDigit(0)

        self.changeDigits()

    def inc(self):

        self.bombNum += 1
        self.changeDigits()

    def dec(self):

        self.bombNum -= 1
        self.changeDigits()


    def changeDigits(self):

        strBomb = str(self.bombNum)

        if self.bombNum >= 100:
            self.digit1.changeDigit(strBomb[0])
            self.digit2.changeDigit(strBomb[1])
            self.digit3.changeDigit(strBomb[2])

        elif self.bombNum >= 10:
            self.digit1.changeDigit(0)
            self.digit2.changeDigit(strBomb[0])
            self.digit3.changeDigit(strBomb[1])

        else:
            self.digit1.changeDigit(0)
            self.digit2.changeDigit(0)
            self.digit3.changeDigit(strBomb[0])

class Timer(pygame.sprite.Sprite):
    """
    Keeps track of time with 3 digit sprites
    """

    def __init__(self, w: int, h: int, right: int, top: int, digit1: Digit, digit2: Digit, digit3: Digit) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((w, h))
        self.image.fill(ColorTheme.TIMER)
        self.rect = self.image.get_rect()

        self.initialized = False

        self.rect.topright = (right, top)

        self.startTime = 0

        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3

    def init(self):
        """
        Start timer when the user clicks on a bomb
        """

        self.initialized = True
        self.startTime = time.time()

        self.digit1.changeDigit(0)
        self.digit2.changeDigit(0)
        self.digit3.changeDigit(0)

    def update(self):

        if self.initialized:
            elapsedTime = round(time.time() - self.startTime)

            stringTime = str(elapsedTime)
            
            if elapsedTime >= 1000:
                
                self.digit1.changeDigit(9)
                self.digit2.changeDigit(9)
                self.digit3.changeDigit(9)
                
                self.initialized = False
                
            if elapsedTime >= 100:
                self.digit1.changeDigit(stringTime[0])
                self.digit2.changeDigit(stringTime[1])
                self.digit3.changeDigit(stringTime[2])

            elif elapsedTime >= 10:
                self.digit2.changeDigit(stringTime[0])
                self.digit3.changeDigit(stringTime[1])

            else:
                self.digit3.changeDigit(stringTime[0])
                
    def stop(self):
        
        self.initialized = False

class PlayButton(pygame.sprite.Sprite):

    def __init__(self, w, h) -> None:

        pygame.sprite.Sprite.__init__(self)
        
        self.width = w
        self.height = h
        
        self.happyImg = widgetImageDir + "/smiley.png"
        self.sadImg = widgetImageDir + "/frowny.png"
        self.surprisedImg = widgetImageDir + "/surprised.png"
        
        self.image = pygame.transform.scale(pygame.image.load(self.happyImg), (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()
        
    def happy(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.happyImg), (self.width, self.height)).convert_alpha()
        
    def sad(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.sadImg), (self.width, self.height)).convert_alpha()
        
    def surprised(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.surprisedImg), (self.width, self.height)).convert_alpha()
        
class ModeIndicator(pygame.sprite.Sprite):
    
    def __init__(self, w, h) -> None:

        pygame.sprite.Sprite.__init__(self)
        
        self.width = w
        self.height = h
        
        self.imgDir = f"{widgetImageDir}/FlaggingModeWidget/"
        
        self.normalModeImg = f"{self.imgDir}NormalMode.png"
        self.quickFlaggingModeImg = f"{self.imgDir}FlaggingMode.png"
        
        self.image = pygame.transform.scale(pygame.image.load(self.normalModeImg), (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()
        
    def setQuickFlagMode(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.quickFlaggingModeImg), (self.width, self.height)).convert_alpha()
    
    def setNormalMode(self):
        
        self.image = pygame.transform.scale(pygame.image.load(self.normalModeImg), (self.width, self.height)).convert_alpha()
            
class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, name, color):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((300, 70))
        self.image.fill(ColorTheme.BUTTON)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    def hover(self):
        
        self.image.fill(ColorTheme.BUTTON_HOVER)
        
    def unhover(self):
        
        self.image.fill(ColorTheme.BUTTON)

class Label(pygame.sprite.Sprite):
    """
    Object to display text
    Does not update
    """

    def __init__(self, name, text, loc, alignment, bgColor = None, size = 30, color=ColorTheme.MENU_TEXT_ITEM):
        """
        name for matching with the button object name and keeping the same background color
        string text
        tuple location
        int alignment (-1 = left, 0 = center, 1 = right)
        3 tuple for color default is white
        """

        pygame.sprite.Sprite.__init__(self)
        
        self.name = name
        self.text = text
        self.loc = loc
        self.alignment = alignment
        self.bgColor = bgColor
        self.size = size
        self.color = color

        self.font = pygame.font.SysFont("None", size)
        self.image = self.font.render(self.text, 1, self.color, self.bgColor)
            
        self.rect = self.image.get_rect()

        self.align()
            
    def align(self):
        
        # left aligned
        if self.alignment == -1:

            self.rect.left = self.loc[0]
            self.rect.centery = self.loc[1]

        # center aligned
        elif self.alignment == 0:

            self.rect.center = self.loc

        # right aligned
        else:

            self.rect.right = self.loc[0]
            self.rect.centery = self.loc[1]
        
            
    def render(self):
        
        self.image = self.font.render(self.text, 1, self.color, self.bgColor)
        self.rect = self.image.get_rect()
        self.align()
        
    def hover(self):
        
        self.bgColor = ColorTheme.BUTTON_HOVER
        self.render()
        
    def unhover(self):
        
        self.bgColor = ColorTheme.BUTTON
        self.render()
        
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.imgSrc = f"{cellImageDir}/bomb.png"
        self.image = pygame.image.load(self.imgSrc).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.left = random.randint(0, 100)
        self.rect.top = random.randint(0, 100)
        
        self.x = random.randint(-5, 5)
        self.y = random.randint(-5, 5)
        
        self.degrees = 0
        self.rotationSpeed = random.randint(0, 10)
    
    def update(self):
        
        self.rotate()
        
        if self.rect.right < 0:
            self.rect.left = self.screen.get_width()
        elif self.rect.left > self.screen.get_width():
            self.rect.right = 0  
        else:
            self.rect.centerx += self.x
            
        if self.rect.bottom < 0:
            self.rect.top = self.screen.get_height()
        elif self.rect.top > self.screen.get_height(): 
            self.rect.bottom = 0
        else:
            self.rect.centery += self.y
            
    def rotate(self):
        """
        Animates image
        """
        
        if (self.degrees + self.rotationSpeed > 360):
            
            self.degrees = 0
            
        else:
            
            self.degrees += self.rotationSpeed
        
        self.image = pygame.transform.rotate(
                                pygame.image.load(self.imgSrc).convert_alpha(), self.degrees)