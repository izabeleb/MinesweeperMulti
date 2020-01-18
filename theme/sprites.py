# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:58:58 2019

@author: bauzy
"""
import random
import time
from typing import Optional
from typing import Tuple
import pygame
from theme.color import ColorTheme
from theme.constants import CELL_IMAGE_DIR, WIDGET_IMAGE_DIR


class Mouse(pygame.sprite.Sprite):
    """Sprite for the cursor."""
    def __init__(self):
        pygame.sprite.Sprite()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        super().__init__()

    def update(self):
        """Update the cursor position."""
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


class Box(pygame.sprite.Sprite):
    """Sprite for each MineField Cell.

    Args:
        size (int): The size for each box.
        coords (Tuple[int, int]): The location coordinates for the sprite.
    """
    def __init__(self, size: int, coords: Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.size = size

        self.default_img = f"{CELL_IMAGE_DIR}/defaultBox.png"
        self.bomb_img = f"{CELL_IMAGE_DIR}/bomb.png"
        self.flag_img = f"{CELL_IMAGE_DIR}/flagged.png"
        self.incorrectly_flagged_img = f"{CELL_IMAGE_DIR}/incorrectlyFlagged.png"

        self.image = pygame.transform.scale(
            pygame.image.load(self.default_img), (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.coords = coords
        super().__init__()

    def set_default(self):
        """Set the image to the default basic box."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.default_img), (self.size, self.size)).convert_alpha()

    def set_bomb(self):
        """Set the image to a bomb."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.bomb_img), (self.size, self.size)).convert_alpha()

    def set_flagged(self):
        """Set the image to a flag."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.flag_img), (self.size, self.size)).convert_alpha()

    def set_num(self, num: int):
        """Set the image to that representing a given single digit number.

        Args:
            num (int): The number to represent.
        """
        self.image = pygame.transform.scale(
            pygame.image.load(f"{CELL_IMAGE_DIR}/{num}.png"), (self.size, self.size)) \
            .convert_alpha()

    def set_incorrectly_flagged(self):
        """Set the image to an incorrect flag."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.incorrectly_flagged_img), (self.size, self.size)).convert_alpha()


class GameBar(pygame.sprite.Sprite):
    """Sprite for game bar (menu bar) ad the top of the game screen.

    Args:
        screen: The screen nto which it should be rendered.
        game_bar_height (int): The height of the game bar.
    """
    def __init__(self, screen, game_bar_height: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((screen.get_width(), game_bar_height))
        self.image.fill(ColorTheme.GAMEBAR)
        self.rect = self.image.get_rect()


class Digit(pygame.sprite.Sprite):
    """Sprite class used for the Timer and BombCounter widget sprites.

    Args:
        width (int): The width for the sprite.
        height (int): The height for the sprite.
        left (int): The x coordinate for the left side of the box.
        top (int): The y coordinate for the top of the box.
        value (int): The number to be displayed by the box.
    """
    def __init__(self, width: int, height: int, left: int, top: int, value: int):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        self.image = self.image = pygame.transform.scale(
            pygame.image.load(f"{WIDGET_IMAGE_DIR}/{value}.png"), (self.width, self.height)) \
            .convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        self.value = value

    def change_digit(self, value: int):
        """Change the number represented by this digit sprite."""
        self.value = value
        self.image = pygame.transform.scale(
            pygame.image.load(f"{WIDGET_IMAGE_DIR}/{self.value}.png"), (self.width, self.height)) \
            .convert_alpha()


class BombCounter(pygame.sprite.Sprite):
    """Keeps track of the amount of bombs.

    Args:
        width (int): The width for the sprite.
        height (int): The height for the sprite.
        digit1 (Digit): The first digit on the timer.
        digit2 (Digit): Thh second digit on the timer
        digit3 (Digit): THe third digit on the timer.
        bomb_num (int): The amount of bombs un-flagged on the MineField.
    """
    def __init__(self, width, height, digit1: Digit, digit2: Digit, digit3: Digit, bomb_num):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(ColorTheme.BOMB_COUNTER)
        self.rect = self.image.get_rect()

        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3

        self.initialized = False
        self.bomb_num = bomb_num

    def init(self):
        """Set the bomb counter to initial default values."""
        self.initialized = True

        self.digit1.change_digit(0)
        self.digit2.change_digit(0)
        self.digit3.change_digit(0)

        self.change_digits()

    def inc(self):
        """Increment the value of bomb_num"""
        self.bomb_num += 1
        self.change_digits()

    def dec(self):
        """Decrement the vale of bomb_nu."""
        self.bomb_num -= 1
        self.change_digits()

    def change_digits(self):
        """Update the values of each digit associated with the bomb counter."""
        count = self.bomb_num

        for digit in (self.digit1, self.digit2, self.digit3):
            if not count:
                break
            digit.change_digit(self.bomb_num % 10)
            count %= 10

        # strBomb = str(self.bombNum)
        #
        # if self.bombNum >= 100:
        #     self.digit1.change_digit(strBomb[0])
        #     self.digit2.change_digit(strBomb[1])
        #     self.digit3.change_digit(strBomb[2])
        #
        # elif self.bombNum >= 10:
        #     self.digit1.change_digit(0)
        #     self.digit2.change_digit(strBomb[0])
        #     self.digit3.change_digit(strBomb[1])
        #
        # else:
        #     self.digit1.change_digit(0)
        #     self.digit2.change_digit(0)
        #     self.digit3.change_digit(strBomb[0])


class Timer(pygame.sprite.Sprite):
    """Keeps track of time with 3 digit sprites.

    Args:
        width (int): The width for the sprite.
        height (int): The height for the sprite.
        digit1 (Digit): The first digit on the timer.
        digit2 (Digit): Thh second digit on the timer
        digit3 (Digit): THe third digit on the timer.
    """
    def __init__(self, width: int, height: int, right: int, top: int, digit1: Digit, digit2: Digit,
                 digit3: Digit):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(ColorTheme.TIMER)
        self.rect = self.image.get_rect()

        self.initialized = False

        self.rect.topright = (right, top)

        self.start_time = 0

        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3

    def init(self):
        """Start timer when the user clicks on a bomb."""
        self.initialized = True
        self.start_time = time.time()

        self.digit1.change_digit(0)
        self.digit2.change_digit(0)
        self.digit3.change_digit(0)

    def update(self):
        """Update the timer to the current time."""
        if self.initialized:
            elapsed_time = round(time.time() - self.start_time)
            string_time = str(elapsed_time)

            if elapsed_time >= 1000:
                self.digit1.change_digit(9)
                self.digit2.change_digit(9)
                self.digit3.change_digit(9)
                self.initialized = False

            if elapsed_time >= 100:
                self.digit1.change_digit(string_time[0])
                self.digit2.change_digit(string_time[1])
                self.digit3.change_digit(string_time[2])

            elif elapsed_time >= 10:
                self.digit2.change_digit(string_time[0])
                self.digit3.change_digit(string_time[1])

            else:
                self.digit3.change_digit(string_time[0])

    def stop(self):
        """Freeze the current state of the time."""
        self.initialized = False


class PlayButton(pygame.sprite.Sprite):
    """Sprite for the play button.

    Args:
        width (int): The width of the pay button.
        height (int): THe height of the ply button.
    """
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        self.happy_img = WIDGET_IMAGE_DIR + "/smiley.png"
        self.sad_img = WIDGET_IMAGE_DIR + "/frowny.png"
        self.surprised_img = WIDGET_IMAGE_DIR + "/surprised.png"

        self.image = pygame.transform.scale(
            pygame.image.load(self.happy_img), (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()

    def happy(self):
        """Show a happy face for the play button."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.happy_img), (self.width, self.height)).convert_alpha()

    def sad(self):
        """Show a sad face for the play button."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.sad_img), (self.width, self.height)).convert_alpha()

    def surprised(self):
        """Show a surprised face for the play button."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.surprised_img), (self.width, self.height)).convert_alpha()


