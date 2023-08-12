"""
The 'game_stats' module contains the GameStats class
that manages the statistics that can change during the game.
"""

from src.utils.constants import MAX_HP
from src.utils.game_utils import play_sound


class GameStats:
    """The GameStats class tracks statistics such as the current
    health of the ships, the number of bullets for each ship,
    the scores, and the level. It also provides methods
    for resetting the statistics and increasing the level.
    """

    def __init__(self, game, phoenix_ship, thunderbird_ship):
        self.game = game
        self.settings = game.settings
        self.phoenix_hp, self.thunderbird_hp, self.max_hp = 0, 0, 0
        self.reset_stats(phoenix_ship, thunderbird_ship)
        self.game_active = False
        self.high_score = 0

    def reset_stats(self, phoenix_ship, thunderbird_ship):
        """Resets the statistics to their initial values."""
        phoenix_ship.state.alive = True
        thunderbird_ship.state.alive = True
        self.max_hp = MAX_HP
        self.thunderbird_score = 0
        self.phoenix_score = 0
        self.level = 1
        self.high_score = 0
        self.thunder_bullets = self.game.settings.thunderbird_bullet_count
        self.fire_bullets = self.game.settings.phoenix_bullet_count
        self.phoenix_hp = self.settings.starting_phoenix_hp
        self.thunderbird_hp = self.settings.starting_thunder_hp

        if self.settings.game_modes.one_life_reign:
            self._set_one_life_reign_stats()

    def increase_level(self):
        """Increases the level by one."""
        self.level += 1

    def _set_one_life_reign_stats(self):
        """Set ship hp and max hp for the One Life Reign game mode"""
        self.phoenix_hp = self.thunderbird_hp = 0
        self.max_hp = 1

    def revive_thunderbird(self, ship):
        """Revive Thunderbird"""
        self.thunderbird_hp = 1
        self._revive_ship(ship)

    def revive_phoenix(self, ship):
        """Revive Phoenix"""
        self.phoenix_hp = 1
        self._revive_ship(ship)

    def _revive_ship(self, ship):
        """Revive the ship"""
        ship.state.alive = True
        ship.reset_ship_state()
        ship.center_ship()
        ship.start_warp()
        play_sound(self.game.sound_manager.game_sounds, "warp")

        if self.settings.game_modes.last_bullet:
            self.game.score_board.render_bullets_num()
