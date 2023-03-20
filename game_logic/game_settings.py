"""
The game_settings module contains the settings for the game such as:
background , sounds, bullet, ships, aliens, game speed.
"""

import pygame
from utils.constants import (
    BACKGROUNDS,
    SOUNDS,
    GAME_CONSTANTS,
    DIFFICULTIES,
    OTHER,
)


class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width = 1260
        self.screen_height = 700
        # game background images
        self.bg_img = pygame.image.load(BACKGROUNDS['space'])
        self.second_bg = pygame.image.load(BACKGROUNDS['space2'])
        self.third_bg = pygame.image.load(BACKGROUNDS['space4'])
        # other images
        self.game_over = pygame.image.load(OTHER['gameover'])
        self.pause = pygame.image.load(OTHER['pause'])

        # Sounds
        self.fire_sound = pygame.mixer.Sound(SOUNDS['bullet'])

        # Game modes settings
        self.endless_onslaught, self.slow_burn, self.meteor_madness = False, False, False

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
        self.aliens_num = 10
        self.alien_direction = 1

        # Bosses Settings
        self.boss_hp = 50
        self.boss_points = 2500

        # Asteroid settings
        self.asteroid_speed = 1.5
        self.asteroid_freq = 1000

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        if self.alien_speed < GAME_CONSTANTS['MAX_ALIEN_SPEED']:
            self.alien_speed += self.speedup_scale
            self.alien_bullet_speed += self.speedup_scale
        self.alien_points = int(self.alien_points + GAME_CONSTANTS['SCORE_SCALE'])

        if self.aliens_num < GAME_CONSTANTS['MAX_ALIEN_NUM']:
            self.aliens_num += 2

        # bosses have more hp on medium or hard difficulty
        if self.speedup_scale == DIFFICULTIES['MEDIUM']:
            self.boss_hp = 75
        elif self.speedup_scale == DIFFICULTIES['HARD']:
            self.boss_hp = 100
