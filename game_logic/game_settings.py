"""
The game_settings module contains the settings for the game such as:
background , sounds, bullet, ships, aliens, game speed.
"""
from dataclasses import dataclass
from utils.constants import (
    BACKGROUNDS,
    SOUNDS,
    LEVEL_SOUNDS,
    GAME_CONSTANTS,
    OTHER,
)
from utils.game_utils import load_images, load_sounds


class Settings:
    """A class to store all settings for Alien Onslaught."""
    lv_sounds = load_sounds(LEVEL_SOUNDS)
    game_sounds = load_sounds(SOUNDS)

    def __init__(self):
        """Initialize the game's static settings."""
        self._init_screen_settings()
        self._init_images()
        self._init_sounds()
        self._init_game_settings()
        self.dynamic_settings()

    def _init_screen_settings(self):
        """Initialize screen settings."""
        self.screen_width = 1260
        self.screen_height = 700

    def _init_images(self):
        """Initialize images for the game."""
        self.bg_images = load_images(BACKGROUNDS)
        self.other_images = load_images(OTHER)
        self.bg_img = self.bg_images['space']
        self.second_bg = self.bg_images['space2']
        self.third_bg = self.bg_images['space3']
        self.fourth_bg = self.bg_images['space4']
        self.game_over = self.other_images['gameover']
        self.pause = self.other_images['pause']
        self.game_title = self.other_images['game_title']
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.y = - 270

    def _init_sounds(self):
        """Initialize sounds for the game."""
        self.level_sounds = self.lv_sounds
        self.fire_sound = self.game_sounds['bullet']
        self.menu_music = self.game_sounds['menu']

        self.menu_music.set_volume(0.4)
        self.fire_sound.set_volume(0.1)

    def _init_game_settings(self):
        """Initialize game mode settings."""
        self.gm = GameModes()
        self.ui_options = UIOptions()
        self.speedup_scale = 0.3
        self.missiles_speed = 5.0
        self.immune_time = 5000
        self.scaled_time = 120000
        self.alien_immune_time = 12000

    def dynamic_settings(self):
        """Settings that can change during the game."""
        # Thunderbird settings
        self.thunderbird_ship_speed = 3.5
        self.thunderbird_bullet_speed = 5.0
        self.thunderbird_bullets_allowed = 1
        self.thunderbird_bullet_count = 1
        self.thunderbird_missiles_num = 3

        # Phoenix settings
        self.phoenix_ship_speed = 3.5
        self.phoenix_bullet_speed = 5.0
        self.phoenix_bullets_allowed = 1
        self.phoenix_bullet_count = 1
        self.phoenix_missiles_num = 3

        # Alien Settings
        self.alien_speed = 1.0
        self.alien_bullet_speed = 1.5
        self.alien_points = 1
        self.fleet_rows = 3
        self.last_bullet_rows = 2
        self.aliens_num = 8
        self.alien_direction = 1

        # Bosses Settings
        self.boss_hp = 25 if self.gm.boss_rush else 50
        self.boss_points = 1000 if self.gm.boss_rush else 2500

        # Asteroid settings
        self.asteroid_speed = 1.5
        self.asteroid_freq = 1000

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        if self.alien_speed < GAME_CONSTANTS['MAX_ALIEN_SPEED']:
            self.alien_speed += self.speedup_scale
            self.alien_bullet_speed += self.speedup_scale
        self.alien_points = int(self.alien_points + GAME_CONSTANTS['SCORE_SCALE'])

        if not self.gm.last_bullet and self.aliens_num < GAME_CONSTANTS['MAX_ALIEN_NUM']:
            self.aliens_num += 2



@dataclass
class UIOptions:
    """Represents options for the user interface of the game."""
    paused: bool = False
    show_difficulty: bool = False
    resizable: bool = False
    high_score_saved: bool = False
    show_high_scores: bool = False
    show_game_modes: bool = False


@dataclass
class GameModes:
    """Represents the available game modes for the game"""
    endless_onslaught: bool = False
    slow_burn: bool = False
    meteor_madness: bool = False
    boss_rush: bool = False
    last_bullet: bool = False
    game_mode: str = 'normal'
