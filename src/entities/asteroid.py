"""The 'asteroid' module contains the Asteroid class used to create asteroid instances."""

import random

from pygame.sprite import Sprite
from src.utils.animation_constants import asteroid_frames


class Asteroid(Sprite):
    """A class to represent an asteroid in the game."""

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.speed = self.settings.asteroid_speed

        self.frames = asteroid_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        self._initialize_position()

    def _initialize_position(self):
        """Set the initial position of the asteroid."""
        self.rect = self.frames[0].get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0
        self.y_pos = float(self.rect.y)

    def update(self):
        """Update the asteroid's animation and position."""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]

        self.y_pos += self.speed
        self.rect.y = int(self.y_pos)

    def draw(self):
        """Draw the asteroid on the screen."""
        self.screen.blit(self.image, self.rect)
