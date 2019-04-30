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
        self.image = pygame.image.load("images/defaultBox.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.coords: tuple = coords
        self.clicked: bool = False
        super().__init__()


def main():
    # display
    pygame.display.set_caption("Minesweeper")

    # entities
    background = pygame.Surface(screen.get_size())
    background.fill((0, 255, 0))
    screen.blit(background, (0, 0))

    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)

    boxes = []
    boxSize = 30
    x = 0
    y = 0
    numCol = 10
    numRow = 10

    field = MineField.MineField(numRow, numCol)
    print(repr(field))

    for r in range(numRow):
        x = 0
        for c in range(numCol):
            box = Box(boxSize, (r, c))
            box.rect.left = x
            box.rect.top = y
            boxes.append(box)
            x += boxSize

        y += boxSize

    boxGroup = pygame.sprite.Group(boxes)

    sprites = [boxGroup, mouseGroup]

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

        # move the fish; check boundaries

        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        # refresh
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
