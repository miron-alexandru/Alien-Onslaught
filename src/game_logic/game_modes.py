"""
'The game_modes' module contains the GameModesManager class
which manages the game modes and behavior for every game mode in the game.
"""

import time
import pygame

from utils.constants import (
    DIFFICULTIES,
    GAME_CONSTANTS,
    BOSS_LEVELS,
    BOSS_RUSH_POINTS_MAP,
    NORMAL_BOSS_POINTS,
    BOSS_RUSH_HP_MAP,
    NORMAL_BOSS_HP_MAP,
)


class GameModesManager:
    """The GameModesManager class manages game modes in the game.
    It contains methods that update various game settings for different game modes.
    """

    def __init__(self, game, settings, stats):
        self.game = game
        self.settings = settings
        self.stats = stats

    def update_normal_boss_info(self):
        """Updates the points and hp of bosses in the normal game mode."""
        self.settings.boss_points = NORMAL_BOSS_POINTS.get(
            self.stats.level, self.settings.boss_points
        )
        self.settings.boss_hp = NORMAL_BOSS_HP_MAP.get(
            self.stats.level, self.settings.boss_hp
        )

        if (
            self.stats.level in BOSS_LEVELS
            and self.settings.speedup_scale == DIFFICULTIES["MEDIUM"]
        ):
            self.settings.boss_hp += 25

        if (
            self.stats.level in BOSS_LEVELS
            and self.settings.speedup_scale == DIFFICULTIES["HARD"]
        ):
            self.settings.boss_hp += 45

    def update_boss_rush_info(self):
        """Updates the points and hp of bosses in Boss Rush."""
        self.settings.boss_points = BOSS_RUSH_POINTS_MAP.get(
            self.stats.level, self.settings.boss_points
        )
        self.settings.boss_hp = BOSS_RUSH_HP_MAP.get(
            self.stats.level, self.settings.boss_hp
        )

        if self.settings.speedup_scale == DIFFICULTIES["MEDIUM"]:
            self.settings.boss_hp += 15
        elif self.settings.speedup_scale == DIFFICULTIES["HARD"]:
            self.settings.boss_hp += 25

    def _create_boss_rush_bullets(self, bullets_manager):
        """Creates bullets for bosses in Boss Rush."""
        if self.stats.level < 10:
            bullets_manager(1, 450, 400)
        else:
            bullets_manager(1, 200, 350)

    def create_normal_level_bullets(self, bullets_manager):
        """Create bullets for the normal game."""
        if self.stats.level in BOSS_LEVELS:
            bullets_manager(1, 550, 550)
        else:
            bullets_manager(self.settings.alien_bullets_num, 800, 7000)

    def set_max_alien_bullets(self, difficulty):
        """Set the maximum number of alien bullets based on difficulty."""
        if difficulty == DIFFICULTIES["MEDIUM"]:
            self.settings.max_alien_bullets = 9
        elif difficulty == DIFFICULTIES["HARD"]:
            self.settings.max_alien_bullets = 10

    def check_alien_bullets_num(self):
        """Increase alien bullets number every 3 levels, up to a maximum limit."""
        if (
            self.stats.level % 3 == 0
            and self.settings.alien_bullets_num < self.settings.max_alien_bullets
        ):
            self.settings.alien_bullets_num += 1

    def meteor_madness(
        self,
        create_asteroids,
        update_asteroids,
        collision_handler,
        prepare_level,
        thunderbird_hit,
        phoenix_hit,
    ):
        """Play the Meteor Madness game mode where players must navigate a barrage of asteroids.
        As each level progresses, the number of asteroids coming towards the player will increase,
        and their speed will become more relentless. Additionally, the player's speed will decrease,
        adding an extra layer of challenge to the game.
        """
        create_asteroids(frequency=self.settings.asteroid_freq)
        update_asteroids()
        collision_handler(thunderbird_hit, phoenix_hit)

        if not self.game.ui_options.paused:
            level_time = 60000  # miliseconds
            current_time = pygame.time.get_ticks() - self.game.pause_time
            if current_time > self.game.last_level_time + level_time:
                self.game.last_level_time = current_time
                prepare_level()

    def last_bullet(self, thunderbird, phoenix, asteroid_handler):
        """Play the Last Bullet game mode in which the players must fight aliens
        but they have a limited number of bullets, when a player remains with no bullets
        he dies, when both players are out of bullets, the game is over.
        """
        asteroid_handler(start_at_level_7=True)

        aliens_remaining = len(self.game.aliens.sprites())

        flying_thunder_bullets = sum(
            bullet.rect.left > 0
            and bullet.rect.right < self.settings.screen_width
            and bullet.rect.top > 0
            and bullet.rect.bottom < self.settings.screen_height
            for bullet in self.game.thunderbird_bullets.sprites()
        )

        flying_phoenix_bullets = sum(
            bullet.rect.left > 0
            and bullet.rect.right < self.settings.screen_width
            and bullet.rect.top > 0
            and bullet.rect.bottom < self.settings.screen_height
            for bullet in self.game.phoenix_bullets.sprites()
        )

        if (
            thunderbird.remaining_bullets <= 0 <= flying_thunder_bullets <= 0
            and aliens_remaining > 0
        ):
            thunderbird.state.alive = False

        if (
            phoenix.remaining_bullets <= 0 <= flying_phoenix_bullets <= 0
            and aliens_remaining > 0
        ):
            phoenix.state.alive = False

        if all(not player.state.alive for player in [thunderbird, phoenix]):
            self.stats.game_active = False

    def boss_rush(self, asteroid_handler, bullets_manager):
        """Play the Boss Rush game mode in which the players must battle
        a series of increasingly difficult bosses, with each level presenting a new challenge.
        """
        asteroid_handler(always=True)
        self._create_boss_rush_bullets(bullets_manager)

    def endless_onslaught(self, aliens_manager, asteroid_handler):
        """Play the Endless Onslaught game mode,
        where fleets of aliens and asteroids are endlessly swarming towards the player.
        As time goes on, the speed of the aliens and their bullets will increase.
        """
        if len(self.game.aliens) < GAME_CONSTANTS["ENDLESS_MAX_ALIENS"]:
            aliens_manager(self.settings.fleet_rows)

        asteroid_handler(always=True)

        # Increase alien and bullet speed every 120 seconds
        current_time = time.time()
        if current_time - self.game.last_increase_time >= 120:  # seconds
            self.settings.alien_speed += 0.1
            self.settings.alien_bullet_speed += 0.1
            self.game.last_increase_time = current_time

    def slow_burn(self, asteroid_handler):
        """Play the Slow Burn game mode, where players must navigate through increasingly
        challenging aliens as the speed of their ship and bullets gradually decreases over time.
        """
        asteroid_handler(always=True)

        current_time = time.time()
        if current_time - self.game.last_increase_time >= 120:  # seconds
            self.settings.thunderbird_ship_speed = max(
                2.0, self.settings.thunderbird_ship_speed - 0.2
            )
            self.settings.phoenix_ship_speed = max(
                2.0, self.settings.phoenix_ship_speed - 0.2
            )
            self.settings.thunderbird_bullet_speed = max(
                2.0, self.settings.thunderbird_bullet_speed - 0.2
            )
            self.settings.phoenix_bullet_speed = max(
                2.0, self.settings.phoenix_bullet_speed - 0.2
            )
            self.game.last_increase_time = current_time