class ModeIndicator(pygame.sprite.Sprite):
    """Sprite indicating the current play mode of the game.

    Args:
        width (int): THe width of the sprite.
        height (int): The height of the sprite.
    """
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        self.img_dir = f"{WIDGET_IMAGE_DIR}/FlaggingModeWidget/"

        self.normal_mode_img = f"{self.img_dir}NormalMode.png"
        self.quick_flagging_mode_img = f"{self.img_dir}FlaggingMode.png"

        self.image = pygame.transform.scale(
            pygame.image.load(self.normal_mode_img), (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()

    def set_quick_flag_mode(self):
        """Display the quick flag mode."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.quick_flagging_mode_img), (self.width, self.height)).convert_alpha()

    def set_normal_mode(self):
        """Display the normal mode."""
        self.image = pygame.transform.scale(
            pygame.image.load(self.normal_mode_img), (self.width, self.height)).convert_alpha()


class Button(pygame.sprite.Sprite):
    """Sprite for buttons.

    Args:
        x_coord (int): The x coordinate for the button.
        y_coord (int): The y coordinate for the button.
        width (int): The width of the button.
        height (int): THe height of the button.
    """
    def __init__(self, x_coord, y_coord, name, width=300, height=70):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(ColorTheme.BUTTON)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_coord
        self.rect.centery = y_coord

    def hover(self):
        """Adjust the color theme of the button while cursor hovers over it."""
        self.image.fill(ColorTheme.BUTTON_HOVER)

    def unhover(self):
        """Adjust the color theme of the button while the cursor is not hovering over it."""
        self.image.fill(ColorTheme.BUTTON)


class Label(pygame.sprite.Sprite):
    """Static object to display text.

    Args:
        name (str): The name of the label.
        text (str): The text displayed by the label.
        loc (tuple): Specifies the x and y coordinates for the label.
        alignment (int): Specifies the type of alignment for the label.
        bg_color (Optional[int, int, int]): The background color for the label.
        size (int): The size of the label.
        color (Tuple[int, int, int]): The color for the label.
    """
    def __init__(self, name: str, text: str, loc: Tuple[int, int], alignment: int,
                 bg_color: Optional[Tuple[int, int, int]] = None, size: int = 30,
                 color: Tuple[int, int, int] = ColorTheme.MENU_TEXT_ITEM):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.text = text
        self.loc = loc
        self.alignment = alignment
        self.color = color
        self.bg_color = bg_color
        self.size = size

        self.font = pygame.font.SysFont("None", size)
        self.image = self.font.render(self.text, 1, self.color, self.bg_color)

        self.rect = self.image.get_rect()

        self.align()

    def align(self):
        """Align the label."""
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

    def render(self):
        """Render the label to the screen."""
        self.image = self.font.render(self.text, 1, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        self.align()

    def render_text(self, text):
        """Render the text to the label."""
        self.text = text
        self.image = self.font.render(self.text, 1, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        self.align()

    def focus(self):
        """Change Label color when receiving focus."""
        self.bg_color = ColorTheme.TEXTBOX_FOCUS
        self.render()

    def unfocus(self):
        """Change label color when not receiving focus."""
        self.bg_color = ColorTheme.TEXTBOX_UNFOCUS
        self.render()

    def hover(self):
        """Change the label color when hovered over by cursor."""
        self.bg_color = ColorTheme.BUTTON_HOVER
        self.render()

    def unhover(self):
        """Change the label color when not hovered over by cursor."""
        self.bg_color = ColorTheme.BUTTON
        self.render()


class Bomb(pygame.sprite.Sprite):
    """Sprite for bombs.

    Args:
        screen: The screen to display the bombs to.
    """
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.img_src = f"{CELL_IMAGE_DIR}/bomb.png"
        self.image = pygame.image.load(self.img_src).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left = random.randint(0, 100)
        self.rect.top = random.randint(0, 100)

        self.x_coord = random.randint(-5, 5)
        self.y_coord = random.randint(-5, 5)

        self.degrees = 0
        self.rotation_speed = random.randint(0, 10)

    def update(self):
        """Update the location and orientation of the bomb."""
        self.rotate()

        if self.rect.right < 0:
            self.rect.left = self.screen.get_width()
        elif self.rect.left > self.screen.get_width():
            self.rect.right = 0
        else:
            self.rect.centerx += self.x_coord

        if self.rect.bottom < 0:
            self.rect.top = self.screen.get_height()
        elif self.rect.top > self.screen.get_height():
            self.rect.bottom = 0
        else:
            self.rect.centery += self.y_coord

    def rotate(self):
        """Animates image."""
        if self.degrees + self.rotation_speed > 360:
            self.degrees = 0
        else:
            self.degrees += self.rotation_speed
        self.image = pygame.transform.rotate(
            pygame.image.load(self.img_src).convert_alpha(), self.degrees)


class InputBox(pygame.sprite.Sprite):
    """Sprite for taking input from user.

    Args:
        name (str): The name of the input box.
        size: The size for the input box.
        loc: The coordinates for the input boc.
    """
    def __init__(self, name: str, size: tuple, loc: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.focused = False
        self.loc = loc

        self.image = pygame.Surface(size)
        self.image.fill(ColorTheme.TEXTBOX_UNFOCUS)
        self.rect = self.image.get_rect()
        self.rect.center = loc

    def focus(self):
        """Change the input box color while receiving focus."""
        self.focused = True
        self.image.fill(ColorTheme.TEXTBOX_FOCUS)

    def unfocus(self):
        """Change the input box color while not receiving focus."""
        self.focused = False
        self.image.fill(ColorTheme.TEXTBOX_UNFOCUS)
