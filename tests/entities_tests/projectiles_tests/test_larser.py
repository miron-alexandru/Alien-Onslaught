"""
This module tests the Laser module which is used to create
the laser weapon in the game.
"""

import unittest
from unittest.mock import MagicMock

from src.entities.projectiles.laser import Laser


class TestLaser(unittest.TestCase):
    """Test cases for the Laser class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.ship = MagicMock()
        self.ship.rect.midtop = (100, 100)
        self.game.settings.game_modes.cosmic_conflict = False
        self.laser = Laser(self.game, self.ship)

    def test_update_frame_counter(self):
        """Test if the update method increments the frame_counter."""
        initial_frame_counter = self.laser.frame_counter

        self.laser.update()

        self.assertEqual(self.laser.frame_counter, initial_frame_counter + 1)

    def test_update_current_frame(self):
        """Test if the update method updates the current_frame."""
        initial_current_frame = self.laser.current_frame
        self.laser.frame_counter = self.laser.frame_update_rate - 1
        expected_current_frame = (initial_current_frame + 1) % len(self.laser.frames)

        self.laser.update()

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
        initial_blit_calls = self.game.screen.blit.call_count

        self.laser.draw()

        self.assertEqual(self.game.screen.blit.call_count, initial_blit_calls + 1)

    def test_set_laser_frames(self):
        """Test the set_laser_frames method."""
        self.game.settings.game_modes.cosmic_conflict = False
        initial_image = self.laser.image

        self.laser.set_laser_frames()

        self.assertEqual(self.laser.image, initial_image)


if __name__ == "__main__":
    unittest.main()
