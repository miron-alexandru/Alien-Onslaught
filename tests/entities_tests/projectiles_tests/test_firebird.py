"""
This module tests the Firebird class which is used to create
bullets for the Phoenix player.
"""

from unittest.mock import MagicMock
import unittest

import pygame

from src.entities.projectiles.player_bullets import Firebird
from src.managers.player_managers.weapons_manager import WeaponsManager


class TestFirebird(unittest.TestCase):
    """Test cases for the Firebird class."""

    def setUp(self):
        self.game = MagicMock()
        self.manager = WeaponsManager(self.game)
        self.ship = MagicMock()
        self.firebird = Firebird(self.manager, self.ship)

    def test_init(self):
        """Test the initialization of the Firebird."""
        self.assertIsInstance(self.firebird, Firebird)
        self.assertEqual(self.firebird.ship, self.ship)
        self.assertIsNotNone(self.firebird.image)
        self.assertIsNotNone(self.firebird.rect)
        self.assertEqual(
            self.firebird.speed, self.manager.settings.phoenix_bullet_speed
        )

    def test_init_rotation(self):
        """Test the initialization of the Firebird with rotation."""
        self.manager.settings.game_modes.cosmic_conflict = True
        firebird = Firebird(self.manager, self.ship)
        expected_width, expected_height = firebird.image.get_size()
        rotated_image = pygame.transform.rotate(firebird.image, 90)
        actual_width, actual_height = rotated_image.get_size()

        # Assertions
        self.assertIsNotNone(firebird.image)
        self.assertIsNotNone(firebird.rect)
        self.assertEqual(firebird.speed, self.manager.settings.phoenix_bullet_speed)
        self.assertEqual(
            (actual_width, actual_height), (expected_height, expected_width)
        )

    def test_init_scaled(self):
        """Test the initialization of the scaled Firebird."""
        scaled_firebird = Firebird(self.manager, self.ship, scaled=True)

        self.assertIsNotNone(scaled_firebird.image)
        self.assertIsNotNone(scaled_firebird.rect)
        self.assertEqual(
            scaled_firebird.speed, self.manager.settings.phoenix_bullet_speed
        )
        self.assertNotEqual(scaled_firebird.image, self.firebird.image)
        self.assertEqual(
            scaled_firebird.image.get_size(),
            (
                int(self.firebird.image.get_width() * 0.5),
                int(self.firebird.image.get_height() * 0.5),
            ),
        )


if __name__ == "__main__":
    unittest.main()
