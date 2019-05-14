"""Creates the main entry point and center for all game functionality."""
from minefield.MineField import MineField
from minefield.MineField import Cell
from multiplayer import Client
import pygame
import time
from mode import Mode
from Sprites import *

pygame.init()
screen = pygame.display.set_mode((640, 480))

cellImageDir = "images/cells"
widgetImageDir = "images/widgets"

setCellImageDir(cellImageDir)
setWidgetImageDir(widgetImageDir)


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


def setupGame(field: MineField) -> tuple:
    # display
    pygame.display.set_caption("Minesweeper")

    gameBarHeight = 50
    boxSize = 30

    # for generating a grid of boxes
    x = 0
    y = gameBarHeight

    screenWidth = field.get_col() * boxSize
    screenHeight = (field.get_row() * boxSize) + gameBarHeight

    screen = pygame.display.set_mode((screenWidth, screenHeight))

    # background
    background = pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MINESWEEPER_BG)
    screen.blit(background, (0, 0))

    # mouse
    mouse = Mouse()

    # game bar and widgets (bomb counter, timer, and new game button )
    gameBar = GameBar(screen, gameBarHeight)
    gameBar.rect.topleft = (0,0)
    bombDigit1 = Digit(30, 30, 10, 10, 9)
    bombDigit2 = Digit(30, 30, 40, 10, 9)
    bombDigit3 = Digit(30, 30, 70, 10, 9)

    timerDigit1 = Digit(30, 30, screen.get_width() - 90, 10, 9)
    timerDigit2 = Digit(30, 30, screen.get_width() - 60, 10, 9)
    timerDigit3 = Digit(30, 30, screen.get_width() - 30, 10, 9)

    bombCounter = BombCounter(40, 30, bombDigit1, bombDigit2, bombDigit3, field.get_mine_count())
    timer = Timer(40, 30, screen.get_width() - 10, 10, timerDigit1, timerDigit2, timerDigit3)
    playButton = PlayButton(30, 30)
    modeIndicator = ModeIndicator(30, 30)

    digitGroup = pygame.sprite.Group(bombDigit1, bombDigit2, bombDigit3, timerDigit1, timerDigit2, timerDigit3)

    bombCounter.rect.topleft = (10, 10)
    playButton.rect.centerx = (screen.get_width() / 2) - 20
    playButton.rect.top = 10
    modeIndicator.rect.centerx = (screen.get_width() / 2) + 20
    modeIndicator.rect.top = 10

    boxes = []
    for r in range(field.get_row()):
        x = 0
        for c in range(field.get_col()):
            box = Box(boxSize, (r, c))
            box.rect.left = x
            box.rect.top = y
            boxes.append(box)
            x += boxSize

        y += boxSize

    return screen, background, mouse, gameBar, bombCounter, timer, playButton, modeIndicator, boxes, digitGroup


def main(game_mode: Mode = Mode(), client: Client = None):
    if client is None:
        field: MineField = MineField(game_mode.get_height(),
                                     game_mode.get_width())
    else:
        field: MineField = client.get_mine_field()

    fps = 30

    screen, background, mouse, gameBar, bombCounter, timer, playButton, modeIndicator, boxes, digitGroup = setupGame(field)

    mouseGroup = pygame.sprite.Group(mouse)
    gameBarGroup = pygame.sprite.Group(gameBar)
    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton, modeIndicator])
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
                modeClick = mouse.rect.colliderect(modeIndicator.rect)

                # Handle extraneous clicks
                if not boxClicked and not replayClick and not modeClick:
                    continue

                if modeClick:

                    quick_flag = not quick_flag

                    if quick_flag:
                        modeIndicator.setQuickFlagMode()

                    else:
                        modeIndicator.setNormalMode()
                        modeIndicator.setNormalMode()

                    continue

                if replayClick:
                    field = MineField(game_mode.get_height(), game_mode.get_width())
                    screen, background, mouse, gameBar, bombCounter, timer, playButton, modeIndicator, boxes, digitGroup = setupGame(field)

                    mouseGroup = pygame.sprite.Group(mouse)
                    gameBarGroup = pygame.sprite.Group(gameBar)
                    widgetGroup = pygame.sprite.Group([bombCounter, timer, playButton, modeIndicator])
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
                        modeIndicator.setQuickFlagMode()

                    else:
                        modeIndicator.setNormalMode()

                    if leftClick and not replayClick:

                        cell: 'Cell' = field.get_cell_at(*boxClicked[0].coords)

                        if first_click and cell.is_mine():
                            new_loc: tuple = field.move_mine(cell)
                            old_loc: tuple = (cell.get_row(), cell.get_col())
                            client.move_mine(old_loc, new_loc)

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

                            if client is not None:
                                client.send_change(cell.get_row(),
                                                  cell.get_col(),
                                                  'HIT')
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
                            client.send_change(cell.get_row(),
                                               cell.get_col(),
                                               'FLAG')

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
