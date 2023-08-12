"""
The "player_bullets" module contains the Thunderbolt and Firebird classes which
represent the bullets for the Thunderbird and Phoenix ship respectively.
"""

import pygame
from src.entities.projectiles.bullet import Bullet


class Thunderbolt(Bullet):
    """A class to create bullets for Thunderbird ship."""

    def __init__(self, manager, ship, scaled=False):
        super().__init__(
            manager,
            manager.weapons["thunderbird"]["weapon"],
            ship,
            manager.settings.thunderbird_bullet_speed,
        )
        if manager.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, -90)
        if scaled:
            self.scale_bullet(0.5)


class Firebird(Bullet):
    """A class to create bullets for Phoenix ship."""

    def __init__(self, manager, ship, scaled=False):
        super().__init__(
            manager,
            manager.weapons["phoenix"]["weapon"],
            ship,
            manager.settings.phoenix_bullet_speed,
        )
        if manager.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, 90)
        if scaled:
            self.scale_bullet(0.5)
