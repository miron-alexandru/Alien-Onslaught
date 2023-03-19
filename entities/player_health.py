"""The player_health module contains the class that creates the health for the player(s)"""

import pygame
from pygame.sprite import Sprite
from utils.constants import OTHER


class Heart(Sprite):
    """This class manages the health of the player(s)
    in the game by displaying a heart image on the screen."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(OTHER['heart'])
        self.rect = self.image.get_rect(topleft = (0, 0))

    def blitme(self):
        """Draw image"""
        self.screen.blit(self.image, self.rect)
