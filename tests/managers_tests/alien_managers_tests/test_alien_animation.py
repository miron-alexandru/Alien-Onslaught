"""
This module tests the AlienAnimation class which is used for
alien animation in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.managers.alien_managers.aliens_behaviors import AlienAnimation


class AlienAnimationTestCase(unittest.TestCase):
    """Test cases for the AlienAnimation class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.alien = MagicMock()
        self.animation = AlienAnimation(self.game, self.alien)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.animation.alien, self.alien)
        self.assertEqual(self.animation.game, self.game)
        self.assertEqual(self.animation.scale, 1.0)
        self.assertEqual(self.animation.frame_update_rate, 6)
        self.assertEqual(self.animation.frame_counter, 0)
        self.assertEqual(self.animation.current_frame, 0)
        self.assertIsInstance(self.animation.frames, list)
        self.assertIsInstance(self.animation.image, pygame.Surface)

    def test_update_animation(self):
        """Test the update_animation method."""
        self.animation.frame_counter = 5
        initial_frame = self.animation.current_frame

        self.animation.update_animation()

        self.assertEqual(
            self.animation.current_frame,
            (initial_frame + 1) % len(self.animation.frames),
        )
        self.assertEqual(self.animation.frame_counter, 0)

    def test_change_scale(self):
        """Test the change_scale method."""
        initial_image = self.animation.image
        initial_frames = self.animation.frames
        scale = 3

        self.animation.change_scale(scale)

        self.assertNotEqual(self.animation.image, initial_image)
        self.assertNotEqual(self.animation.frames, initial_frames)
        self.assertEqual(self.animation.scale, scale)

    @patch("pygame.transform.scale")
    def test_update_scale(self, mock_scale):
        """Test the update scale method."""
        scale = 2.0
        self.animation.scale = scale

        # Call the _update_scale() method
        self.animation._update_scale()

        # Verify that the image and frames have been scaled
        self.assertEqual(mock_scale.call_count, len(self.animation.frames) + 1)

    def test_get_current_image(self):
        """Test the get_current_image method."""
        current_image = self.animation.get_current_image()
        self.assertEqual(current_image, self.animation.image)


if __name__ == "__main__":
    unittest.main()
