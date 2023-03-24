"""
The game_stats module contains code that manages the statistics that change during the game.
"""
from utils.constants import STARTING_HP, MAX_HP


class GameStats:
    """Track statistics for the game."""
    def __init__(self, game, phoenix_ship, thunderbird_ship):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats(phoenix_ship, thunderbird_ship)
        self.game_active = False
        self.high_score = 0

    def reset_stats(self, phoenix_ship, thunderbird_ship):
        """Initialize statistics that can change during the game."""
        phoenix_ship.state['alive'] = True
        thunderbird_ship.state['alive'] = True
        self.phoenix_hp = self.thunderbird_hp = STARTING_HP
        self.max_hp = MAX_HP
        self.thunder_bullets = self.settings.thunderbird_bullet_count
        self.fire_bullets = self.settings.phoenix_bullet_count
        self.thunderbird_score = 0
        self.phoenix_score = 0
        self.level = 1

    def increase_level(self):
        """Increases the level by one"""
        self.level += 1
