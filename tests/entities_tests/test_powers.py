"""
This module tests the Power class that is used to create power ups
and penalties in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.entities.powers import Power


class TestPower(unittest.TestCase):
    """Test cases for Power class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.power = Power(self.game)

    def test_init(self):
        """Test the initialization of the Power."""
        self.assertIsInstance(self.power.image, pygame.Surface)
        self.assertIsInstance(self.power.health_image, pygame.Surface)
        self.assertIsInstance(self.power.speed, float)
        self.assertEqual(self.power.last_power_time, 0)
        self.assertIsInstance(self.power.rect, pygame.Rect)
        self.assertGreaterEqual(self.power.rect.x, 0)
        self.assertEqual(self.power.rect.y, 0)
        self.assertFalse(self.power.health)
        self.assertFalse(self.power.weapon)
        self.assertIsNone(self.power.weapon_name)

    def test_initialize_position(self):
        """Test the initialize_position method."""
        self.game.settings.screen_width = 700
        self.power._initialize_position()

        self.assertTrue(
            0
            <= self.power.rect.x
            <= self.game.settings.screen_width - self.power.rect.width
        )
        self.assertEqual(self.power.rect.y, 0)
        self.assertEqual(self.power.y_pos, float(self.power.rect.y))

    def test_make_health_power_up(self):
        """Test the creation of a health power up."""
        self.power.make_health_power_up()

        self.assertTrue(self.power.health)
        self.assertEqual(self.power.image, self.power.health_image)

    def test_make_weapon_power_up(self):
        """Test the creation of a weapon power up."""
        self.power.make_weapon_power_up()

        self.assertTrue(self.power.weapon)
        self.assertIsNotNone(self.power.weapon_name)
        self.assertIsInstance(self.power.image, pygame.Surface)

    def test_update(self):
        """Test the update of the Power."""
        initial_y_pos = self.power.y_pos

        self.power.update()

        self.assertEqual(self.power.y_pos, initial_y_pos + self.power.speed)
        self.assertEqual(int(self.power.rect.y), int(self.power.y_pos))

    def test_draw(self):
        """Test the drawing of the power."""
        self.power.draw()

        self.game.screen.blit.assert_called_once_with(self.power.image, self.power.rect)


if __name__ == "__main__":
    unittest.main()
