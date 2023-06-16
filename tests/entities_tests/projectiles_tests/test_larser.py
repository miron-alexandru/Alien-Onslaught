"""
This module tests the Laser module which is used to create
the laser weapon in the game.
"""


import unittest
from unittest.mock import MagicMock

import pygame
from src.entities.projectiles import Laser
from src.game_logic.game_settings import Settings


class TestLaser(unittest.TestCase):
    """Test cases for the Laser class."""

    def setUp(self):
        """Set up test environment."""
        self.screen = MagicMock(spec=pygame.Surface)
        self.settings = Settings()
        self.game = MagicMock()
        self.game.screen = self.screen
        self.game.settings = self.settings
        self.ship = MagicMock()
        self.ship.rect = MagicMock()
        self.ship.rect.midbottom = (100, 200)
        self.ship.rect.midtop = (100, 100)
        self.laser = Laser(self.game, self.ship)

    def test_update_frame_counter(self):
        """Test the update method increments the frame_counter."""
        initial_frame_counter = self.laser.frame_counter
        self.laser.update()
        self.assertEqual(self.laser.frame_counter, initial_frame_counter + 1)

    def test_update_current_frame(self):
        """Test the update method updates the current_frame."""
        initial_current_frame = self.laser.current_frame
        self.laser.frame_counter = self.laser.frame_update_rate - 1

        self.laser.update()

        expected_current_frame = (initial_current_frame + 1) % len(self.laser.frames)
        self.assertEqual(self.laser.current_frame, expected_current_frame)

    def test_update_laser_kill(self):
        """Test the update method kills the laser when the duration
        is exceeded or the ship is exploding.
        """
        self.laser.duration = 0
        self.laser.ship.state.exploding = True
        self.laser.update()
        self.assertFalse(self.laser.alive())

    def test_draw(self):
        """Test the draw method."""
        initial_blit_calls = self.screen.blit.call_count
        self.laser.draw()
        self.assertEqual(self.screen.blit.call_count, initial_blit_calls + 1)

    def test_set_laser_frames(self):
        """Test the set_laser_frames method."""
        initial_image = self.laser.image
        self.laser.set_laser_frames()
        self.assertEqual(self.laser.image, initial_image)


if __name__ == "__main__":
    unittest.main()