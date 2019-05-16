
#import and initialize
import pygame
from Sprites import Mouse, Label, InputBox, Button
from ColorTheme import ColorTheme
pygame.init()

def main():

    pygame.font.init()
    
    screen = pygame.display.set_mode((640, 550))
    #display

    #entities
    background=pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MENU_BG)
    screen.blit(background, (0,0))
    
    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)
    
    lblHostname = Label("lblHostname", "Hostname", (screen.get_width() / 2, 100), 0)
    lblPort = Label("lblPort", "Port", (screen.get_width() / 2, 250), 0)
    lblGroup = pygame.sprite.Group(lblHostname, lblPort)
    
    txtHostname = InputBox("txtHostname", (450, 70), (screen.get_width() / 2, 170))
    txtPort = InputBox("txtPort", (450, 70), (screen.get_width() / 2, 320))
    txtGroup = pygame.sprite.Group(txtHostname, txtPort)
    
    inputHostname = Label("txtHostname", "", (screen.get_width() / 2, 170), 0, None, 20, (0, 0, 0))
    inputPort = Label("txtPort", "", (screen.get_width() / 2, 320), 0, None, 20, (0, 0, 0))
    inputGroup = pygame.sprite.Group(inputHostname, inputPort)
    
    lblSave = Label("save", "Save", (screen.get_width() / 2, 450), 0)
    btnSave = Button(screen.get_width() / 2, 450, "save")
    
    btnGroup = pygame.sprite.Group(btnSave, lblSave)
    
    sprites = [mouseGroup, lblGroup, txtGroup, inputGroup, btnGroup]

    #assign
    clock = pygame.time.Clock()
    keepGoing = True
    textString = ""
    activeTextBox = ""
    
    # can enter some defaults here
    hostname = ""
    port = ""
    
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
        clock.tick(30)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                for btnClicked in pygame.sprite.spritecollide(mouse, btnGroup, False):
                    
                    # save button is clicked
                    keepGoing = False
                    hostname = inputHostname.text
                    port = inputPort.text
                
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
        
    return hostname, port

if __name__ == "__main__":
    main()