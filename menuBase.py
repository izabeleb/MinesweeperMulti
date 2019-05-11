
#import and initialize
import pygame
from Sprites import Mouse, Button, Label, Bomb
from ColorTheme import ColorTheme
pygame.init()

def main(title: str, nameLabelList: str):
    """
    title: what the title at the top of the menu screen should be
    nameLabelList: 
        a 2d list of information about each button
        includes the name of the button for identification purposes and
        the physical display name on how the button name will appear on screen
        like so:
    
        [
            [name, nameAsItAppearsOnScreen],
            [..., ...]
        ]
    """
    
    pygame.font.init()
    buttonColor = ColorTheme.BUTTON
    
    height = 200 + (len(nameLabelList) * 100)
    screen = pygame.display.set_mode((640, height))
    #display

    #entities
    background=pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MENU_BG)
    screen.blit(background, (0,0))
    
    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)
    
    buttonGroup = pygame.sprite.Group()
    labelGroup = pygame.sprite.Group(Label(title, title, (screen.get_width() / 2, 100), 0, None, 60))
    
    vPos = 200
    inc = 80
    
    for label in nameLabelList:
        
        buttonGroup.add(Button(screen.get_width() / 2, vPos, label[0], buttonColor))
        labelGroup.add(Label(label[0], label[1], (screen.get_width() / 2, vPos), 0, buttonColor))
        vPos += inc
        
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
    
    buttonLastHovered = ""

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
                    
        buttonHovered = pygame.sprite.spritecollide(mouse, buttonGroup, False)
         
        if buttonHovered == []:
            
            for buttonItem in buttonGroup.sprites():
                        
                if buttonItem.name == buttonLastHovered:
                    
                    buttonItem.unhover()
                    
            for labelItem in labelGroup.sprites():
                        
                if labelItem.name == buttonLastHovered:
                    
                    labelItem.unhover()
        
        else:
            
            for button in pygame.sprite.spritecollide(mouse, buttonGroup, False):
                        
                # a new button is being hovered on
                if button.name != buttonLastHovered: 
                                    
                    for buttonItem in buttonGroup.sprites():
                        
                        if buttonItem.name == buttonLastHovered:
                            
                            buttonItem.unhover()
                            
                    for labelItem in labelGroup.sprites():
                        
                        if labelItem.name == buttonLastHovered:
                    
                            labelItem.unhover()
                            
                button.hover()
                
                buttonLastHovered = button.name
                
                for labelItem in labelGroup.sprites():
                        
                    if labelItem.name == buttonLastHovered:
                    
                        labelItem.hover()

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