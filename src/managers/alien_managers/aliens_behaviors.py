"""
The 'aliens_behaviors' module contains classes for managing alien behaviors like
movement and animations.

Classes:
    - 'AlienMovement': A class that manages the movement of aliens.
    - 'AlienAnimation': This class manages the animation for normal aliens.
"""


import math
import random
import pygame

from src.utils.constants import LEVEL_PREFIX
from src.utils.game_utils import load_alien_images


class AlienMovement:
    """Manages the creation, update, and behavior
    of a fleet of aliens and bosses in a game.
    """

    def __init__(self, alien, game):
        self.alien = alien
        self.settings = game.settings

        self.direction = self.settings.alien_direction
        self.last_direction_change = pygame.time.get_ticks()
        self.direction_change_delay = 0

        self.sins = {
            "time_offset": random.uniform(0, 2 * math.pi),
            "amplitude": random.randint(1, 2),
            "frequency": random.uniform(0.001, 0.005),
        }

    def update_horizontal_position(self):
        """Update the horizontal position of the alien and
        create random movement.
        """
        now = pygame.time.get_ticks()
        if now - self.last_direction_change > self.direction_change_delay:
            # Check if alien is not near the edge of the screen
            if not self.alien.check_edges():
                self.direction *= -1
            self.last_direction_change = now
            # how often the direction changes
            self.direction_change_delay = random.randint(5000, 15000)  # miliseconds

    def update_vertical_position(self):
        """Update the vertical position of the alien and
        create random movement.
        """
        now = pygame.time.get_ticks()
        current_time = now + self.sins["time_offset"]
        self.alien.rect.y = round(
            self.alien.rect.y
            + self.sins["amplitude"] * math.sin(self.sins["frequency"] * current_time)
            + 0.1
        )


class AlienAnimation:
    """This class manages the animation of an alien,
    based on its level prefix. The alien frames are chosen
    based on the current level in the game.
    """

    def __init__(self, game, alien, scale=1.0):
        self.alien = alien
        self.game = game
        self.scale = scale

        self.frame_update_rate = 6
        self.frame_counter = 0
        self.current_frame = 0

        self.frames = {}

        level_prefix = LEVEL_PREFIX.get(game.stats.level // 4 + 1, "Alien7")
        if level_prefix not in self.frames:
            self.frames[level_prefix] = load_alien_images(level_prefix)

        self.frames = self.frames[level_prefix]
        self.image = self.frames[self.current_frame]

    def _update_scale(self):
        """Scale the alien frames."""
        scaled_w = int(self.image.get_width() * self.scale)
        scaled_h = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.frames = [
            pygame.transform.scale(frame, (scaled_w, scaled_h)) for frame in self.frames
        ]

    def update_animation(self):
        """Update alien animation."""
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.frame_counter = 0

    def change_scale(self, scale):
        """Update scale of Alien."""
        self.scale = scale
        self._update_scale()

    def get_current_image(self):
        """Return the current alien image."""
        return self.image
