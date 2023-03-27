"""The game_modes module manages the game modes and behavior for every game mode in the game."""

import time
import pygame

from utils.constants import (
    DIFFICULTIES, GAME_CONSTANTS,
    BOSS_LEVELS, boss_rush_points_map,
    normal_boss_points, boss_rush_hp_map,
    normal_boss_hp_map,
)

class GameModesManager:
    """The GameModesManager class manages game modes in the game."""
    def __init__(self, game, settings, stats):
        self.game = game
        self.settings = settings
        self.stats = stats

    def update_normal_boss_info(self):
        """Updates the points and hp of bosses in the other game modes."""
        self.settings.boss_points = (
             normal_boss_points.get(self.stats.level, self.settings.boss_points))
        self.settings.boss_hp = normal_boss_hp_map.get(self.stats.level, self.settings.boss_hp)

        if (self.stats.level in BOSS_LEVELS and
             self.settings.speedup_scale == DIFFICULTIES['MEDIUM']):
            self.settings.boss_hp += 25

        if self.stats.level in BOSS_LEVELS and self.settings.speedup_scale == DIFFICULTIES['HARD']:
            self.settings.boss_hp += 50


    def update_boss_rush_info(self):
        """Updates the points and hp of bosses in Boss Rush"""
        self.settings.boss_points = (
            boss_rush_points_map.get(self.stats.level, self.settings.boss_points))
        self.settings.boss_hp = boss_rush_hp_map.get(self.stats.level, self.settings.boss_hp)

        if self.settings.speedup_scale == DIFFICULTIES['MEDIUM']:
            self.settings.boss_hp += 25
        elif self.settings.speedup_scale == DIFFICULTIES['HARD']:
            self.settings.boss_hp += 50


    def _create_boss_rush_bullets(self, bullets_manager):
        """Creates bullets for bosses in Boss Rush."""
        if self.stats.level < 10:
            bullets_manager(1, 500, 500)
        else:
            bullets_manager(1, 200, 200)


    def create_normal_level_bullets(self, bullets_manager):
        """Create bullets for the normal game."""
        if self.stats.level in BOSS_LEVELS:
            bullets_manager(1, 500, 500)

        else:
            bullets_manager(4, 4500, 7000)


    def meteor_madness(self, create_asteroids, update_asteroids, collision_handler,
                        prepare_level, thunderbird_hit, phoenix_hit):
        """Starts the Meteor Madness game mode where players must navigate a barrage of asteroids.
        As each level progresses, the number of asteroids coming towards the player will increase,
        and their speed will become more relentless. Additionally, the player's speed will decrease,
        adding an extra layer of challenge to the game."""
        create_asteroids(frequency=self.settings.asteroid_freq)
        update_asteroids()
        collision_handler(thunderbird_hit, phoenix_hit)

        if not self.game.paused:
            level_time = 60000 # miliseconds
            current_time = pygame.time.get_ticks() - self.game.pause_time
            if current_time > self.game.last_level_time + level_time:
                self.game.last_level_time = current_time
                prepare_level()


    def boss_rush(self, asteroid_handler, bullets_manager):
        """ Starts the Boss Rush game mode in which the players must battle
        a series of increasingly difficult bosses, with each level presenting a new challenge."""
        asteroid_handler(always=True)
        self._create_boss_rush_bullets(bullets_manager)


    def endless_onslaught(self, aliens_manager, asteroid_handler):
        """Starts the Endless Onslaught game mode,
        where fleets of aliens and asteroids swarm towards the player.
        As time goes on, the speed of the aliens and their bullets will increase."""
        if len(self.game.aliens) < GAME_CONSTANTS['ENDLESS_MAX_ALIENS']:
            aliens_manager()

        asteroid_handler(always=True)

        # Increase alien and bullet speed every 120 seconds
        current_time = time.time()
        if current_time - self.game.last_increase_time >= 120: # seconds
            self.settings.alien_speed += 0.1
            self.settings.alien_bullet_speed += 0.1
            self.game.last_increase_time = current_time


    def slow_burn(self, asteroid_handler):
        """Starts the Slow Burn game mode, where players must navigate through increasingly
        challenging aliens as the speed of their ship and bullets gradually decreases over time."""
        asteroid_handler(always=True)

        current_time = time.time()
        if current_time - self.game.last_increase_time >= 120: # seconds
            self.settings.thunderbird_ship_speed = max(2.0,
                                                    self.settings.thunderbird_ship_speed - 0.2)
            self.settings.phoenix_ship_speed = max(2.0, self.settings.phoenix_ship_speed - 0.2)
            self.settings.thunderbird_bullet_speed = max(2.0,
                                                     self.settings.thunderbird_bullet_speed - 0.2)
            self.settings.phoenix_bullet_speed = max(2.0,self.settings.phoenix_bullet_speed - 0.2)
            self.game.last_increase_time = current_time
