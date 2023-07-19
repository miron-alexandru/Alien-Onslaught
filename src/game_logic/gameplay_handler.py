"""
'The gameplay_handler' module contains the GameplayHandler class
which manages the game modes and behavior for every game mode in the game.
"""

import time
import pygame

from src.utils.constants import (
    DIFFICULTIES,
    GAME_CONSTANTS,
    BOSS_LEVELS,
    NORMAL_BOSS_POINTS,
    NORMAL_BOSS_HP_MAP,
    AVAILABLE_BULLETS_MAP,
    AVAILABLE_BULLETS_MAP_SINGLE,
)


class GameplayHandler:
    """The GameplayHandler class manages different gameplay
    behaviors in the game based on the active game modes.
    """

    def __init__(self, game, settings, stats):
        self.game = game
        self.settings = settings
        self.stats = stats
        self.score_board = game.score_board
        self.ships = game.ships

        self.last_increase_time = self.last_decrease_time = self.last_level_time = 0
        self.level_time = 100000

    def create_normal_level_bullets(self, bullets_manager):
        """Create bullets for the normal game."""
        if self.stats.level in BOSS_LEVELS:
            bullets_manager(1, 550, 550)
        else:
            bullets_manager(self.settings.alien_bullets_num, 900, 7500)

    def handle_level_progression(self):
        """Handles the progression of levels in the game for different game modes."""
        if not self.game.aliens:
            if self.settings.game_modes.last_bullet:
                self._prepare_last_bullet_level()
            elif (
                not self.settings.game_modes.meteor_madness
                and not self.settings.game_modes.cosmic_conflict
            ):
                self._prepare_next_level()

            if not self.game.singleplayer:
                self.check_for_player_revive()

    def _prepare_last_bullet_level(self):
        """Level progression handler for the Last Bullet game mode"""
        self._prepare_level()
        self.prepare_last_bullet_bullets()

    def prepare_last_bullet_bullets(self):
        """Prepare the number of bullets in the Last Bullet game mode
        based on the level"""

        available_bullets_map = (
            AVAILABLE_BULLETS_MAP_SINGLE
            if self.game.singleplayer
            else AVAILABLE_BULLETS_MAP
        )

        for bullet_range, bullets in available_bullets_map.items():
            if self.stats.level in bullet_range:
                available_bullets = bullets
                break
        else:
            available_bullets = 50 if self.game.singleplayer else 25

        if not self.game.game_loaded:
            for ship in self.ships:
                ship.remaining_bullets = available_bullets

        self.score_board.render_bullets_num()

    def _prepare_next_level(self):
        """Level progression handler"""
        self._prepare_level()
        self.handle_boss_stats()

    def _prepare_level(self):
        """Common level progression handler"""
        self.reset_game_objects()
        self.settings.increase_speed()
        self.stats.increase_level()
        self.score_board.prep_level()
        self.handle_alien_creation()
        self.game.sound_manager.prepare_level_music()
        self.set_max_alien_bullets(self.settings.speedup_scale)
        self.check_alien_bullets_num()

        for ship in self.ships:
            ship.center_ship()

    def handle_boss_stats(self):
        """Updates stats for bosses based on the game mode."""
        if self.settings.game_modes.boss_rush:
            self.update_boss_rush_info()
            return

        self.update_normal_boss_info()

    def handle_alien_creation(self):
        """Choose what aliens to create for every game mode."""
        match self.settings.game_modes.game_mode:
            case "cosmic_conflict":
                return
            case "meteor_madness":
                return
            case "boss_rush":
                self.game.aliens_manager.create_boss_alien()
                self.game.collision_handler.handled_collisions.clear()
            case "last_bullet":
                self.game.aliens_manager.create_fleet(self.settings.last_bullet_rows)
            case _ if self.stats.level in BOSS_LEVELS:
                self.game.aliens_manager.create_boss_alien()
                self.game.collision_handler.handled_collisions.clear()
            case _:
                self.game.aliens_manager.create_fleet(self.settings.fleet_rows)

    def check_for_player_revive(self):
        """Revive the other player after the third Boss Fight.
        Method used only for multiplayer.
        """
        if self.stats.level == 21:
            if not self.game.phoenix_ship.state.alive:
                self.stats.revive_phoenix(self.game.phoenix_ship)
            if not self.game.thunderbird_ship.state.alive:
                self.stats.revive_thunderbird(self.game.thunderbird_ship)
            self.score_board.create_health()

    def reset_game_objects(self):
        """Clear the screen of game objects."""
        all_groups = [
            self.game.thunderbird_bullets,
            self.game.thunderbird_missiles,
            self.game.thunderbird_laser,
            self.game.phoenix_missiles,
            self.game.phoenix_laser,
            self.game.phoenix_bullets,
            self.game.alien_bullet,
            self.game.powers,
            self.game.asteroids,
        ]

        for group in all_groups:
            group.empty()

        if not self.game.game_loaded:
            self.game.aliens.empty()

    def update_normal_boss_info(self):
        """Updates the points and hp of bosses in the normal game mode."""
        self.settings.boss_points = NORMAL_BOSS_POINTS.get(
            self.stats.level, self.settings.boss_points
        )
        self.settings.boss_hp = NORMAL_BOSS_HP_MAP.get(
            self.stats.level, self.settings.boss_hp
        )

        if self.stats.level in BOSS_LEVELS:
            if self.settings.speedup_scale == DIFFICULTIES["MEDIUM"]:
                self.settings.boss_hp += 25
            elif self.settings.speedup_scale == DIFFICULTIES["HARD"]:
                self.settings.boss_hp += 45

    def update_boss_rush_info(self):
        """Updates the points and hp of bosses in Boss Rush."""
        hp_increment = 17
        points_increment = 575

        if self.settings.speedup_scale == DIFFICULTIES["MEDIUM"]:
            hp_increment += 2
        elif self.settings.speedup_scale == DIFFICULTIES["HARD"]:
            hp_increment += 3

        self.settings.boss_points = 1000 + (self.stats.level - 1) * points_increment

        self.settings.boss_hp = 25 + (self.stats.level - 1) * hp_increment

    def _create_boss_rush_bullets(self, bullets_manager):
        """Creates bullets for bosses in Boss Rush."""
        if self.stats.level < 10:
            bullets_manager(1, 450, 400)
        else:
            bullets_manager(1, 200, 350)

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

        current_time = pygame.time.get_ticks() - self.game.pause_time
        if current_time > self.last_level_time + self.level_time:
            self.last_level_time = current_time
            self._prepare_asteroids_level()

    def _prepare_asteroids_level(self):
        """Level progression handler for the Meteor Madness game mode."""
        self.game.asteroids.empty()

        if self.settings.asteroid_speed < GAME_CONSTANTS["MAX_AS_SPEED"]:
            self.settings.asteroid_speed += 0.3
        if self.settings.asteroid_freq > GAME_CONSTANTS["MAX_AS_FREQ"]:
            self.settings.asteroid_freq -= 100
        self.settings.thunderbird_ship_speed = max(
            2.0, self.settings.thunderbird_ship_speed - 0.2
        )
        self.settings.phoenix_ship_speed = max(
            2.0, self.settings.phoenix_ship_speed - 0.2
        )
        self.stats.thunderbird_score += 2000
        self.score_board.update_high_score()

        self.stats.increase_level()
        self.score_board.prep_level()
        self.score_board.render_high_score()

    def last_bullet(self, thunderbird, phoenix, asteroid_handler):
        """Play the Last Bullet game mode in which the players must fight aliens
        but they have a limited number of bullets, when a player remains with no bullets
        he dies, when both players are out of bullets, the game is over.
        """
        asteroid_handler(create_at_high_levels=True)

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

    def set_last_bullet_bullets(self):
        """Set the number of bullets in the last bullet game mode."""
        if self.settings.game_modes.last_bullet:
            self.settings.thunderbird_bullet_count = 1
            self.settings.phoenix_bullet_count = 1

    def check_remaining_bullets(self):
        """Update the remaining bullets to 0 if the ships
        have not hp left.
        """
        if self.stats.thunderbird_hp < 0:
            self.game.thunderbird_ship.remaining_bullets = 0
        if self.stats.phoenix_hp < 0:
            self.game.phoenix_ship.remaining_bullets = 0
        self.score_board.render_bullets_num()

    def boss_rush(self, asteroid_handler, bullets_manager):
        """Play the Boss Rush game mode in which the players must battle
        a series of increasingly difficult bosses, with each level presenting a new challenge.
        """
        asteroid_handler(force_creation=True)
        self._create_boss_rush_bullets(bullets_manager)

    def endless_onslaught(self, aliens_manager, asteroid_handler):
        """Play the Endless Onslaught game mode,
        where fleets of aliens and asteroids are endlessly swarming towards the player.
        As time goes on, the speed of the aliens and their bullets will increase.
        """
        if len(self.game.aliens) < GAME_CONSTANTS["ENDLESS_MAX_ALIENS"]:
            aliens_manager(self.settings.fleet_rows)

        asteroid_handler(force_creation=True)

        current_time = time.time()
        if current_time - self.last_increase_time >= 90:  # seconds
            self.settings.alien_speed += 0.1
            self.settings.alien_bullet_speed += 0.1
            self.last_increase_time = current_time

    def slow_burn(self, asteroid_handler):
        """Play the Slow Burn game mode, where players must navigate through increasingly
        challenging aliens as the speed of their ship and bullets gradually decreases over time.
        """
        asteroid_handler(force_creation=True)

        current_time = time.time()
        if current_time - self.last_decrease_time >= 90:  # seconds
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
            self.last_decrease_time = current_time

    def cosmic_conflict(self, bullet_collisions, thunderbird_hit, phoenix_hit):
        """Play the Cosmic Conflict game mode where players are fighting against each other."""
        bullet_collisions(thunderbird_hit, phoenix_hit)

    def set_cosmic_conflict_high_score(self):
        """Method used in the Cosmic Conflict game mode which
        sets the high score as the score of the remaining player."""
        if not self.game.phoenix_ship.state.alive:
            self.stats.high_score = self.stats.thunderbird_score
        elif not self.game.thunderbird_ship.state.alive:
            self.stats.high_score = self.stats.phoenix_score

    def reset_cosmic_conflict(self):
        """This method is used when changing the game to
        singleplayer from multiplayer and the game mode is Cosmic Conflict
        to set the Cosmic Conflict setting to False because it is not
        available in singleplayer.
        """
        if self.settings.game_modes.cosmic_conflict:
            self.settings.game_modes.cosmic_conflict = False
            self.settings.game_modes.game_mode = "normal"
