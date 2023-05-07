"""
The 'asteroid' module contains classes for managing asteroids in the game.

Classes:
    - 'Asteroid': A class that represents the asteroids in the game.
    - 'AsteroidsManager': A class that manages the update and creation of asteroids.
"""

import random
import pygame

from pygame.sprite import Sprite
from utils.animation_constants import asteroid_frames


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
        self.rect.y = self.y_pos

    def draw(self):
        """Draw the asteroid on the screen."""
        self.screen.blit(self.image, self.rect)


class AsteroidsManager:
    """The AsteroidsManager class manages the creation and
    update of the asteroids that appear in the game.
    """

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.last_asteroid_time = 0

    def create_asteroids(self, frequency=random.randint(4000, 10000)):
        """Creates multiple asteroids at random intervals.
        The frequency of asteroid creation is determined by the frequency
        argument, which defaults to a random integer between 4000 and 10000 milliseconds.
        """
        if self.last_asteroid_time == 0:
            self.last_asteroid_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_asteroid_time >= frequency:
            self.last_asteroid_time = current_time
            # Create an asteroid at a random location, at the top of the screen.
            asteroid = Asteroid(self)
            asteroid.rect.x = random.randint(
                0, self.settings.screen_width - asteroid.rect.width
            )
            asteroid.rect.y = random.randint(-100, -40)
            self.game.asteroids.add(asteroid)

    def update_asteroids(self):
        """Update asteroids and remove asteroids that went off screen."""
        self.game.asteroids.update()
        for asteroid in self.game.asteroids.copy():
            if asteroid.rect.y > self.settings.screen_height:
                self.game.asteroids.remove(asteroid)
