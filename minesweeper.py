# import and initialize
import pygame
import MineField

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

    def __init__(self, size: int, coords: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/defaultBox.png"), (size, size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.coords: tuple = coords
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
    open_cells: list = list()
    cell.set_visited(True)
    open_cells.append(cell)

    if cell.is_flag() or not field.cell_is_safe(cell):
        return [cell]

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
    numCol = numRow = 10

    screen, background, mouse, gameBar, bombCounter, timer, playButton, field, boxes = setupGame(numCol, numRow)
    
    mouseGroup = pygame.sprite.Group(mouse)
    gameBarGroup = pygame.sprite.Group(gameBar)
    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton])
    boxGroup = pygame.sprite.Group(boxes)
    
    sprites = [mouseGroup, gameBarGroup, widgetGroup, boxGroup]
    
    # assign
    clock = pygame.time.Clock()
    keepGoing = True

    bomb_image: str = "images/bomb.png"
    flag_image: str = "images/flagged.png"
    box_image: str = "images/defaultBox.png"

    while keepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                leftClick, middleClick, rightClick = pygame.mouse.get_pressed()
                boxClicked: Box = pygame.sprite.spritecollide(mouse, boxGroup,
                                                              False)
                # Something nt a box is clicked
                if not boxClicked:
                    continue

                if leftClick:
                    cell: 'Cell' = field.get_cell_at(*boxClicked[0].coords)
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
                            box.image = pygame.image.load(
                                bomb_image).convert_alpha()
                        else:
                            box.image = pygame.image.load(
                                f"images/{repr(cell)}.png").convert_alpha()

                    if rightClick:
                        if cell.is_clicked() and not cell.is_flag():
                            continue
                        cell.set_flag(not cell.is_flag())
                        cell.set_clicked(not cell.is_clicked())

                        if cell.is_flag():
                            box.image = pygame.image.load(
                                flag_image).convert_alpha()
                        else:
                            box.image = pygame.image.load(
                                box_image).convert_alpha()

                    # if leftClick and not cell.is_clicked():
                    #     cell.set_clicked(True)
                    #     if cell.is_mine():
                    #         box.image = pygame.image.load(
                    #             "images/bomb.png").convert_alpha()
                    #     else:
                    #         box.image = pygame.image.load(
                    #             f"images/{repr(cell)}.png").convert_alpha()
                    #
                    # if rightClick:
                    #     cell.set_flag(not cell.is_flag())
                    #     cell.set_clicked(not cell.is_clicked())
                    #
                    #     if cell.is_flag():
                    #         box.image = pygame.image.load(
                    #             "images/flagged.png").convert_alpha()
                    #     else:
                    #         box.image = pygame.image.load(
                    #             "images/defaultBox.png").convert_alpha()

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
