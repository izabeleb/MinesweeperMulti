# -*- coding: utf-8 -*-
"""
Created on Tue May 21 23:18:46 2019

@author: bauzy
Defines menu builder utility functions.
"""
import pygame
from typing import List
from typing import Tuple
from theme.sprites import Bomb, Button, ColorTheme, InputBox, Label, Mouse


def build_simple_menu(title: str, name_label_list: List[List[str]]) -> Tuple:
    """Build a simple menu with a title and buttons.

    Args:
        title (str): what the title at the top of the menu screen should be
        name_label_list (List[List[str]]): a 2d list of information about each button includes the
            name of the button for identification purposes and the physical display name on how the
            button name will appear on screen like so:
                [
                    [name, nameAsItAppearsOnScreen],
                    [..., ...]
                ]

    Returns:
        (Tuple): Specifying whether the game should be exited, and what button was pressed.
    """
    pygame.font.init()

    height = 200 + (len(name_label_list) * 100)
    screen = pygame.display.set_mode((640, height))

    # entities
    background = pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MENU_BG)
    screen.blit(background, (0, 0))

    mouse = Mouse()
    mouse_group = pygame.sprite.Group(mouse)

    button_group = pygame.sprite.Group()
    label_group = pygame.sprite.Group(
        Label(title, title, (screen.get_width() / 2, 100), 0, None, 60))

    v_pos = 200
    inc = 80

    for label in name_label_list:
        button_group.add(Button(screen.get_width() / 2, v_pos, label[0]))
        label_group.add(
            Label(label[0], label[1], (screen.get_width() / 2, v_pos), 0, ColorTheme.BUTTON))
        v_pos += inc

    bombs = list()
    for i in range(20):
        bombs.append(Bomb(screen))
    bomb_group = pygame.sprite.Group(bombs)

    sprites = [mouse_group, bomb_group, button_group, label_group]

    # assign
    clock = pygame.time.Clock()
    keep_going = True
    done_playing = False
    button_name = str()

    button_last_hovered = str()

    while keep_going:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                done_playing = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in pygame.sprite.spritecollide(mouse, button_group, False):
                    button_name = button.name
                    keep_going = False

        button_hovered = pygame.sprite.spritecollide(mouse, button_group, False)

        if button_hovered:
            for buttonItem in button_group.sprites():
                if buttonItem.name == button_last_hovered:
                    buttonItem.unhover()

            for labelItem in label_group.sprites():
                if labelItem.name == button_last_hovered:
                    labelItem.unhover()
        else:
            for button in pygame.sprite.spritecollide(mouse, button_group, False):
                # a new button is being hovered on
                if button.name != button_last_hovered:
                    for buttonItem in button_group.sprites():
                        if buttonItem.name == button_last_hovered:
                            buttonItem.unhover()

                    for labelItem in label_group.sprites():

                        if labelItem.name == button_last_hovered:
                            labelItem.unhover()

                button.hover()

                button_last_hovered = button.name
                for labelItem in label_group.sprites():
                    if labelItem.name == button_last_hovered:
                        labelItem.hover()

        # move the items
        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        # refresh
        pygame.display.flip()

    return done_playing, button_name


def build_input_menu(*fields: str) -> Tuple:
    """Build a menu taking input for passed fields.

    Args:
        *fields (str): The fields to take input for.

    Returns:
        (Tuple): The values of the passed fields in their respective order.
    """
    pygame.font.init()

    # display
    screen = pygame.display.set_mode((640, 550))

    # entities
    mouse = Mouse()
    mouse_group = pygame.sprite.Group(mouse)

    lbl_group = pygame.sprite.Group()
    txt_group = pygame.sprite.Group()
    input_group = pygame.sprite.Group()

    lbl_height = 100
    input_height = 170

    height_inc = 150
    button_gap = 50

    for input_item in fields:
        lbl_group.add(Label(f"lbl{input_item}", f"{input_item}",
                            (screen.get_width() / 2, lbl_height), 0))
        txt_group.add(InputBox(f"txt{input_item}", (450, 70),
                               (screen.get_width() / 2, input_height)))
        input_group.add(Label(f"txt{input_item}", "",
                              (screen.get_width() / 2, input_height), 0, None, 20, (0, 0, 0)))

        lbl_height += height_inc
        input_height += height_inc

    lbl_save = Label("save", "Save", (screen.get_width() / 2, lbl_height + button_gap), 0)
    btn_save = Button(screen.get_width() / 2, lbl_height + button_gap, "save")

    btn_group = pygame.sprite.Group(btn_save, lbl_save)

    sprites = [mouse_group, lbl_group, txt_group, input_group, btn_group]

    # fix screen size
    screen_height = lbl_height + btn_save.height + button_gap
    screen = pygame.display.set_mode((640, screen_height))

    background=pygame.Surface(screen.get_size())
    background.fill(ColorTheme.MENU_BG)
    screen.blit(background, (0, 0))

    # assign
    clock = pygame.time.Clock()
    keep_going = True
    text_string = str()
    active_text_box = str()

    print(keep_going)
    while keep_going:
        # This block allows backspace key to delete multiple characters
        keys = pygame.key.get_pressed()

        if keys[pygame.K_BACKSPACE]:
            text_string = text_string[:-1]
            for inputLabel in input_group.sprites():
                if inputLabel.name == active_text_box:
                    inputLabel.render_text(text_string)

        # time
        clock.tick(15)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btnClicked in pygame.sprite.spritecollide(mouse, btn_group, False):
                    # save button is clicked
                    keep_going = False

                # textbox is clicked
                for inputClicked in pygame.sprite.spritecollide(mouse, txt_group, False):
                    if inputClicked.name != active_text_box:
                        text_string = ""

                        # unfocus old textbox
                        for inputBox in txt_group.sprites():
                            if inputBox.name == active_text_box:
                                inputBox.unfocus()

                        for inputBox in input_group.sprites():
                            if inputBox.name == active_text_box:
                                inputBox.unfocus()

                        # focus new textbox
                        active_text_box = inputClicked.name
                        for inputBox in txt_group.sprites():
                            if inputBox.name == active_text_box:
                                inputBox.focus()

                        for inputBox in input_group.sprites():
                            if inputBox.name == active_text_box:
                                inputBox.focus()
            elif event.type == pygame.KEYDOWN:
                # add other characters needed for hostnames and ports in a better way
                if (event.key in range(pygame.K_a, pygame.K_z + 1)
                        or event.key in range(pygame.K_0, pygame.K_9 + 1)
                        or event.key == pygame.K_PERIOD
                        or event.key == pygame.K_MINUS):
                    text_string += event.unicode

                    for inputLabel in input_group.sprites():
                        if inputLabel.name == active_text_box:
                            inputLabel.render_text(text_string)

        btn_hovered = pygame.sprite.spritecollide(mouse, btn_group, False)

        if btn_hovered:
            for item in btn_group.sprites():
                item.unhover()
        else:
            for item in btn_group.sprites():
                item.hover()

        # move the items
        for spriteGroup in sprites:
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)

        # refresh
        pygame.display.flip()

    typed_text = list()

    for input_item in input_group:
        typed_text.append(input_item.text)

    return (*typed_text,)
