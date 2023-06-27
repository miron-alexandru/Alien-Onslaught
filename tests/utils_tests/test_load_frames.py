"""This module tests the load_frames function."""

import os
import unittest
import pygame

from src.utils.game_utils import load_frames, BASE_PATH


class LoadFramesTests(unittest.TestCase):
    """Test case for the load_frames function
    which is used to load the frames constants.
    """

    def setUp(self):
        self.image = pygame.Surface((54, 32))

    def test_load_frames(self):
        """Test for the load_frames function."""
        filename_pattern = "frame_{}.png"
        num_frames = 3
        start = 0

        # Create sample image files for testing
        for i in range(start, start + num_frames):
            filename = filename_pattern.format(i)
            pygame.image.save(self.image, os.path.join(BASE_PATH, filename))

        frames = load_frames(filename_pattern, num_frames, start)

        self.assertEqual(len(frames), num_frames)
        self.assertIsInstance(frames[0], pygame.Surface)

        for i in range(start, start + num_frames):
            filename = filename_pattern.format(i)
            os.remove(os.path.join(BASE_PATH, filename))


if __name__ == "__main__":
    unittest.main()
