"""Defines Mode class for specifying game difficulty and configuration."""
from __future__ import annotations
import json
import os
import typing
from typing import Optional


class Mode:
    """Modify the game mode (easy, normal, hard, etc).

    Args:
        mode (dict): The dictionary representing the game mode.
    """
    EASY = {'height': 10, 'width': 10, "bombs": 25}
    NORMAL = {'height': 20, 'width': 20, "bombs": 100}
    HARD = {'height': 30, 'width': 30, "bombs": 225}

    __NOTIFICATION_EMAIL = "notification_email"

    def __init__(self, mode: dict = None):
        self.__mode = mode

    def store_mode(self):
        """Write the current node to 'settings.json'"""
        with open('settings.json', 'w') as store:
            json.dump(self.__mode, store)

    def height(self) -> int:
        """Retrieve the board mode height."""
        return self.__mode['height']

    def width(self) -> int:
        """Retrieve the width of the game board."""
        return self.__mode['width']

    def bomb_count(self) -> int:
        """Retrieve the amount of bombs in the game board."""
        return self.__mode['bombs']

    def email(self) -> typing.Optional[str]:
        """Retrieve the notification email if present."""
        return self.__mode[Mode.__NOTIFICATION_EMAIL] if Mode.__NOTIFICATION_EMAIL in self.__mode else None

    @staticmethod
    def restore_mode(path='settings.json') -> Optional[Mode]:
        """Build a Mode object from the values stored in a file.

        Args:
            path (str): The path to the file from which to read the mode object.

        Returns:
            (Mode):  The mode object loaded from the file.
        """
        if not os.path.isfile(path):
            return Mode()

        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r') as file_mode:
                mode_json = file_mode.read()
        except json.JSONDecodeError:
            return None

        return Mode(json.loads(mode_json))

    @staticmethod
    def build(height: int, width: int, bombs: int, notification_email: typing.Optional[str]) -> Mode:
        """Build a mode object.

        Args:
            height (int): The height of the board.
            width (int): The width of the board.
            bombs (int): The amount of bombs for the board.
            notification_email (str): the emil to send a ine hit notification to.

        Returns:
            (Mode): The mode object built from the passed values.
        """
        return Mode({"height": height, "width": width, "bombs": bombs, Mode.__NOTIFICATION_EMAIL: notification_email})
