"""
This module tests the AsteroidsManagers which is used
to handle the asteroids in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.managers.asteroids_manager import AsteroidsManager


class TestAsteroidsManager(unittest.TestCase):
    """Test cases for the AsteroidsManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.game.asteroids = pygame.sprite.Group()
        self.asteroids_manager = AsteroidsManager(self.game)

    def test_create_asteroids(self):
        """Test the creation of the asteroids."""
        self.asteroids_manager.create_asteroids(frequency=0)
        self.asteroids_manager.create_asteroids(frequency=0)
        self.asteroids_manager.create_asteroids(frequency=0)

        self.assertEqual(len(self.game.asteroids), 3)

    def test_update_asteroids(self):
        """Test the update of the asteroid."""
        asteroid = MagicMock()
        asteroid.rect.y = 500
        self.game.settings.screen_height = 400

        # Create a mock group that behaves like pygame.sprite.Group
        asteroids_group = MagicMock()
        asteroids_group.copy.return_value = [asteroid]

        self.game.asteroids = asteroids_group

        self.asteroids_manager.update_asteroids()

        asteroids_group.update.assert_called_once()
        asteroids_group.remove.assert_called_with(asteroid)

    def test_handle_asteroids(self):
        """Test the handling of asteroids."""
        self.game.stats.level = 5  # Lower than level 7
        self.asteroids_manager.create_asteroids = MagicMock()

        self.asteroids_manager.handle_asteroids()

        self.assertFalse(self.asteroids_manager.create_asteroids.called)

        self.game.stats.level = 7  # Level 7 or above

        self.asteroids_manager.handle_asteroids()

        self.assertTrue(self.asteroids_manager.create_asteroids.called)

        self.game.stats.level = 5  # Lower than level 7

        self.asteroids_manager.handle_asteroids(force_creation=True)

        self.assertTrue(self.asteroids_manager.create_asteroids.called)

    def test_handle_asteroids_collision(self):
        """Test if the collision for asteroids is checked."""
        self.game.stats.level = 7

        self.asteroids_manager.handle_asteroids()

        self.assertTrue(self.game.collision_handler.check_asteroids_collisions.called)
        self.game.collision_handler.check_asteroids_collisions.assert_called_once_with(
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )


if __name__ == "__main__":
    unittest.main()
