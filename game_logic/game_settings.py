"""
The game_settings module contains the settings for the game such as:
background , sounds, bullet, ships, aliens, game speed.
"""
from dataclasses import dataclass
from utils.constants import (
    BACKGROUNDS,
    SOUNDS,
    GAME_CONSTANTS,
    OTHER,
)
from utils.game_utils import load_images, load_sounds


class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width = 1260
        self.screen_height = 700
        # load images and sounds
        self.bg_images = load_images(BACKGROUNDS)
        self.other_images = load_images(OTHER)
        self.sounds = load_sounds(SOUNDS)
        # define background images
        self.bg_img = self.bg_images['space']
        self.second_bg = self.bg_images['space2']
        self.third_bg = self.bg_images['space4']
        # define other images
        self.game_over = self.other_images['gameover']
        self.pause = self.other_images['pause']
        self.game_title = self.other_images['game_title']

        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.y = - 270

        # define sounds
        self.fire_sound = self.sounds['bullet']

        # Game modes settings
        self.gm = GameModes()
        # UiOptions
        self.ui_options = UIOptions()
        # How quickly the game speeds up
        self.speedup_scale = 0.3

        self.dynamic_settings()


    def dynamic_settings(self):
        """Settings that can change during the game."""
        # Thunderbird settings
        self.thunderbird_ship_speed = 3.5
        self.thunderbird_bullet_speed = 5.0
        self.thunderbird_bullets_allowed = 1
        self.thunderbird_bullet_count = 1

        # Phoenix settings
        self.phoenix_ship_speed = 3.5
        self.phoenix_bullet_speed = 5.0
        self.phoenix_bullets_allowed = 1
        self.phoenix_bullet_count = 1

        # Alien Settings
        self.alien_speed = 1.0
        self.alien_bullet_speed = 1.5
        self.alien_points = 1
        self.fleet_rows = 3
        self.last_bullet_rows = 2
        self.aliens_num = 10
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
