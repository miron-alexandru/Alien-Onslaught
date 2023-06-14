"""
This module tests the Asteroid class that manages the asteroids
in the game.
"""

import unittest
from unittest.mock import MagicMock

from src.entities.asteroid import Asteroid
from src.game_logic.game_settings import Settings

class TestAsteroid(unittest.TestCase):
    """Test cases for the Asteroid class"""
    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.screen = MagicMock()
        self.game.screen = self.screen
        self.settings = Settings()
        self.game.settings = self.settings
        self.asteroid = Asteroid(self.game)

    def test_initialize_position(self):
        """Test the position initialization of the asteroid."""
        self.asteroid._initialize_position()
        self.assertTrue(0 <= self.asteroid.rect.x <= self.settings.screen_width - self.asteroid.rect.width)
        self.assertEqual(self.asteroid.rect.y, 0)

    def test_update(self):
        """Test the update of the asteroid."""
        initial_frame = self.asteroid.current_frame
        self.asteroid.update()
        self.assertEqual(self.asteroid.current_frame, (initial_frame + 1) % len(self.asteroid.frames))
        self.assertEqual(self.asteroid.image, self.asteroid.frames[self.asteroid.current_frame])
        self.assertEqual(self.asteroid.y_pos, 0 + self.asteroid.speed)
        self.assertEqual(int(self.asteroid.rect.y), int(self.asteroid.y_pos))

    def test_draw(self):
        """Test the drawing of the asteroid."""
        self.asteroid.draw()
        self.screen.blit.assert_called_once_with(self.asteroid.image, self.asteroid.rect)

if __name__ == '__main__':
    unittest.main()
