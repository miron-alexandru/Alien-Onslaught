"""
The asteroid module contains the class for creating instances of asteroids in the game.
"""

import random
import pygame

from pygame.sprite import Sprite
from utils.game_utils import load_frames


class Asteroid(Sprite):
    """This class is responsible for managing the position
    and animation of asteroids in the game."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.speed = self.settings.asteroid_speed

        self.frames = []
        load_frames('asteroid/Asteroid-A-09-{:03d}.png', 120, self.frames)
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

    def draw_asteroid(self):
        """Draw the asteroid"""
        self.screen.blit(self.image, self.rect)



class AsteroidsManager:
    """The AsteroidsManager class manages the creation and
    update of the asteroids that appear on the game screen."""
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.last_asteroid_time = 0

    def create_asteroids(self):
        """Create multiple asteroids"""
        if self.last_asteroid_time == 0:
            self.last_asteroid_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        # change the range to determine how often asteroids are created.
        if current_time - self.last_asteroid_time >= random.randint(4000, 10000): # miliseconds
            self.last_asteroid_time = current_time
            # create asteroid at a random location, at the top of the screen.
            asteroid = Asteroid(self)
            asteroid.rect.x = random.randint(0, self.settings.screen_width - asteroid.rect.width)
            asteroid.rect.y = random.randint(-100, -40)
            self.game.asteroids.add(asteroid)


    def update_asteroids(self):
        """Update asteroids and remove asteroids that went off screen."""
        self.game.asteroids.update()
        for asteroid in self.game.asteroids.copy():
            if asteroid.rect.bottom <= 0:
                self.game.asteroids.remove(asteroid)
