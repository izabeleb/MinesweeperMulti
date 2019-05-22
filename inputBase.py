# -*- coding: utf-8 -*-
"""
Created on Tue May 21 23:18:46 2019

@author: bauzy
"""


#import and initialize
import pygame
from Sprites import Mouse, Label, InputBox, Button
from ColorTheme import ColorTheme
pygame.init()

def main(inputList: list):
    """
    Accepts a list of inputs needed as display strings
    returns inputs as an unpacked list
    """

    pygame.font.init()
    
    #display
    screen = pygame.display.set_mode((640, 550))

    #entities    
    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)
    
    lblGroup = pygame.sprite.Group()
    txtGroup = pygame.sprite.Group()
    inputGroup = pygame.sprite.Group()
    
    lblHeight = 100
    inputHeight = 170
    
    heightInc = 150
    buttonGap = 50
    
    for inputItem in inputList:
        
        lblGroup.add(Label(f"lbl{inputItem}", f"{inputItem}", (screen.get_width() / 2, lblHeight), 0))
        txtGroup.add(InputBox(f"txt{inputItem}", (450, 70), (screen.get_width() / 2, inputHeight)))
        inputGroup.add(Label(f"txt{inputItem}", "", (screen.get_width() / 2, inputHeight), 0, None, 20, (0, 0, 0)))
        
        lblHeight += heightInc
        inputHeight += heightInc
    
    lblSave = Label("save", "Save", (screen.get_width() / 2, lblHeight + buttonGap), 0)
    btnSave = Button(screen.get_width() / 2, lblHeight + buttonGap, "save")
    
    btnGroup = pygame.sprite.Group(btnSave, lblSave)
    
    sprites = [mouseGroup, lblGroup, txtGroup, inputGroup, btnGroup]

    # fix screen size
    screenHeight = lblHeight + btnSave.height + buttonGap
    screen = pygame.display.set_mode((640, screenHeight))
    
    background=pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MENU_BG)
    screen.blit(background, (0,0))

    #assign
    clock = pygame.time.Clock()
    keepGoing = True
    textString = ""
    activeTextBox = ""
    
    #loop
    while keepGoing:  
        
        # This block allows backspace key to delete multiple characters
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_BACKSPACE]:
                    
            textString = textString[:-1]
            
            for inputLabel in inputGroup.sprites():
                                
                if inputLabel.name == activeTextBox:
                                    
                    inputLabel.renderText(textString)

        #time
        clock.tick(15)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                for btnClicked in pygame.sprite.spritecollide(mouse, btnGroup, False):
                    
                    # save button is clicked
                    keepGoing = False
                
                # textbox is clicked
                for inputClicked in pygame.sprite.spritecollide(mouse, txtGroup, False):
                
                    if inputClicked.name != activeTextBox:
                        
                        textString = ""
                        
                        # unfocus old textbox
                        for inputBox in txtGroup.sprites():
                            
                            if inputBox.name == activeTextBox:
                                
                                inputBox.unfocus()
                                
                        for inputBox in inputGroup.sprites():
                            
                            if inputBox.name == activeTextBox:
                                
                                inputBox.unfocus()
                                
                            
                        # focus new textbox
                        activeTextBox = inputClicked.name
                        
                        for inputBox in txtGroup.sprites():
                            
                            if inputBox.name == activeTextBox:
                                
                                inputBox.focus() 
                                
                        for inputBox in inputGroup.sprites():
                            
                            if inputBox.name == activeTextBox:
                                
                                inputBox.focus()
            
            elif event.type == pygame.KEYDOWN:
                
                # add other characters needed for hostnames and ports in a better way
                if (event.key in range(pygame.K_a, pygame.K_z + 1) or 
                    event.key in range(pygame.K_0, pygame.K_9 + 1) or
                    event.key == pygame.K_PERIOD or 
                    event.key == pygame.K_MINUS):
                    
                    textString += event.unicode
                    
                    for inputLabel in inputGroup.sprites():
                                
                        if inputLabel.name == activeTextBox:
                                    
                            inputLabel.renderText(textString)                    
                    
        btnHovered = pygame.sprite.spritecollide(mouse, btnGroup, False)
        
        if btnHovered == []:
            
            for item in btnGroup.sprites():
                
                item.unhover()
                
        else:
            
            for item in btnGroup.sprites():
                
                item.hover()

        #move the items

        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        #refresh
        pygame.display.flip()
        
    typedText = []
    
    for inputItem in inputGroup:
        
        typedText.append(inputItem.text)
        
    return (*typedText,)

if __name__ == "__main__":
    main()