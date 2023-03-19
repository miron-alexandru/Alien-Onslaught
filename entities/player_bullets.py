"""The player_bullets module contains the classes creating and managing
the ships bullets."""

import pygame
from pygame.sprite import Sprite
from utils.constants import SHIPS


class Thunderbolt(Sprite):
    """A class to manage bullets for Thunderbird ship."""
    def __init__(self, game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load(SHIPS['thunderbolt'])
        self.rect = self.image.get_rect()
        self.rect.midtop = (game.thunderbird_ship.rect.centerx,
                             game.thunderbird_ship.rect.top)

        self.y_pos = float(self.rect.y)


    def update(self):
        """Update the bullet position on screen."""
        self.y_pos -= self.settings.thunderbird_bullet_speed
        self.rect.y = self.y_pos

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)


class Firebird(Thunderbolt):
    """A class to manage bullets for Phoenix ship."""
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load(SHIPS['firebird'])
        self.rect = self.image.get_rect()
        self.rect.midtop = (game.phoenix_ship.rect.centerx,
                             game.phoenix_ship.rect.top)

        self.y_pos = float(self.rect.y)

    def update(self):
        """Update the bullet position on screen."""
        self.y_pos -= self.settings.phoenix_bullet_speed
        self.rect.y = self.y_pos
