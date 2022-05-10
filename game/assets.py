import pygame
from game.constants import UOM_LOGO_PATH, HEADER_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT


class Assets():
    def __init__(self, background_path):
        original_image = pygame.image.load(
            UOM_LOGO_PATH)
        self.uom_logo = pygame.transform.scale(
            original_image, (original_image.get_rect().width * HEADER_HEIGHT / original_image.get_rect().height, HEADER_HEIGHT))
        original_image = pygame.image.load(
            background_path)
        self.background_image = pygame.transform.scale(
            original_image, (BOARD_WIDTH, BOARD_HEIGHT))
