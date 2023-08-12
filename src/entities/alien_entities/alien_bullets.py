"""
The 'alien_bullets' module contains classes for creating bullets for aliens and bosses.

Classes:
    - 'AlienBullet': A class to manage bullets fired by normal aliens.
    - 'BossBullet': A class to manage bullets fired by the boss aliens.
"""

import random

import pygame
from pygame.sprite import Sprite

from src.utils.constants import LEVEL_PREFIX, ALIEN_BULLETS_IMG
from src.utils.game_utils import (
    load_alien_bullets,
    load_boss_bullets,
    load_single_image,
)
from src.entities.alien_entities.aliens import BossAlien


class AlienBullet(Sprite):
    """A class that manages bullets for the aliens."""

    bullet_images = load_alien_bullets()

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        level_prefix = LEVEL_PREFIX.get(game.stats.level // 4 + 1, "Alien7")
        bullet_name = f"alien_bullet{level_prefix[-1]}"
        self.image = load_single_image(ALIEN_BULLETS_IMG[bullet_name])
        self.rect = self.image.get_rect()
        self._choose_random_alien(game)

    def _choose_random_alien(self, game):
        """Choose a random alien as the source of the bullet."""
        random_alien = random.choice(game.aliens.sprites())
        self.rect.centerx = random_alien.rect.centerx
        self.rect.bottom = random_alien.rect.bottom
        self.y_pos = float(self.rect.y)

        if random_alien.is_baby and not isinstance(random_alien, BossAlien):
            self.scale_bullet(0.7)

    def scale_bullet(self, scale):
        """Scale the bullet image and rect."""
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """Update bullet position."""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos

    def draw(self):
        """Draw the bullet on screen."""
        self.screen.blit(self.image, self.rect)


class BossBullet(Sprite):
    """A class that manages bullets for the boss alien."""

    bullet_images = load_boss_bullets()

    def __init__(self, game, alien):
        """Initialize a new bullet for an alien."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.alien = alien
        self.image = self.bullet_images["boss_bullet2"]
        self.rect = self.image.get_rect()
        self._init_variables(alien)
        self._update_image(game)

    def _init_variables(self, alien):
        """Initialize position and speed variables."""
        self.rect.inflate_ip(-40, -40)
        self.rect.center = alien.rect.center
        self.rect.bottom = alien.rect.bottom
        self.y_pos = float(self.rect.y)
        self.x_vel = random.uniform(-4, 4)

    def _update_image(self, game):
        """Change the bullet image for specific bosses."""
        if self.settings.game_modes.boss_rush:
            image_name = f"boss_bullet{game.stats.level}"
        else:
            image_name = f"normal_bullet{game.stats.level}"

        if image_name in self.bullet_images:
            self.image = self.bullet_images[image_name]

    def update(self):
        """Update the bullet location on screen."""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos
        self.rect.x += round(self.x_vel)

    def draw(self):
        """Draw the bullet on screen."""
        self.screen.blit(self.image, self.rect)
