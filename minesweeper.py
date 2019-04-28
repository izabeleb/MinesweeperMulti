#import and initialize
import pygame, random
pygame.init()


screen = pygame.display.set_mode((640, 480))

class Mouse(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

    def update(self):

        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
            
        
class Box(pygame.sprite.Sprite):
    
    def __init__(self, size):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/defaultBox.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.isBomb = random.choice((True, False))

def main():
    #display

    pygame.display.set_caption("basic sushi")

    #entities
    background=pygame.Surface(screen.get_size())
    background.fill((0,255,0))
    screen.blit(background, (0,0))

    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)
    
    boxes = []
    boxSize = 30
    x = 0
    y = 0
    numCol = 10
    numRow = 10
    for r in range(numRow):
        
        x = 0
        
        for c in range(numCol):
        
            box = Box(boxSize)
            box.rect.left = x
            box.rect.top = y
            
            boxes.append(box)
            
            x += boxSize
        
        y += boxSize
        
        
    boxGroup = pygame.sprite.Group(boxes)
    
    sprites = [boxGroup, mouseGroup]

    #assign
    clock = pygame.time.Clock()
    keepGoing = True

    #loop
    while keepGoing:


        #time
        clock.tick(30)

        #events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                
                boxClicked = pygame.sprite.spritecollide(mouse, boxGroup, False)
                
                for box in boxClicked:
                    
                    if pressed1:
                    
                        print(box.isBomb)
                        
                        if box.isBomb:
                            print("Filling image")
                            box.image = pygame.image.load("images/bomb.png").convert_alpha()
                            
                        else:
                            
                            box.kill()
                            
                    if pressed3:
                        
                        box.image = pygame.image.load("images/flagged.png").convert_alpha()
                

        #move the fish; check boundaries
        
        for spriteGroup in sprites:
            
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        #refresh
        pygame.display.flip()

    pygame.quit()
    
if __name__ == "__main__":
    main()
