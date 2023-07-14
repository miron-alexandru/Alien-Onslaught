"""
This module tests the Thunderbolt class which is used to create
bullets for the Thunderbird player.
"""

from unittest.mock import MagicMock
import unittest

import pygame

from src.entities.projectiles.player_bullets import Thunderbolt
from src.managers.player_managers.weapons_manager import WeaponsManager


class TestThunderbolt(unittest.TestCase):
    """Test cases for the Thunderbolt class."""

    def setUp(self):
        self.game = MagicMock()
        self.manager = WeaponsManager(self.game)
        self.ship = MagicMock()
        self.thunderbolt = Thunderbolt(self.manager, self.ship)

    def test_init(self):
        """Test the initialization of the Thunderbolt."""
        self.assertIsInstance(self.thunderbolt, Thunderbolt)
        self.assertEqual(self.thunderbolt.ship, self.ship)
        self.assertIsNotNone(self.thunderbolt.image)
        self.assertIsNotNone(self.thunderbolt.rect)
        self.assertEqual(
            self.thunderbolt.speed, self.manager.settings.thunderbird_bullet_speed
        )

    def test_init_rotation(self):
        """Test the initialization of the Thunderbolt with rotation."""
        self.manager.settings.game_modes.cosmic_conflict = True
        thunderbolt = Thunderbolt(self.manager, self.ship)
        expected_width, expected_height = thunderbolt.image.get_size()
        rotated_image = pygame.transform.rotate(thunderbolt.image, -90)
        actual_width, actual_height = rotated_image.get_size()

        self.assertIsNotNone(thunderbolt.image)
        self.assertIsNotNone(thunderbolt.rect)
        self.assertEqual(
            thunderbolt.speed, self.manager.settings.thunderbird_bullet_speed
        )
        self.assertEqual(
            (actual_width, actual_height), (expected_height, expected_width)
        )

    def test_init_scaled(self):
        """Test the initialization of the scaled Thunderbolt."""
        scaled_thunderbolt = Thunderbolt(self.manager, self.ship, scaled=True)

        self.assertIsNotNone(scaled_thunderbolt.image)
        self.assertIsNotNone(scaled_thunderbolt.rect)
        self.assertEqual(
            scaled_thunderbolt.speed, self.manager.settings.thunderbird_bullet_speed
        )
        self.assertNotEqual(scaled_thunderbolt.image, self.thunderbolt.image)
        self.assertEqual(
            scaled_thunderbolt.image.get_size(),
            (
                int(self.thunderbolt.image.get_width() * 0.5),
                int(self.thunderbolt.image.get_height() * 0.5),
            ),
        )


if __name__ == "__main__":
    unittest.main()
