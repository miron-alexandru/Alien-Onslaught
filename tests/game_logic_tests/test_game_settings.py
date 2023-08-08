"""
This module tests the Settings class which is used to store the 
settings for the game.
"""

import unittest
import pygame

from src.game_logic.game_settings import Settings
from src.utils.game_dataclasses import UIOptions, GameModes


class SettingsTestCase(unittest.TestCase):
    """Test cases for the Settings class."""

    def setUp(self):
        """Set up test environment."""
        self.settings = Settings()

    def test_init_screen_settings(self):
        """Test the initialization of the screen settings."""
        self.assertEqual(self.settings.screen_width, 1260)
        self.assertEqual(self.settings.screen_height, 700)

    def test_init_images(self):
        """Test the initialization of the images."""
        # Test loading of images
        self.assertIsInstance(self.settings.bg_images, dict)
        self.assertIsInstance(self.settings.misc_images, dict)

        # Assertions for specific image attributes
        self.assertIn("space", self.settings.bg_images.keys())
        self.assertIn("space2", self.settings.bg_images.keys())
        self.assertIn("space3", self.settings.bg_images.keys())
        self.assertIn("space4", self.settings.bg_images.keys())

        self.assertIn("gameover", self.settings.misc_images.keys())
        self.assertIn("pause", self.settings.misc_images.keys())
        self.assertIn("game_title", self.settings.misc_images.keys())
        self.assertIn("cursor", self.settings.misc_images.keys())
        self.assertIn("game_icon", self.settings.misc_images.keys())

        self.assertEqual(self.settings.game_title_rect.y, -270)
        self.assertIsInstance(self.settings.game_end_rect, pygame.Rect)
        self.assertIsInstance(self.settings.game_title_rect, pygame.Rect)
        self.assertIsInstance(self.settings.cursor_rect, pygame.Rect)

    def test_init_game_settings(self):
        """Test the initialization of the different game settings."""
        # Test initialization of game modes and UI options
        self.assertIsInstance(self.settings.game_modes, GameModes)
        self.assertIsInstance(self.settings.ui_options, UIOptions)

        # Test initialization of other game-related settings
        self.assertEqual(self.settings.speedup_scale, 0.2)
        self.assertEqual(self.settings.missiles_speed, 5.0)
        self.assertEqual(self.settings.immune_time, 5000)
        self.assertEqual(self.settings.scaled_time, 60)
        self.assertEqual(self.settings.laser_cooldown, 90)
        self.assertEqual(self.settings.required_kill_count, 45)
        self.assertEqual(self.settings.alien_immune_time, 30)
        self.assertEqual(self.settings.frozen_time, 4)
        self.assertEqual(self.settings.max_alien_speed, 3.8)

    def test_regular_thunder_ship(self):
        """Test settings for the regular Thunderbird ship."""
        self.settings.regular_thunder_ship()
        self.assertEqual(self.settings.starting_thunder_ship_speed, 3.5)
        self.assertEqual(self.settings.starting_thunder_bullet_speed, 5.0)
        self.assertEqual(self.settings.starting_thunder_bullet_count, 1)
        self.assertEqual(self.settings.starting_thunder_bullets_allowed, 3)
        self.assertEqual(self.settings.starting_thunder_hp, 3)

    def test_slow_thunder(self):
        """Test settings for the slow Thunderbird ship."""
        self.settings.slow_thunder()
        self.assertEqual(self.settings.starting_thunder_ship_speed, 2.2)
        self.assertEqual(self.settings.starting_thunder_bullet_speed, 3.2)
        self.assertEqual(self.settings.starting_thunder_bullet_count, 6)
        self.assertEqual(self.settings.starting_thunder_bullets_allowed, 6)
        self.assertEqual(self.settings.starting_thunder_hp, 5)

    def test_heavy_artillery_thunder(self):
        """Test settings for the heavy artillery Thunderbird ship."""
        self.settings.heavy_artillery_thunder()
        self.assertEqual(self.settings.starting_thunder_ship_speed, 3.0)
        self.assertEqual(self.settings.starting_thunder_bullet_speed, 6.0)
        self.assertEqual(self.settings.starting_thunder_bullet_count, 2)
        self.assertEqual(self.settings.starting_thunder_bullets_allowed, 6)
        self.assertEqual(self.settings.starting_thunder_hp, 1)

    def test_regular_phoenix_ship(self):
        """Test settings for the regular Phoenix ship."""
        self.settings.regular_phoenix_ship()
        self.assertEqual(self.settings.starting_phoenix_ship_speed, 3.5)
        self.assertEqual(self.settings.starting_phoenix_bullet_speed, 5.0)
        self.assertEqual(self.settings.starting_phoenix_bullet_count, 1)
        self.assertEqual(self.settings.starting_phoenix_bullets_allowed, 3)
        self.assertEqual(self.settings.starting_phoenix_hp, 3)

    def test_fast_phoenix(self):
        """Test settings for the fast Phoenix ship."""
        self.settings.fast_phoenix()
        self.assertEqual(self.settings.starting_phoenix_ship_speed, 6.0)
        self.assertEqual(self.settings.starting_phoenix_bullet_speed, 8.5)
        self.assertEqual(self.settings.starting_phoenix_bullet_count, 1)
        self.assertEqual(self.settings.starting_phoenix_bullets_allowed, 3)
        self.assertEqual(self.settings.starting_phoenix_hp, 1)

    def test_heavy_artillery_phoenix(self):
        """Test settings for the heavy artillery Phoenix ship."""
        self.settings.heavy_artillery_phoenix()
        self.assertEqual(self.settings.starting_phoenix_ship_speed, 3.0)
        self.assertEqual(self.settings.starting_phoenix_bullet_speed, 4.5)
        self.assertEqual(self.settings.starting_phoenix_bullet_count, 4)
        self.assertEqual(self.settings.starting_phoenix_bullets_allowed, 8)
        self.assertEqual(self.settings.starting_phoenix_hp, 2)

    def test_dynamic_settings(self):
        """Test the settings of the dynamic settings."""
        self.settings.dynamic_settings()

        # Test Thunderbird settings
        self.assertEqual(self.settings.thunderbird_ship_speed, 3.5)
        self.assertEqual(self.settings.thunderbird_bullet_speed, 5.0)
        self.assertEqual(self.settings.thunderbird_bullets_allowed, 3)
        self.assertEqual(self.settings.thunderbird_bullet_count, 1)
        self.assertEqual(self.settings.thunderbird_missiles_num, 3)

        # Test Phoenix settings
        self.assertEqual(self.settings.phoenix_ship_speed, 3.5)
        self.assertEqual(self.settings.phoenix_bullet_speed, 5.0)
        self.assertEqual(self.settings.phoenix_bullets_allowed, 3)
        self.assertEqual(self.settings.phoenix_bullet_count, 1)
        self.assertEqual(self.settings.phoenix_missiles_num, 3)

        # Test Alien settings
        self.assertEqual(self.settings.alien_speed, 0.8)
        self.assertEqual(self.settings.alien_bullet_speed, 1.5)
        self.assertEqual(self.settings.alien_points, 1)
        self.assertEqual(self.settings.fleet_rows, 2)
        self.assertEqual(self.settings.last_bullet_rows, 2)
        self.assertEqual(self.settings.aliens_num, 8)
        self.assertEqual(self.settings.alien_direction, 1)
        self.assertEqual(self.settings.alien_bullets_num, 2)
        self.assertEqual(self.settings.max_alien_bullets, 8)

        # Test Boss settings
        self.assertEqual(self.settings.boss_hp, 50)
        self.assertEqual(self.settings.boss_points, 2500)

        # Test Asteroid settings
        self.assertEqual(self.settings.asteroid_speed, 1.5)
        self.assertEqual(self.settings.asteroid_freq, 720)

        # Test settings in One Life Reign mode
        self.settings.game_modes.one_life_reign = True
        self.settings.dynamic_settings()
        self.assertEqual(self.settings.thunderbird_ship_speed, 7.0)
        self.assertEqual(self.settings.thunderbird_bullet_speed, 10.0)
        self.assertEqual(self.settings.thunderbird_bullets_allowed, 6)
        self.assertEqual(self.settings.thunderbird_bullet_count, 2)
        self.assertEqual(self.settings.phoenix_ship_speed, 7.0)
        self.assertEqual(self.settings.phoenix_bullet_speed, 10.0)
        self.assertEqual(self.settings.phoenix_bullets_allowed, 6)
        self.assertEqual(self.settings.phoenix_bullet_count, 2)

    def test_increase_speed(self):
        """Test the increase_speed method."""
        self.settings.increase_speed()

        self.assertEqual(self.settings.alien_speed, 1.0)
        self.assertEqual(self.settings.alien_bullet_speed, 1.7)
        self.assertEqual(self.settings.alien_points, 5)

        # Test increasing alien number only when not in last bullet game mode
        self.assertEqual(self.settings.aliens_num, 10)

        # Add more assertions as needed
        self.settings.game_modes.last_bullet = True

        # Test is the aliens_num was not increased in the last bullet game mode
        self.settings.increase_speed()
        self.assertEqual(self.settings.aliens_num, 10)

    def test_disable_ui_flags(self):
        """Test the disable_ui_flags method."""
        self.settings.disable_ui_flags()

        self.assertFalse(self.settings.ui_options.show_difficulty)
        self.assertFalse(self.settings.ui_options.show_game_modes)
        self.assertFalse(self.settings.ui_options.show_high_scores)
        self.assertFalse(self.settings.ui_options.ship_selection)


if __name__ == "__main__":
    unittest.main()
