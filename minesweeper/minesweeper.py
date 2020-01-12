"""Creates the main entry point and center for all game functionality."""
from menu import Mode
from multiplayer import client
from theme.sprites import *
from .utils import *

screen = pygame.display.set_mode((640, 480))

gameBarHeight = 50
boxSize = 30


def setup_board(field: MineField) -> tuple:
    # display
    pygame.display.set_caption("Minesweeper")

    # for generating a grid of boxes
    x = 0
    y = gameBarHeight

    screen_width = field.max_col * boxSize
    screen_height = (field.max_row * boxSize) + gameBarHeight

    screen = pygame.display.set_mode((screen_width, screen_height))

    # background
    background = pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MINESWEEPER_BG)
    screen.blit(background, (0, 0))

    # mouse
    mouse = Mouse()

    # game bar and widgets (bomb counter, timer, and new game button )
    game_bar = GameBar(screen, gameBarHeight)
    game_bar.rect.topleft = (0, 0)
    bomb_digit1 = Digit(30, 30, 10, 10, 9)
    bomb_digit2 = Digit(30, 30, 40, 10, 9)
    bomb_digit3 = Digit(30, 30, 70, 10, 9)

    timer_digit1 = Digit(30, 30, screen.get_width() - 90, 10, 9)
    timer_digit2 = Digit(30, 30, screen.get_width() - 60, 10, 9)
    timer_digit3 = Digit(30, 30, screen.get_width() - 30, 10, 9)

    bomb_counter = BombCounter(40, 30, bomb_digit1, bomb_digit2, bomb_digit3, field.mine_count)
    timer = Timer(40, 30, screen.get_width() - 10, 10, timer_digit1, timer_digit2, timer_digit3)
    play_button = PlayButton(30, 30)
    mode_indicator = ModeIndicator(30, 30)

    digit_group = pygame.sprite.Group(bomb_digit1, bomb_digit2, bomb_digit3, timer_digit1,
                                      timer_digit2, timer_digit3)

    bomb_counter.rect.topleft = (10, 10)
    play_button.rect.centerx = (screen.get_width() / 2) - 20
    play_button.rect.top = 10
    mode_indicator.rect.centerx = (screen.get_width() / 2) + 20
    mode_indicator.rect.top = 10

    boxes = list()
    for r in range(field.max_row):
        x = 0
        for c in range(field.max_col):
            box = Box(boxSize, (r, c))
            box.rect.left = x
            box.rect.top = y
            boxes.append(box)
            x += boxSize

        y += boxSize

    return screen, background, mouse, game_bar, bomb_counter, timer, play_button, mode_indicator, \
           boxes, digit_group


def run_minesweeper(game_mode: Mode = Mode(), client: client = None):
    if client is None:
        field: MineField = MineField(game_mode.height(),
                                     game_mode.width(),
                                     None, game_mode.bomb_count())
    else:
        field: MineField = client.get_mine_field()

    fps = 30

    screen, background, mouse, game_bar, bomb_counter, timer, play_button, mode_indicator, boxes,\
        digit_group = setup_board(field)

    mouse_group = pygame.sprite.Group(mouse)
    game_bar_group = pygame.sprite.Group(game_bar)
    widget_group = pygame.sprite.Group([bomb_counter, timer, play_button, mode_indicator])
    box_group = pygame.sprite.Group(boxes)

    sprites = [mouse_group, game_bar_group, widget_group, box_group, digit_group]

    # assign
    clock = pygame.time.Clock()
    keep_going: bool = True
    first_click: bool = True
    quick_flag: bool = False
    mine_hit: bool = False

    while keep_going:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                replay_click = mouse.rect.colliderect(play_button.rect)
                box_clicked: List[pygame.sprite] = pygame.sprite.spritecollide(mouse,
                                                                               box_group,
                                                                               False)
                mode_click = mouse.rect.colliderect(mode_indicator.rect)

                # Handle extraneous clicks
                if not box_clicked and not replay_click and not mode_click:
                    continue

                if mode_click:

                    quick_flag = not quick_flag

                    if quick_flag:
                        mode_indicator.set_quick_flag_mode()

                    else:
                        mode_indicator.set_normal_mode()
                        mode_indicator.set_normal_mode()

                    continue

                if replay_click:
                    field = MineField(game_mode.height(), game_mode.width(), None,
                                      game_mode.bomb_count())
                    screen, background, mouse, game_bar, bomb_counter, timer, play_button,\
                        mode_indicator, boxes, digit_group = setup_board(field)

                    mouse_group = pygame.sprite.Group(mouse)
                    game_bar_group = pygame.sprite.Group(game_bar)
                    widget_group = pygame.sprite.Group(
                        [bomb_counter, timer, play_button, mode_indicator])
                    box_group = pygame.sprite.Group(boxes)

                    sprites = [mouse_group, game_bar_group, widget_group, box_group, digit_group]

                    first_click = True
                    mine_hit = False

                if not mine_hit:

                    left_click, middle_click, right_click = pygame.mouse.get_pressed()

                    if middle_click:
                        quick_flag = not quick_flag

                    if quick_flag:
                        left_click, right_click = right_click, left_click
                        mode_indicator.set_quick_flag_mode()

                    else:
                        mode_indicator.set_normal_mode()

                    if left_click and not replay_click:

                        cell: Cell = field.get_cell_at(*box_clicked[0].coords)

                        if first_click and cell.is_mine:
                            new_loc: tuple = field.move_mine(cell)
                            old_loc: tuple = (cell.row, cell.col)

                            if client is not None:
                                client.move_mine(old_loc, new_loc)

                        if first_click:
                            first_click = False
                            timer.init()
                            bomb_counter.init()

                        open_cells: list = get_open_cells(field, cell)
                        boxes_affected: list = [
                            cell_to_box(boxes, field, cell) for cell in open_cells
                        ]
                    else:
                        boxes_affected: list = box_clicked

                    for box in boxes_affected:
                        cell: Cell = field.get_cell_at(*box.coords)

                        if left_click and not cell.is_flag and not cell.clicked:
                            cell.clicked = True

                            if client is not None:
                                client.send_change(cell.row, cell.col, 'HIT')
                            if cell.is_mine:
                                box.set_bomb()
                                mine_hit = True
                                play_button.sad()
                                timer.stop()
                                show_mines(box_group, field)
                            else:
                                box.set_num(repr(cell))
                                play_button.surprised()

                        if right_click:
                            if cell.clicked and not cell.is_flag:
                                continue
                            cell.is_flag = not cell.is_flag
                            field.flagged_count += 1
                            cell.clicked = not cell.clicked

                            if client is not None:
                                client.send_change(cell.row, cell.col, 'FLAG')

                            if cell.is_flag:
                                box.set_flagged()
                                bomb_counter.dec()
                            else:
                                box.set_default()
                                field.flagged_count -= 1
                                bomb_counter.inc()

            elif event.type == pygame.MOUSEBUTTONUP:
                if not mine_hit:
                    play_button.happy()

        # update groups
        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        # refresh
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_minesweeper()
