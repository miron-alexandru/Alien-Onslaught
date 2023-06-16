"""
This module tests the Asteroid class which is used to create
asteroids in the game.
"""


import unittest
from unittest.mock import MagicMock

import pygame

from src.entities.asteroid import Asteroid
from src.game_logic.game_settings import Settings


class TestAsteroid(unittest.TestCase):
    """Test cases for the Asteroid class."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.screen = MagicMock(spec=pygame.Surface)
        self.game.screen = self.screen
        self.settings = Settings()
        self.game.settings = self.settings
        self.asteroid = Asteroid(self.game)

    def test_init(self):
        """Test the initialization of the Asteroid."""
        self.assertEqual(self.asteroid.speed, self.settings.asteroid_speed)
        self.assertIsNotNone(self.asteroid.frames)
        self.assertEqual(self.asteroid.current_frame, 0)
        initial_image = self.asteroid.frames[0]
        self.assertEqual(self.asteroid.image, initial_image)

    def test_initialize_position(self):
        """Test the _initialize_position method."""
        self.asteroid._initialize_position()
        self.assertGreaterEqual(self.asteroid.rect.x, 0)
        self.assertLessEqual(
            self.asteroid.rect.x,
            self.settings.screen_width - self.asteroid.rect.width,
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
        self.assertAlmostEqual(
            self.asteroid.y_pos,
            initial_y_pos + self.asteroid.speed,
            delta=self.asteroid.speed * 0.1,
        )
        self.assertAlmostEqual(
            int(self.asteroid.rect.y),
            int(self.asteroid.y_pos),
        )

    def test_draw(self):
        """Test the draw method."""
        self.asteroid.draw()
        self.screen.blit.assert_called_once_with(
            self.asteroid.image, self.asteroid.rect
        )


if __name__ == "__main__":
    unittest.main()
