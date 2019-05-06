# import and initialize
import pygame
import MineField
from random import randint
import time

pygame.init()
screen = pygame.display.set_mode((640, 480))

cellImageDir = "images/cells"
widgetImageDir = "images/widgets"


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
        self.image.fill((90,90,90))
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
        self.image.fill((150,150,150))
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
            self.digit2.changeDigit(strBomb[0])
            self.digit3.changeDigit(strBomb[1])

        else:
            self.digit3.changeDigit(strBomb[0])

class Timer(pygame.sprite.Sprite):
    """
    Keeps track of time with 3 digit sprites
    """

    def __init__(self, w: int, h: int, right: int, top: int, digit1: Digit, digit2: Digit, digit3: Digit) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((w, h))
        self.image.fill((150,150,150))
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
        
def showMines(boxGroup, field):
    
    for box in boxGroup:
        
        cell = field.get_cell_at(*box.coords)
        if (cell.is_mine() and not cell.is_flag()):
            
            box.setBomb()
            
        elif (not cell.is_mine() and cell.is_flag()):
            
            box.setIncorrectlyFlagged()

def get_open_cells(field: MineField, cell: 'Cell') -> list:
    """Get a list of open connected field cell coordinates.

    Args:
        field (MineField): the MineField to search for open and connected
            cells.
        row (int): the row coordinate for the target cell.
        col (int): the column coordinate for the target cell.

    Returns:
        (list): a list of all open and connected cells.
    """

    if cell.is_flag() or cell.is_mine() or not field.cell_is_safe(cell):
        return [cell]

    open_cells: list = list()
    cell.set_visited(True)
    open_cells.append(cell)

    for c in field.surrounding_cells(cell):
        open_cells.append(c)

        if c.is_flag() or c.is_visited() or not field.cell_is_safe(c):
            continue

        open_cells += get_open_cells(field, c)

    return open_cells


def cell_to_box(boxes: list, field: MineField, cell: 'Cell') -> Box:
    """Get the Box instance corresponding to a cell from a list of boxes.

    Args:
        boxes (list): the list of boxes to pull from.
        field (MineField): the mine field of the cell.
        cell (Cell): the cell to find the corresponding box to.

    Returns:
        (Box): the box corresponding to the passed cell.
    """
    return boxes[field.get_col() * cell.get_row() + cell.get_col()]


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
        # minefield
    field = MineField.MineField(numRow, numCol)

    # background
    background = pygame.Surface(screen.get_size())
    background.fill((0, 255, 0))
    screen.blit(background, (0, 0))

    # mouse
    mouse = Mouse()

    # game bar and widgets (bomb counter, timer, and new game button )
    gameBar = GameBar(screen, gameBarHeight)
    gameBar.rect.topleft = (0,0)

    bombDigit1 = Digit(30, 30, 10, 10, 9)
    bombDigit2 = Digit(30, 30, 40, 10, 9)
    bombDigit3 = Digit(30, 30, 70, 10, 9)

    bombCounter = BombCounter(40, 30, bombDigit1, bombDigit2, bombDigit3, field.get_mine_count())

    timerDigit1 = Digit(30, 30, screen.get_width() - 90, 10, 9)
    timerDigit2 = Digit(30, 30, screen.get_width() - 60, 10, 9)
    timerDigit3 = Digit(30, 30, screen.get_width() - 30, 10, 9)

    digitGroup = pygame.sprite.Group(bombDigit1, bombDigit2, bombDigit3, timerDigit1, timerDigit2, timerDigit3)

    timer = Timer(40, 30, screen.get_width() - 10, 10, timerDigit1, timerDigit2, timerDigit3)
    playButton = PlayButton(30, 30)

    bombCounter.rect.topleft = (10, 10)
    #timer.rect.topright = ()
    playButton.rect.centerx = screen.get_width() / 2
    playButton.rect.top = 10

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

    return screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes, digitGroup


def main():
    numCol = numRow = 20
    fps = 30

    screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes, digitGroup = setupGame(numCol, numRow)

    mouseGroup = pygame.sprite.Group(mouse)
    gameBarGroup = pygame.sprite.Group(gameBar)
    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton])
    boxGroup = pygame.sprite.Group(boxes)


    sprites = [mouseGroup, gameBarGroup, widgetGroup, boxGroup, digitGroup]

    # assign
    clock = pygame.time.Clock()
    keepGoing: bool = True
    first_click: bool = True
    quick_flag: bool = False
    mineHit: bool = False

    while keepGoing:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                replayClick = mouse.rect.colliderect(playButton.rect)
                boxClicked: Box = pygame.sprite.spritecollide(mouse, boxGroup,
                                                              False)
                # Handle extraneous clicks
                if not boxClicked and not replayClick:
                    continue

                if replayClick:

                    screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes, digitGroup = setupGame(numCol, numRow)

                    mouseGroup = pygame.sprite.Group(mouse)
                    gameBarGroup = pygame.sprite.Group(gameBar)
                    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton])
                    boxGroup = pygame.sprite.Group(boxes)

                    sprites = [mouseGroup, gameBarGroup, widgetGroup, boxGroup, digitGroup]

                    first_click = True
                    mineHit = False

                if not mineHit: 
                    
                    leftClick, middleClick, rightClick = pygame.mouse.get_pressed()
    
                    if middleClick:
                        quick_flag = not quick_flag
    
                    if quick_flag:
                        leftClick, rightClick = rightClick, leftClick
    
                    if leftClick and not replayClick:
    
                        cell: 'Cell' = field.get_cell_at(*boxClicked[0].coords)
    
                        if first_click and cell.is_mine():
                            field.move_mine(cell)
                            
                        if first_click:
    
                            first_click = False
                            timer.init()
                            bombCounter.init()
    
                        open_cells: list = get_open_cells(field, cell)
                        boxes_affected: list = [
                            cell_to_box(boxes, field, cell)for cell in open_cells
                        ]
                    else:
                        boxes_affected: list = boxClicked
    
                    for box in boxes_affected:
                        cell: 'Cell' = field.get_cell_at(*box.coords)
    
                        if leftClick and not cell.is_flag() and not \
                                cell.is_clicked():
                            cell.set_clicked(True)
                            if cell.is_mine():
                                box.setBomb()
                                mineHit = True
                                playButton.sad()
                                timer.stop()
                                showMines(boxGroup, field)
                            else:
                                box.setNum(repr(cell))
                                playButton.surprised()
    
                        if rightClick:
                            if cell.is_clicked() and not cell.is_flag():
                                continue
                            cell.set_flag(not cell.is_flag())
                            field.add_flagged()
                            cell.set_clicked(not cell.is_clicked())
    
                            if cell.is_flag():
                                box.setFlagged()
                                bombCounter.dec()
                            else:
                                box.setDefault()
                                field.subtract_flagged()
                                bombCounter.inc()
            elif event.type == pygame.MOUSEBUTTONUP:
                 
                if not mineHit:
                    playButton.happy()

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
