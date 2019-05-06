# -*- coding: utf-8 -*-
"""
Created on Sun May  5 20:42:43 2019

@author: bauzy
"""

"""
    basicSushi.py
    a program that moves a fish across the screen

"""

#import and initialize
import pygame, random
pygame.init()

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

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, name):

        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((300, 70))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
class Label(pygame.sprite.Sprite):
    """
    Object to display text
    """
    
    def __init__(self, text, loc, alignment, color = (255, 255, 255)):
        """
        string text
        tuple location
        int alignment (-1 = left, 0 = center, 1 = right)
        3 tuple for color default is white
        """

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("None", 30)
        self.text = text
        self.color = color
        self.loc = loc
        self.alignment = alignment
        
        
        
        # image
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

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
            
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.imgSrc = "images/cells/bomb.png"
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

def main():
    
    pygame.font.init()
    
    screen = pygame.display.set_mode((640, 480))
    #display

    pygame.display.set_caption("Minesweeper")

    #entities
    background=pygame.Surface(screen.get_size())
    background.fill((0,255,0))
    screen.blit(background, (0,0))
    
    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)

    singlePlayer = Button(screen.get_width() / 2, 100, "singlePlayer")
    multiPlayer = Button(screen.get_width() / 2, 200, "multiPlayer")
    settings = Button(screen.get_width() / 2, 300, "settings")
    buttonGroup = pygame.sprite.Group(singlePlayer, multiPlayer, settings)
    
    singlePlayerLabel = Label("Single Player", (screen.get_width() / 2, 100), 0)
    multiPlayerLabel = Label("MultiPlayer", (screen.get_width() / 2, 200), 0)
    settingsLabel = Label("Settings", (screen.get_width() / 2, 300), 0)
    
    labelGroup = pygame.sprite.Group(singlePlayerLabel, multiPlayerLabel, settingsLabel)
    
    bombs = []
    for i in range(20):
        bombs.append(Bomb(screen))
    bombGroup = pygame.sprite.Group(bombs)
    
    sprites = [mouseGroup, bombGroup, buttonGroup, labelGroup]

    #assign
    clock = pygame.time.Clock()
    keepGoing = True
    donePlaying = False
    buttonName = ""

    #loop
    while keepGoing:


        #time
        clock.tick(30)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                for button in pygame.sprite.spritecollide(mouse, buttonGroup, False):
                    
                    buttonName = button.name
                    keepGoing = False

        #move the items

        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        #refresh
        pygame.display.flip()

    return donePlaying, buttonName
    
if __name__ == "__main__":
    main()
