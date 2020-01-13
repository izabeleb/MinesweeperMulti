"""Theme constant value for resource locations and element sizing."""
import os
import pygame

# image directories
CELL_IMAGE_DIR = f"{os.path.dirname(__file__)}/images/cells"
WIDGET_IMAGE_DIR = f"{os.path.dirname(__file__)}/images/widgets"

# window element sizes
GAME_BAR_HEIGHT = 50
BOX_SIZE = 30
DEFAULT_SCREEN = pygame.display.set_mode((640, 480))
