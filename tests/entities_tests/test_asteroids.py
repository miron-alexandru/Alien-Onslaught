"""
This module tests the Asteroid class which is used to create
asteroids in the game.
"""

import unittest
from unittest.mock import MagicMock

from src.entities.asteroid import Asteroid


class TestAsteroid(unittest.TestCase):
    """Test cases for the Asteroid class."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.game.settings.asteroid_speed = 3
        self.asteroid = Asteroid(self.game)

    def test_init(self):
        """Test the initialization of the Asteroid."""
        self.assertEqual(self.asteroid.speed, self.game.settings.asteroid_speed)
        self.assertIsNotNone(self.asteroid.frames)
        self.assertEqual(self.asteroid.current_frame, 0)
        initial_image = self.asteroid.frames[0]
        self.assertEqual(self.asteroid.image, initial_image)

    def test_initialize_position(self):
        """Test the _initialize_position method."""
        self.game.settings.screen_width = 700
        self.asteroid._initialize_position()

        self.assertGreaterEqual(self.asteroid.rect.x, 0)
        self.assertLessEqual(
            self.asteroid.rect.x,
            self.game.settings.screen_width - self.asteroid.rect.width,
        )
        self.assertEqual(self.asteroid.rect.y, 0)

    def test_update(self):
        """Test the update method."""
        initial_frame = self.asteroid.current_frame
        initial_y_pos = self.asteroid.y_pos

        self.asteroid.update()

        # Verify frame update
        self.assertEqual(
            self.asteroid.current_frame, (initial_frame + 1) % len(self.asteroid.frames)
        )
        self.assertEqual(
            self.asteroid.image, self.asteroid.frames[self.asteroid.current_frame]
        )

        # Verify position update
        self.assertEqual(
            self.asteroid.y_pos,
            initial_y_pos + self.asteroid.speed,
        )
        self.assertEqual(
            self.asteroid.rect.y,
            self.asteroid.y_pos,
        )

    def test_draw(self):
        """Test the draw method."""
        self.asteroid.draw()

        self.game.screen.blit.assert_called_once_with(
            self.asteroid.image, self.asteroid.rect
        )


if __name__ == "__main__":
    unittest.main()
