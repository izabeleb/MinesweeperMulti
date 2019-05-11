import pygame

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

    def __init__(self, text, loc, alignment, color=(255, 255, 255)):
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


class Mode:
    MODE_EASY: tuple = (10, 10)
    MODE_NORMAL: tuple = (20, 20)
    MODE_HARD: tuple = (30, 30)

    def __init__(self, mode: tuple = None) -> None:
        if mode is None:
            mode = Mode.MODE_NORMAL

        self.mode = mode

    def mode_to_dict(self):
        return {'HEIGHT': self.mode[0], 'WIDTH': self.mode[1]}

    @staticmethod
    def restore_mode(path='setings.json') -> 'Mode':
        import os

        if not os.path.isfile(path):
            return Mode()

        mode_json: str = ''
        with open(path, 'w') as file_mode:
            mode_json += file_mode.read()

        mode_json: dict = mode_json.loads()

        return Mode((mode_json['HEIGHT'], mode_json['WIDTH']))

    def store_mode(self) -> None:
        import json

        with open('settings.json', 'w') as store:
            store.write(json.dumps(self.mode_to_dict()))


def main() -> tuple:
    pygame.font.init()

    screen = pygame.display.set_mode((640, 480))
    # display

    pygame.display.set_caption("Minesweeper")

    # entities
    background = pygame.Surface(screen.get_size())
    background.fill((0, 255, 0))
    screen.blit(background, (0, 0))

    mouse = Mouse()
    mouseGroup = pygame.sprite.Group(mouse)

    mode_easy = Button(screen.get_width() / 2, 100, 'mode_easy')
    mode_normal = Button(screen.get_width() / 2, 200, 'mode_normal')
    mode_hard = Button(screen.get_width() / 2, 300, 'mode_hard')
    exit_button = Button(screen.get_width() / 2, 400, 'exit')
    button_group = pygame.sprite.Group(mode_easy, mode_normal, mode_hard,
                                       exit_button)

    easy_label = Label("Easy", (screen.get_width() / 2, 100), 0)
    normal_label = Label("Normal", (screen.get_width() / 2, 200), 0)
    hard_label = Label("Hard", (screen.get_width() / 2, 300), 0)
    exit_label = Label("Return to main menu", (screen.get_width() / 2, 400), 0)
    mode_label_group = pygame.sprite.Group(easy_label, normal_label,
                                           hard_label, exit_label)

    sprites: list = [mouseGroup, button_group, mode_label_group]

    clock = pygame.time.Clock()
    keep_going: bool = True
    target_button: str = ''
    game_mode: Mode = Mode()

    while keep_going:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for mode in pygame.sprite.spritecollide(mouse, button_group,
                                                        False):
                    target_button = mode.name
                    print(target_button)
                    if target_button == 'exit':
                        keep_going = False
                    elif target_button == 'mode_easy':
                        game_mode = Mode(Mode.MODE_EASY)
                    elif target_button == 'mode_normal':
                        game_mode = Mode(Mode.MODE_NORMAL)
                    elif target_button == 'mode_hard':
                        game_mode = Mode(Mode.MODE_HARD)

        for group in sprites:
            group.clear(screen, background)
            group.update()
            group.draw(screen)

        pygame.display.flip()

    return False, game_mode


if __name__ == '__main__':
    main()