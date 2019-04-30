# import and initialize
import pygame
import MineField
import Cell

pygame.init()

screen = pygame.display.set_mode((640, 480))


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

    def __init__(self, size, coords: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/defaultBox.png"), (size, size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.coords: tuple = coords
        self.clicked: bool = False
        super().__init__()
        
class GameBar(pygame.sprite.Sprite):
    
    def __init__(self, screen, gameBarHeight: int) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((screen.get_width(), gameBarHeight))
        self.image.fill((90,90,90))
        self.rect = self.image.get_rect()

class BombCounter(pygame.sprite.Sprite):
    
    def __init__(self, w, h) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((w, h))
        self.image.fill((150,150,150))
        self.rect = self.image.get_rect()

class Timer(pygame.sprite.Sprite):
    
    def __init__(self, w, h) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((w, h))
        self.image.fill((150,150,150))
        self.rect = self.image.get_rect()


class PlayButton(pygame.sprite.Sprite):
    
    def __init__(self, w, h) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load("images/smiley.png"), (w, h)).convert_alpha()
        self.rect = self.image.get_rect()
        
        
def setupGame(numCol: int = 10, numRow: int = 10):
    
    # display
    pygame.display.set_caption("Minesweeper")
    
    gameBarHeight = 50
    boxSize = 30
    
    # for generating a grid of boxes
    x = 0
    y = gameBarHeight
    
    screenWidth = numCol * boxSize
    screenHeight = (numRow * boxSize) + gameBarHeight

    screen = pygame.display.set_mode((screenWidth, screenHeight))

    # -----entities------
    
    # background
    background = pygame.Surface(screen.get_size())
    background.fill((0, 255, 0))
    screen.blit(background, (0, 0))

    # mouse
    mouse = Mouse()

    # game bar and widgets (bomb counter, timer, and new game button )
    gameBar = GameBar(screen, gameBarHeight)
    gameBar.rect.topleft = (0,0)
    
    bombCounter = BombCounter(40, 30)
    timer = Timer(40, 30)
    playButton = PlayButton(30, 30)
    
    bombCounter.rect.topleft = (10, 10)
    timer.rect.topright = (screen.get_width() - 10, 10)
    playButton.rect.centerx = screen.get_width() / 2
    playButton.rect.top = 10

    # minefield
    field = MineField.MineField(numRow, numCol)
    print(repr(field))

    boxes = []
    for r in range(numRow):
        x = 0
        for c in range(numCol):
            box = Box(boxSize, (r, c))
            box.rect.left = x
            box.rect.top = y
            boxes.append(box)
            x += boxSize

        y += boxSize
    
    return screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes

def main():
    
    numCol = numRow = 30

    screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes = setupGame(numCol, numRow)
    
    mouseGroup = pygame.sprite.Group(mouse)
    gameBarGroup = pygame.sprite.Group(gameBar)
    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton])
    boxGroup = pygame.sprite.Group(boxes)
    
    sprites = [mouseGroup, gameBarGroup, widgetGroup, boxGroup]
    
    # assign
    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                leftClick, middleClick, rightClick = pygame.mouse.get_pressed()
                boxClicked = pygame.sprite.spritecollide(mouse, boxGroup,
                                                         False)
                for box in boxClicked:
                    cell: Cell = field.get_cell_at(*box.coords)

                    if leftClick and not box.clicked:
                        box.clicked = True
                        if cell.is_mine():
                            box.image = pygame.image.load(
                                "images/bomb.png").convert_alpha()
                        else:
                            box.image = pygame.image.load(
                                f"images/{repr(cell)}.png").convert_alpha()
                            
                    if rightClick:
                        if box.clicked and not cell.is_flag():
                            continue
                        cell.set_flag(not cell.is_flag())
                        box.clicked = not box.clicked
                        if cell.flag:
                            box.image = pygame.image.load(
                                "images/flagged.png").convert_alpha()
                        else:
                            box.image = pygame.image.load(
                                "images/defaultBox.png").convert_alpha()

                # play again
                if mouse.rect.colliderect(playButton.rect):
                    
                    screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes = setupGame(numCol, numRow)
                    
                    mouseGroup = pygame.sprite.Group(mouse)
                    gameBarGroup = pygame.sprite.Group(gameBar)
                    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton])
                    boxGroup = pygame.sprite.Group(boxes)
    
                    sprites = [mouseGroup, gameBarGroup, widgetGroup, boxGroup]
                    
        # update groups

        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        # refresh
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
