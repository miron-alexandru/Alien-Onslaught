"""
The 'asteroids_manager' module contains the AsteroidsManager class that manages
the update and creation of asteroids."""

import random
import pygame

from src.entities.asteroid import Asteroid


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

    def handle_asteroids(self, create_at_high_levels=True, force_creation=False):
        """Create, update, and check collisions for asteroids.
        Args:
            create_at_high_levels (bool, optional): Whether to create asteroids when
                the current level is 7 or above. Defaults to True.
            force_creation (bool, optional): Whether to always create and update asteroids.
                Defaults to False.
        """
        if force_creation or (create_at_high_levels and self.game.stats.level >= 7):
            self.create_asteroids()
            self.update_asteroids()
            self.game.collision_handler.check_asteroids_collisions(
                self.game.ships_manager.thunderbird_ship_hit,
                self.game.ships_manager.phoenix_ship_hit,
            )
