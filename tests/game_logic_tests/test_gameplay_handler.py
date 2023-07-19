"""
This module tests the GameplayHandler class which is used to manage the game modes
and gameplay behaviors in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.game_logic.gameplay_handler import GameplayHandler
from src.game_logic.game_settings import Settings


class TestGameplayManager(unittest.TestCase):
    """Test cases for the GameplayManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.settings = Settings()
        self.thunderbird_ship = MagicMock()
        self.phoenix_ship = MagicMock()
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.game.ships = self.ships
        self.game.aliens = pygame.sprite.Group()
        self.gameplay_handler = GameplayHandler(
            self.game, self.settings, self.game.stats
        )

    def test_create_normal_level_bullets(self):
        """Test the creation of bullets in normal game mode."""
        # Normal level case
        bullets_manager = MagicMock()

        self.gameplay_handler.create_normal_level_bullets(bullets_manager)

        bullets_manager.assert_called_once_with(
            self.settings.alien_bullets_num, 900, 7500
        )

        # Boss level case
        bullets_manager.reset_mock()
        self.game.stats.level = 10  # Boss level

        self.gameplay_handler.create_normal_level_bullets(bullets_manager)

        bullets_manager.assert_called_once_with(1, 550, 550)

    def test_handle_level_progression(self):
        """Test the handle_level_progression method in multiplayer."""
        self.game.singleplayer = False
        self.settings.game_modes.last_bullet = False
        self.settings.game_modes.meteor_madness = False
        self.gameplay_handler.check_for_player_revive = MagicMock()
        self.gameplay_handler._prepare_next_level = MagicMock()

        self.gameplay_handler.handle_level_progression()

        self.gameplay_handler._prepare_next_level.assert_called_once()
        self.gameplay_handler.check_for_player_revive.assert_called_once()

    def test_handle_level_progression_last_bullet(self):
        """Test the handle_level_progression in the last bullet game mode."""
        self.game.singleplayer = True
        self.settings.game_modes.last_bullet = True
        self.gameplay_handler._prepare_last_bullet_level = MagicMock()
        self.gameplay_handler.check_for_player_revive = MagicMock()

        self.gameplay_handler.handle_level_progression()

        self.gameplay_handler._prepare_last_bullet_level.assert_called_once()
        self.gameplay_handler.check_for_player_revive.assert_not_called()

    def test_handle_level_progression_meteor_madness(self):
        """Test the handle_level_progression in the meteor madness game mode."""
        self.settings.game_modes.last_bullet = False
        self.settings.game_modes.meteor_madness = True
        self.gameplay_handler._prepare_next_level = MagicMock()
        self.gameplay_handler.check_for_player_revive = MagicMock()
        self.gameplay_handler._prepare_last_bullet_level = MagicMock()

        self.gameplay_handler.handle_level_progression()

        self.gameplay_handler._prepare_next_level.assert_not_called()
        self.gameplay_handler.check_for_player_revive.assert_not_called()
        self.gameplay_handler._prepare_last_bullet_level.assert_not_called()

    def test__prepare_last_bullet_level(self):
        """Test the prepare_last_bullet_level method."""
        self.gameplay_handler._prepare_level = MagicMock()
        self.gameplay_handler.prepare_last_bullet_bullets = MagicMock()

        self.gameplay_handler._prepare_last_bullet_level()

        self.gameplay_handler._prepare_level.assert_called_once()
        self.gameplay_handler.prepare_last_bullet_bullets.assert_called_once()

    def test_prepare_last_bullet_bullets_singleplayer(self):
        """Test the prepare_last_bullet_bullets in singleplayer."""
        self.game.singleplayer = True
        self.game.game_loaded = False
        self.gameplay_handler.score_board.render_bullets_num = MagicMock()

        self.gameplay_handler.prepare_last_bullet_bullets()

        for ship in self.ships:
            self.assertEqual(ship.remaining_bullets, 50)

        self.gameplay_handler.score_board.render_bullets_num.assert_called_once()

    def test_prepare_last_bullet_bullets_multiplayer(self):
        """Test the prepare_last_bullet_bullets in multiplayer."""
        self.game.singleplayer = False
        self.game.game_loaded = False
        self.gameplay_handler.score_board.render_bullets_num = MagicMock()

        self.gameplay_handler.prepare_last_bullet_bullets()

        for ship in self.ships:
            self.assertEqual(ship.remaining_bullets, 25)

        self.gameplay_handler.score_board.render_bullets_num.assert_called_once()

    def test__prepare_next_level(self):
        """Test the prepare_next_level method."""
        self.gameplay_handler._prepare_level = MagicMock()
        self.gameplay_handler.handle_boss_stats = MagicMock()

        self.gameplay_handler._prepare_next_level()

        self.gameplay_handler._prepare_level.assert_called_once()
        self.gameplay_handler.handle_boss_stats.assert_called_once()

    def test__prepare_level(self):
        """Test the prepare_level method."""
        self.gameplay_handler.reset_game_objects = MagicMock()
        self.settings.increase_speed = MagicMock()
        self.gameplay_handler.handle_alien_creation = MagicMock()
        self.gameplay_handler.set_max_alien_bullets = MagicMock()
        self.gameplay_handler.check_alien_bullets_num = MagicMock()

        self.gameplay_handler._prepare_level()

        self.gameplay_handler.reset_game_objects.assert_called_once()
        self.settings.increase_speed.assert_called_once()
        self.game.stats.increase_level.assert_called_once()
        self.game.score_board.prep_level.assert_called_once()
        self.gameplay_handler.handle_alien_creation.assert_called_once()
        self.game.sound_manager.prepare_level_music.assert_called_once()
        self.gameplay_handler.set_max_alien_bullets.assert_called_once_with(
            self.settings.speedup_scale
        )
        self.gameplay_handler.check_alien_bullets_num.assert_called_once()

        for ship in self.ships:
            ship.center_ship.assert_called_once()

    def test_handle_boss_stats(self):
        """Test the handle_boss_stats method."""
        # Boss rush game mode case
        self.settings.game_modes.boss_rush = True
        self.gameplay_handler.update_boss_rush_info = MagicMock()
        self.gameplay_handler.update_normal_boss_info = MagicMock()

        self.gameplay_handler.handle_boss_stats()

        self.gameplay_handler.update_boss_rush_info.assert_called_once()
        self.gameplay_handler.update_normal_boss_info.assert_not_called()

        # Other game modes case
        self.gameplay_handler.update_boss_rush_info.reset_mock()
        self.gameplay_handler.update_normal_boss_info.reset_mock()
        self.settings.game_modes.boss_rush = False

        self.gameplay_handler.handle_boss_stats()

        self.gameplay_handler.update_boss_rush_info.assert_not_called()
        self.gameplay_handler.update_normal_boss_info.assert_called_once()

    def test_handle_alien_creation_cosmic_conflict(self):
        """Test the handle_alien_creation in the cosmic conflict game mode."""
        self.settings.game_modes.game_mode = "cosmic_conflict"

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_boss_alien.assert_not_called()
        self.game.aliens_manager.create_fleet.assert_not_called()

    def test_handle_alien_creation_meteor_madness(self):
        """Test the handle_alien_creation in the meteor madness game mode."""
        self.settings.game_modes.game_mode = "meteor_madness"

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_boss_alien.assert_not_called()
        self.game.aliens_manager.create_fleet.assert_not_called()

    def test_handle_alien_creation_boss_rush(self):
        """Test the handle_alien_creation in the boss rush game mode."""
        self.settings.game_modes.game_mode = "boss_rush"

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_boss_alien.assert_called_once()
        self.game.collision_handler.handled_collisions.clear.assert_called_once()
        self.game.aliens_manager.create_fleet.assert_not_called()

    def test_handle_alien_creation_last_bullet(self):
        """Test the handle_alien_creation in the last bullet game mode."""
        self.settings.game_modes.game_mode = "last_bullet"

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_fleet.assert_called_once_with(
            self.settings.last_bullet_rows
        )

    def test_handle_alien_creation_boss_level(self):
        """Test the handle alien creation for the boss levels in the other game modes."""
        self.settings.game_modes.game_mode = "Normal"
        self.game.stats.level = 10

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_boss_alien.assert_called_once()
        self.game.collision_handler.handled_collisions.clear.assert_called_once()
        self.game.aliens_manager.create_fleet.assert_not_called()

    def test_handle_alien_creation_regular_level(self):
        """Test the handle_alien_creation in the regular levels."""
        self.settings.game_modes.game_mode = "other_game_mode"
        self.game.stats.level = 3

        self.gameplay_handler.handle_alien_creation()

        self.game.aliens_manager.create_fleet.assert_called_once_with(
            self.settings.fleet_rows
        )
        self.game.aliens_manager.create_boss_alien.assert_not_called()

    def test_check_for_player_revive(self):
        """Test the check_for_player revive method."""
        self.game.stats.level = 21
        self.game.phoenix_ship.state.alive = False
        self.game.thunderbird_ship.state.alive = False

        self.gameplay_handler.check_for_player_revive()

        self.game.stats.revive_phoenix.assert_called_once_with(self.game.phoenix_ship)
        self.game.stats.revive_thunderbird.assert_called_once_with(
            self.game.thunderbird_ship
        )
        self.game.score_board.create_health.assert_called_once()

    def test_reset_game_objects(self):
        """Test the reset_game_objects method."""
        self.game.game_loaded = False
        self.game.aliens.empty = MagicMock()

        self.gameplay_handler.reset_game_objects()

        self.game.thunderbird_bullets.empty.assert_called_once()
        self.game.thunderbird_missiles.empty.assert_called_once()
        self.game.thunderbird_laser.empty.assert_called_once()
        self.game.phoenix_missiles.empty.assert_called_once()
        self.game.phoenix_laser.empty.assert_called_once()
        self.game.phoenix_bullets.empty.assert_called_once()
        self.game.alien_bullet.empty.assert_called_once()
        self.game.powers.empty.assert_called_once()
        self.game.aliens.empty.assert_called_once()
        self.game.asteroids.empty.assert_called_once()

    def test_update_normal_boss_info(self):
        """Test the update_normal_boss_info method."""
        self.game.stats.level = 10  # Boss level
        initial_boss_hp = self.settings.boss_hp

        self._update_normal_boss_info_helper(0.4, initial_boss_hp, 25)
        self._update_normal_boss_info_helper(0.6, initial_boss_hp, 45)

    def _update_normal_boss_info_helper(
        self, difficulty, initial_boss_hp, increase_amount
    ):
        """Helper method used to test the update of normal boss info
        for different difficulties."""
        self.settings.speedup_scale = difficulty
        self.gameplay_handler.update_normal_boss_info()

        self.assertEqual(self.settings.boss_hp, initial_boss_hp + increase_amount)

    def test_update_boss_rush_info(self):
        """Test the update_boss_rush_info method."""
        self.game.stats.level = 5
        self.settings.boss_points = 0
        self.settings.boss_hp = 0

        self._update_boss_rush_info_helper(0.4, 101)
        self._update_boss_rush_info_helper(0.6, 105)

    def _update_boss_rush_info_helper(self, difficulty, expected_hp):
        """Helper method used to test the update of boss rush info
        with different difficulties."""
        self.settings.speedup_scale = difficulty
        self.gameplay_handler.update_boss_rush_info()

        self.assertEqual(self.settings.boss_points, 3300)
        self.assertEqual(self.settings.boss_hp, expected_hp)

    def test_create_boss_rush_bullets_below_10(self):
        """Test the create_boss_rush_bullets in the levels below 10."""
        bullets_manager = MagicMock()

        self.game.stats.level = 5

        self.gameplay_handler._create_boss_rush_bullets(bullets_manager)

        bullets_manager.assert_called_once_with(1, 450, 400)

    def test_create_boss_rush_bullets_above_10(self):
        """Test the create_boss_rush_bullets in the levels above 10."""
        bullets_manager = MagicMock()

        self.game.stats.level = 12

        self.gameplay_handler._create_boss_rush_bullets(bullets_manager)

        bullets_manager.assert_called_once_with(1, 200, 350)

    def test_set_max_alien_bullets(self):
        """Test the set_max_alien_bullets method."""
        self._set_max_alien_bullets_helper(0.4, 9)
        self._set_max_alien_bullets_helper(0.6, 10)

    def _set_max_alien_bullets_helper(self, difficulty, expected_max_bullets):
        """Helper function used to test for different difficulties."""
        self.settings.speedup_scale = difficulty

        self.gameplay_handler.set_max_alien_bullets(self.settings.speedup_scale)

        self.assertEqual(self.settings.max_alien_bullets, expected_max_bullets)

    def test_check_alien_bullets_num(self):
        """Test the check_alien_bullets_num method."""
        self.game.stats.level = 3
        self.settings.alien_bullets_num = 5
        self._check_alien_bullets_num_helper(10)
        self._check_alien_bullets_num_helper(6)

    def _check_alien_bullets_num_helper(self, bullets_num):
        """Helper method to check with different values for the max_alien_bullets"""
        self.settings.max_alien_bullets = bullets_num

        self.gameplay_handler.check_alien_bullets_num()

        self.assertEqual(self.settings.alien_bullets_num, 6)

    @patch("pygame.time.get_ticks")
    def test_meteor_madness(self, mock_get_ticks):
        """Test the meteor_madness method."""
        # Case when the time has not yet passed and the level was not increased.
        create_asteroids = MagicMock()
        update_asteroids = MagicMock()
        collision_handler = MagicMock()
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()
        self.gameplay_handler._prepare_asteroids_level = MagicMock()
        mock_get_ticks.return_value = 1000

        self.game.pause_time = 0
        self.gameplay_handler.last_level_time = 0
        self.gameplay_handler.level_time = 1000

        self.gameplay_handler.meteor_madness(
            create_asteroids,
            update_asteroids,
            collision_handler,
            thunderbird_hit,
            phoenix_hit,
        )

        create_asteroids.assert_called_once_with(frequency=self.settings.asteroid_freq)
        update_asteroids.assert_called_once()
        collision_handler.assert_called_once_with(thunderbird_hit, phoenix_hit)
        self.assertEqual(self.gameplay_handler.last_level_time, 0)
        self.gameplay_handler._prepare_asteroids_level.assert_not_called()

        # Case when the time has passed and the level was increased
        create_asteroids.reset_mock()
        update_asteroids.reset_mock()
        collision_handler.reset_mock()
        self.gameplay_handler._prepare_asteroids_level.reset_mock()
        mock_get_ticks.return_value = 2000

        self.gameplay_handler.meteor_madness(
            create_asteroids,
            update_asteroids,
            collision_handler,
            thunderbird_hit,
            phoenix_hit,
        )

        create_asteroids.assert_called_once_with(frequency=self.settings.asteroid_freq)
        update_asteroids.assert_called_once()
        collision_handler.assert_called_once_with(thunderbird_hit, phoenix_hit)
        self.gameplay_handler._prepare_asteroids_level.assert_called_once()
        self.assertEqual(self.gameplay_handler.last_level_time, 2000)

    def test_prepare_asteroids_level(self):
        """Test the prepare_asteroids_level method."""
        self.settings.asteroid_speed = 2.0
        self.settings.asteroid_freq = 500
        self.settings.thunderbird_ship_speed = 4.0
        self.settings.phoenix_ship_speed = 4.0
        self.game.stats.thunderbird_score = 1000

        self.gameplay_handler._prepare_asteroids_level()

        self.assertEqual(self.game.asteroids.empty.call_count, 1)
        self.assertEqual(self.settings.asteroid_speed, 2.3)
        self.assertEqual(self.settings.asteroid_freq, 400)
        self.assertEqual(self.settings.thunderbird_ship_speed, 3.8)
        self.assertEqual(self.settings.phoenix_ship_speed, 3.8)
        self.assertEqual(self.game.stats.thunderbird_score, 3000)
        self.game.score_board.update_high_score.assert_called_once()
        self.game.stats.increase_level.assert_called_once()
        self.game.score_board.prep_level.assert_called_once()
        self.game.score_board.render_high_score.assert_called_once()

    def test_last_bullet_all_ships_alive(self):
        """Test the last_bullet method when the both ships remain alive."""
        asteroid_handler = MagicMock()
        self.thunderbird_ship.remaining_bullets = 9
        self.phoenix_ship.remaining_bullets = 9
        self.thunderbird_ship.state.alive = True
        self.phoenix_ship.state.alive = True
        self.game.stats.game_active = True

        self.gameplay_handler.last_bullet(
            self.thunderbird_ship, self.phoenix_ship, asteroid_handler
        )

        asteroid_handler.assert_called_once_with(create_at_high_levels=True)
        self.assertEqual(self.thunderbird_ship.state.alive, True)
        self.assertEqual(self.phoenix_ship.state.alive, True)
        self.assertEqual(self.game.stats.game_active, True)

    def test_last_bullet_ship_no_bullets(self):
        """Test the last_bullet method when one of the ships
        remains with no bullets."""
        asteroid_handler = MagicMock()
        self.thunderbird_ship.remaining_bullets = 0
        self.phoenix_ship.remaining_bullets = 9
        self.thunderbird_ship.state.alive = True
        self.phoenix_ship.state.alive = True
        self.game.stats.game_active = True

        self.game.aliens.sprites = MagicMock(spec=pygame.sprite.Group)
        self.game.aliens.sprites.return_value = [MagicMock(), MagicMock()]
        self.game.thunderbird_bullets.sprites.return_value = []

        mock_bullet = MagicMock(spec=pygame.sprite.Sprite)
        mock_bullet.rect = MagicMock()
        mock_bullet.rect.left = 100
        mock_bullet.rect.right = 50
        mock_bullet.rect.top = 45
        mock_bullet.rect.bottom = 79

        self.game.phoenix_bullets.sprites.return_value = [mock_bullet]

        self.gameplay_handler.last_bullet(
            self.thunderbird_ship, self.phoenix_ship, asteroid_handler
        )

        asteroid_handler.assert_called_once_with(create_at_high_levels=True)
        self.assertEqual(self.thunderbird_ship.state.alive, False)
        self.assertEqual(self.phoenix_ship.state.alive, True)
        self.assertEqual(self.game.stats.game_active, True)

    def test_last_bullet_no_ships_alive(self):
        """Test the last_bullet method when both ships have
        the alive state set to False."""
        asteroid_handler = MagicMock()
        self.thunderbird_ship.remaining_bullets = 9
        self.phoenix_ship.remaining_bullets = 9
        self.thunderbird_ship.state.alive = False
        self.phoenix_ship.state.alive = False
        self.game.stats.game_active = True

        self.gameplay_handler.last_bullet(
            self.thunderbird_ship, self.phoenix_ship, asteroid_handler
        )

        asteroid_handler.assert_called_once_with(create_at_high_levels=True)
        self.assertEqual(self.thunderbird_ship.state.alive, False)
        self.assertEqual(self.phoenix_ship.state.alive, False)
        self.assertEqual(self.game.stats.game_active, False)

    def test_check_remaining_bullets(self):
        """Test the check_remaining_bullets method."""
        self.game.stats.thunderbird_hp = -1
        self.game.stats.phoenix_hp = -1

        self.gameplay_handler.check_remaining_bullets()

        self.assertEqual(self.game.thunderbird_ship.remaining_bullets, 0)
        self.assertEqual(self.game.phoenix_ship.remaining_bullets, 0)
        self.game.score_board.render_bullets_num.assert_called_once()

    def test_boss_rush(self):
        """Test the boss_rush method."""
        asteroid_handler = MagicMock()
        bullets_manager = MagicMock()
        self.gameplay_handler._create_boss_rush_bullets = MagicMock()

        self.gameplay_handler.boss_rush(asteroid_handler, bullets_manager)

        asteroid_handler.assert_called_once_with(force_creation=True)
        self.gameplay_handler._create_boss_rush_bullets.assert_called_once_with(
            bullets_manager
        )

    @patch("time.time")
    def test_endless_onslaught(self, mock_time):
        """Test the endless_onslaught method."""
        # Case when the time has passed and the alien stats got increased.
        aliens_manager = MagicMock()
        asteroid_handler = MagicMock()
        mock_time.return_value = 100

        self.game.aliens = [MagicMock() for _ in range(51)]
        self.gameplay_handler.settings.alien_speed = 1.0
        self.gameplay_handler.settings.alien_bullet_speed = 2.0
        self.gameplay_handler.last_increase_time = 0
        self.gameplay_handler.endless_onslaught(aliens_manager, asteroid_handler)

        aliens_manager.assert_not_called()
        asteroid_handler.assert_called_once_with(force_creation=True)
        self.assertEqual(self.gameplay_handler.settings.alien_speed, 1.1)
        self.assertEqual(self.gameplay_handler.settings.alien_bullet_speed, 2.1)
        self.assertEqual(self.gameplay_handler.last_increase_time, 100)

        # Case when the time has not passed and the alien stats remain the same.
        aliens_manager.reset_mock()
        asteroid_handler.reset_mock()
        self.game.aliens = [MagicMock(), MagicMock()]
        self.gameplay_handler.settings.alien_speed = 1.0
        self.gameplay_handler.settings.alien_bullet_speed = 2.0
        self.gameplay_handler.last_increase_time = 100
        self.gameplay_handler.endless_onslaught(aliens_manager, asteroid_handler)

        aliens_manager.assert_called_once_with(self.settings.fleet_rows)
        asteroid_handler.assert_called_once_with(force_creation=True)
        self.assertEqual(self.gameplay_handler.settings.alien_speed, 1.0)
        self.assertEqual(self.gameplay_handler.settings.alien_bullet_speed, 2.0)
        self.assertEqual(self.gameplay_handler.last_increase_time, 100)

    @patch("time.time")
    def test_slow_burn(self, mock_time):
        """Test the slow_burn method."""
        asteroid_handler = MagicMock()
        mock_time.return_value = 100
        self.gameplay_handler.last_decrease_time = 0

        self.gameplay_handler.slow_burn(asteroid_handler)

        asteroid_handler.assert_called_once_with(force_creation=True)
        self.assertEqual(self.gameplay_handler.settings.thunderbird_ship_speed, 3.3)
        self.assertEqual(self.gameplay_handler.settings.phoenix_ship_speed, 3.3)
        self.assertEqual(self.gameplay_handler.settings.thunderbird_bullet_speed, 4.8)
        self.assertEqual(self.gameplay_handler.settings.phoenix_bullet_speed, 4.8)
        self.assertEqual(self.gameplay_handler.last_decrease_time, 100)

    def test_cosmic_conflict(self):
        """Test the cosmic_conflict method."""
        bullet_collisions = MagicMock()
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()

        self.gameplay_handler.cosmic_conflict(
            bullet_collisions, thunderbird_hit, phoenix_hit
        )

        bullet_collisions.assert_called_once_with(thunderbird_hit, phoenix_hit)

    def test_set_cosmic_conflict_high_score(self):
        """Test the set_cosmic_conflict_high_score method."""
        self.game.phoenix_ship.state.alive = False
        self.game.stats.thunderbird_score = 1000

        self.gameplay_handler.set_cosmic_conflict_high_score()

        self.assertEqual(self.game.stats.high_score, 1000)

        self.game.phoenix_ship.state.alive = True
        self.game.thunderbird_ship.state.alive = False
        self.game.stats.phoenix_score = 2000

        self.gameplay_handler.set_cosmic_conflict_high_score()

        self.assertEqual(self.game.stats.high_score, 2000)

    def test_reset_cosmic_conflict(self):
        """Test the reset_cosmic_conflict method."""
        self.settings.game_modes.cosmic_conflict = True
        self.settings.game_modes.game_mode = "cosmic_conflict"

        self.gameplay_handler.reset_cosmic_conflict()

        self.assertFalse(self.settings.game_modes.cosmic_conflict)
        self.assertEqual(self.settings.game_modes.game_mode, "normal")


if __name__ == "__main__":
    unittest.main()
