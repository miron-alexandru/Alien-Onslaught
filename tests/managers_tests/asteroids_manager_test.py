"""
This module tests the AsteroidsManagers which is used
to handle the asteroids in the game.
"""


import unittest
from unittest.mock import MagicMock

from src.entities.asteroid import Asteroid
from src.game_logic.game_settings import Settings
from src.managers.asteroids_manager import AsteroidsManager


class TestAsteroidsManager(unittest.TestCase):
    """Test cases for the AsteroidsManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.settings = Settings()  # Use the actual Settings object
        self.stats = MagicMock()
        self.stats.level = 1
        self.game.asteroids = set()
        self.collision_handler = MagicMock()
        self.ships_manager = MagicMock()
        self.asteroids_manager = AsteroidsManager(self.game)

    def test_create_asteroids(self):
        """Test the creation of the asteroids."""
        self.asteroids_manager.create_asteroids(frequency=0)
        self.assertEqual(
            len(self.game.asteroids), 1
        )  # Check if an asteroid was created

    def test_update_asteroids(self):
        """Test the update of the asteroid."""
        asteroid = Asteroid(self.game)
        asteroid.rect.y = 500
        self.asteroids_manager.update_asteroids()
        self.assertEqual(len(self.game.asteroids), 0)

    def test_handle_asteroids(self):
        """Test the handling of asteroids."""
        self.game.stats.level = 5  # Lower than level 7
        self.asteroids_manager.create_asteroids = MagicMock()
        self.asteroids_manager.handle_asteroids()
        self.assertFalse(self.asteroids_manager.create_asteroids.called)

        self.game.stats.level = 7  # Level 7 or above
        self.asteroids_manager.create_asteroids = MagicMock()
        self.asteroids_manager.handle_asteroids()
        self.assertTrue(self.asteroids_manager.create_asteroids.called)

        self.game.stats.level = 5  # Lower than level 7
        self.asteroids_manager.create_asteroids = MagicMock()
        self.asteroids_manager.handle_asteroids(force_creation=True)
        self.assertTrue(self.asteroids_manager.create_asteroids.called)

    def test_handle_asteroids_collision(self):
        """Test if the collision for asteroids is checked."""
        self.game.stats.level = 7
        asteroid = MagicMock()
        self.game.asteroids = MagicMock(return_value=[asteroid])
        self.game.collision_handler = MagicMock()
        self.game.ships_manager.thunderbird_ship_hit = MagicMock()
        self.game.ships_manager.phoenix_ship_hit = MagicMock()
        self.asteroids_manager.handle_asteroids()

        self.assertTrue(self.game.collision_handler.check_asteroids_collisions.called)
        self.game.collision_handler.check_asteroids_collisions.assert_called_once_with(
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )


if __name__ == "__main__":
    unittest.main()
