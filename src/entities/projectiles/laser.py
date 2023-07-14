"""
This module contains the Laser class that represents the laser weapon
in the game.
"""

import time
import pygame

from pygame.sprite import Sprite
from src.utils.animation_constants import laser_frames


class Laser(Sprite):
    """The Laser class represents a laser object in the game."""

    def __init__(self, game, ship):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.ship = ship

        self.frames = laser_frames
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.set_laser_frames()
        self.rect.midbottom = ship.rect.midtop

        self.frame_update_rate = 5
        self.frame_counter = 0

        self.duration = 1
        self.start_time = time.time()

    def update(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.set_laser_frames()
            self.frame_counter = 0

        if time.time() - self.start_time >= self.duration or self.ship.state.exploding:
            self.kill()

        if self.settings.game_modes.cosmic_conflict:
            if self.ship == self.game.thunderbird_ship:
                self.rect.midleft = self.ship.rect.midright
            else:
                self.rect.midright = self.ship.rect.midleft
        else:
            self.rect.midbottom = self.ship.rect.midtop

    def draw(self):
        """Draw laser on screen."""
        self.screen.blit(self.image, self.rect)

    def set_laser_frames(self):
        """Set the image of the laser based
        on its current state and game mode.
        """
        if self.settings.game_modes.cosmic_conflict:
            if self.ship == self.game.thunderbird_ship:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], -90
                )
            else:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], 90
                )
            self.rect = self.image.get_rect()
        else:
            self.image = self.frames[self.current_frame]