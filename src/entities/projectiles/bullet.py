"""The 'bullet' module contains the Bullet base class used to create player bullets."""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A base class used to create bullets."""

    def __init__(self, game, image_path, ship, speed):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.game = game
        self.speed = speed
        self.ship = ship
        self.image = image_path

        self.rect = self.image.get_rect()
        self.rect.midtop = (ship.rect.centerx, ship.rect.top)
        self.y_pos = float(self.rect.y)
        self.x_pos = float(self.rect.x)

    def update(self):
        """Update the bullet location on screen."""
        if self.game.settings.game_modes.cosmic_conflict:
            self.x_pos += (
                self.speed if self.ship == self.game.thunderbird_ship else -self.speed
            )
            self.rect.x = int(self.x_pos)
        else:
            self.y_pos -= self.speed
            self.rect.y = int(self.y_pos)

    def draw(self):
        """Draw the bullet on screen."""
        self.game.screen.blit(self.image, self.rect)

    def scale_bullet(self, scale):
        """Scale the bullet image and rect."""
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )
        self.rect = self.image.get_rect(center=self.rect.center)
