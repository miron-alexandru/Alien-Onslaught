"""
The 'game_settings' module contains the Settings class which stores 
settings for the game. This includes settings
related to the screen, images, game modes, speed, and various entities
such as ships, aliens, bosses, and asteroids.
"""

from src.utils.constants import (
    BACKGROUNDS,
    GAME_CONSTANTS,
    OTHER,
)
from src.utils.game_utils import load_images
from src.utils.game_dataclasses import GameModes, UIOptions


class Settings:
    """A class to store all settings for Alien Onslaught."""

    def __init__(self):
        self._init_screen_settings()
        self._init_images()
        self._init_game_settings()

        # Default Thunderbird settings
        self.starting_thunder_ship_speed = 3.5
        self.starting_thunder_bullet_speed = 5.0
        self.starting_thunder_bullet_count = 1
        self.starting_thunder_bullets_allowed = 3
        self.starting_thunder_hp = 3

        # Default Phoenix settings.
        self.starting_phoenix_ship_speed = 3.5
        self.starting_phoenix_bullet_speed = 5.0
        self.starting_phoenix_bullet_count = 1
        self.starting_phoenix_bullets_allowed = 3
        self.starting_phoenix_hp = 3

        self.dynamic_settings()

    def _init_screen_settings(self):
        """Initialize screen settings."""
        self.screen_width = 1260
        self.screen_height = 700

    def _init_images(self):
        """Initialize images for the game."""
        self.bg_images = load_images(BACKGROUNDS)
        self.misc_images = load_images(OTHER)
        # Background Images
        self.bg_img = self.bg_images["space"]
        self.second_bg = self.bg_images["space2"]
        self.third_bg = self.bg_images["space3"]
        self.fourth_bg = self.bg_images["space4"]
        # Game over and pause images
        self.game_end_img = self.misc_images["gameover"]
        self.game_end_rect = self.game_end_img.get_rect()
        self.pause = self.misc_images["pause"]
        # Game title and cursor images
        self.game_title = self.misc_images["game_title"]
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.y = -270
        self.cursor_img = self.misc_images["cursor"]
        self.cursor_rect = self.cursor_img.get_rect()
        self.game_icon = self.misc_images["game_icon"]

        # Load and Save game title images
        self.load_game_img = self.misc_images["load_game"]
        self.load_game_rect = self.load_game_img.get_rect()

        self.save_game_img = self.misc_images["save_game"]
        self.save_game_rect = self.save_game_img.get_rect()

    def _init_game_settings(self):
        """This method initializes the settings
        related to game modes and user interface options,
        as well as other game-related settings.
        """
        self.game_modes = GameModes()
        self.timed_laser_modes = [
            "boss_rush",
            "cosmic_conflict",
            "meteor_madness",
            "endless_onslaught",
        ]
        self.ui_options = UIOptions()
        self.speedup_scale = 0.2
        self.missiles_speed = 5.0
        self.immune_time = 5000
        self.scaled_time = 60
        self.laser_cooldown = 90
        self.required_kill_count = 45
        self.alien_immune_time = 30
        self.frozen_time = 4
        self.max_alien_speed = 3.8

    def regular_thunder_ship(self):
        """Settings for the regular Thunderbird."""
        self.starting_thunder_ship_speed = 3.5
        self.starting_thunder_bullet_speed = 5.0
        self.starting_thunder_bullet_count = 1
        self.starting_thunder_bullets_allowed = 3
        self.starting_thunder_hp = 3

    def slow_thunder(self):
        """Settings for the slow Thunderbird."""
        self.starting_thunder_ship_speed = 2.2
        self.starting_thunder_bullet_speed = 3.2
        self.starting_thunder_bullet_count = 6
        self.starting_thunder_bullets_allowed = 6
        self.starting_thunder_hp = 5

    def heavy_artillery_thunder(self):
        """Settings for the heavy artillery Thunderbird."""
        self.starting_thunder_ship_speed = 3.0
        self.starting_thunder_bullet_speed = 6.0
        self.starting_thunder_bullet_count = 2
        self.starting_thunder_bullets_allowed = 6
        self.starting_thunder_hp = 1

    def regular_phoenix_ship(self):
        """Settings for the regular Phoenix."""
        self.starting_phoenix_ship_speed = 3.5
        self.starting_phoenix_bullet_speed = 5.0
        self.starting_phoenix_bullet_count = 1
        self.starting_phoenix_bullets_allowed = 3
        self.starting_phoenix_hp = 3

    def fast_phoenix(self):
        """Settings for the fast Phoenix."""
        self.starting_phoenix_ship_speed = 6.0
        self.starting_phoenix_bullet_speed = 8.5
        self.starting_phoenix_bullet_count = 1
        self.starting_phoenix_bullets_allowed = 3
        self.starting_phoenix_hp = 1

    def heavy_artillery_phoenix(self):
        """Settings for the heavy artillery Phoenix."""
        self.starting_phoenix_ship_speed = 3.0
        self.starting_phoenix_bullet_speed = 4.5
        self.starting_phoenix_bullet_count = 4
        self.starting_phoenix_bullets_allowed = 8
        self.starting_phoenix_hp = 2

    def dynamic_settings(self):
        """Settings that can change during the game."""
        # Thunderbird settings
        self.thunderbird_ship_speed = self.starting_thunder_ship_speed
        self.thunderbird_bullet_speed = self.starting_thunder_bullet_speed
        self.thunderbird_bullets_allowed = self.starting_thunder_bullets_allowed
        self.thunderbird_bullet_count = self.starting_thunder_bullet_count
        self.thunderbird_missiles_num = 3

        # Phoenix settings
        self.phoenix_ship_speed = self.starting_phoenix_ship_speed
        self.phoenix_bullet_speed = self.starting_phoenix_bullet_speed
        self.phoenix_bullets_allowed = self.starting_phoenix_bullets_allowed
        self.phoenix_bullet_count = self.starting_phoenix_bullet_count
        self.phoenix_missiles_num = 3

        # Alien Settings
        self.alien_speed = 0.8
        self.alien_bullet_speed = 1.5
        self.alien_points = 1
        self.fleet_rows = 2
        self.last_bullet_rows = 2
        self.aliens_num = 8
        self.alien_direction = 1
        self.alien_bullets_num = 2
        self.max_alien_bullets = 8

        # Bosses Settings
        self.boss_hp = 25 if self.game_modes.boss_rush else 50
        self.boss_points = 1000 if self.game_modes.boss_rush else 2500

        # Asteroid settings
        self.asteroid_speed = 1.5
        self.asteroid_freq = 720

        if self.game_modes.one_life_reign:
            self._set_one_life_reign_settings()

    def _set_one_life_reign_settings(self):
        """Buff the player's ship for the One Life Reign game mode."""
        self.thunderbird_ship_speed += 3.5
        self.thunderbird_bullet_speed += 5.0
        self.thunderbird_bullets_allowed += 3
        self.thunderbird_bullet_count += 1

        self.phoenix_ship_speed += 3.5
        self.phoenix_bullet_speed += 5.0
        self.phoenix_bullets_allowed += 3
        self.phoenix_bullet_count += 1

    def increase_speed(self):
        """Increase the speed and other alien related values."""
        self._increase_alien_speed()
        self.alien_points = int(self.alien_points + GAME_CONSTANTS["SCORE_SCALE"])
        self._increase_alien_count()

    def _increase_alien_speed(self):
        """Increase the speed of aliens and their bullets."""
        if self.alien_speed < self.max_alien_speed:
            self.alien_speed += self.speedup_scale
            self.alien_bullet_speed += self.speedup_scale

    def _increase_alien_count(self):
        """Increase the number of aliens that are appearing."""
        if (
            not self.game_modes.last_bullet
            and self.aliens_num <= GAME_CONSTANTS["MAX_ALIEN_NUM"]
        ):
            self.aliens_num += 2

    def disable_ui_flags(self):
        """Set some UI flags to false."""
        self.ui_options.show_difficulty = False
        self.ui_options.show_high_scores = False
        self.ui_options.show_game_modes = False
        self.ui_options.ship_selection = False
