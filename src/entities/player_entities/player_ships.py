"""
The 'player_ships' module contains classes for creating the player ships.

Classes:
    - 'Thunderbird': Represents the Thunderbird ship.
    - 'Phoenix': Represents the Phoenix ship.
"""

import os
import pygame

from src.utils.game_utils import BASE_PATH
from src.utils.constants import SHIPS

from src.entities.player_entities.ship import Ship


class Thunderbird(Ship):
    """Class that represents the Thunderbird ship."""

    def __init__(self, game):
        self.screen_rect = game.screen.get_rect()
        super().__init__(
            game,
            os.path.join(BASE_PATH, SHIPS["thunderbird1"]),
            self.screen_rect.left + 10,
        )
        self.missiles_num = game.settings.thunderbird_missiles_num
        self.ship_type = "thunderbird"
        self.offset = -300

    def set_cosmic_conflict_pos(self):
        """Set the ship position for the Cosmic Conflict game mode."""
        if self.game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, -90)
        self.cosmic_conflict_pos = self.screen_rect.left + 10


class Phoenix(Ship):
    """Class that represents the Phoenix ship in the game."""

    def __init__(self, game):
        self.screen_rect = game.screen.get_rect()
        super().__init__(
            game,
            os.path.join(BASE_PATH, SHIPS["phoenix1"]),
            self.screen_rect.right - 50,
        )
        self.missiles_num = game.settings.phoenix_missiles_num
        self.ship_type = "phoenix"
        self.offset = 200

    def set_cosmic_conflict_pos(self):
        """Set the ship position for the Cosmic Conflict game mode."""
        if self.game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, 90)
        self.cosmic_conflict_pos = self.screen_rect.right - 50
