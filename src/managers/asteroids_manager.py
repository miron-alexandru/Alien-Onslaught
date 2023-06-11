"""
The 'asteroids_manager' module contains classes for managing asteroids in the game.

Classes:
    - 'AsteroidsManager': A class that manages the update and creation of asteroids.
"""

import random
import pygame

from entities.asteroid import Asteroid


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
