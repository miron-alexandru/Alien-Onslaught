"""
This module tests the MissileEx class that manages the missile
explosion animation in the game.
"""

import copy
import unittest
from unittest.mock import Mock

import pygame

from src.animations.entities_animations import MissileEx
from src.utils.animation_constants import missile_ex_frames


class MissileExTests(unittest.TestCase):
    """Test cases for the MissileEx class."""

    def setUp(self):
        """Set up the test environment."""
        self.missile = pygame.sprite.Sprite()
        self.missile.rect = pygame.Rect(0, 0, 50, 50)  # type: ignore
        self.missile.screen = pygame.Surface((800, 600))  # type: ignore

    def test_init(self):
        """Test the initialization of MissileEx."""
        missile_ex = MissileEx(self.missile)

        self.assertEqual(missile_ex.missile, self.missile)
        self.assertEqual(missile_ex.screen, self.missile.screen)  # type: ignore
        self.assertEqual(missile_ex.ex_frames, missile_ex_frames)
        self.assertEqual(missile_ex.current_frame, 0)
        self.assertEqual(missile_ex.ex_image, missile_ex_frames[0])
        self.assertEqual(missile_ex.frame_update_rate, 5)
        self.assertEqual(missile_ex.frame_counter, 0)

    def test_update_animation(self):
        """Test the update of the explosion animation frames."""
        missile_ex = MissileEx(self.missile)
        missile_ex.current_frame = 0
        initial_frame = copy.copy(missile_ex.ex_image)

        missile_ex.update_animation()

        self.assertEqual(missile_ex.current_frame, 0)
        self.assertNotEqual(missile_ex.ex_image, initial_frame)
        self.assertEqual(missile_ex.ex_rect.center, self.missile.rect.center)  # type: ignore

        missile_ex.current_frame = len(missile_ex_frames) - 1

        missile_ex.update_animation()

        self.assertEqual(missile_ex.current_frame, len(missile_ex_frames) - 1)
        self.assertNotEqual(missile_ex.ex_image, initial_frame)
        self.assertEqual(missile_ex.ex_rect.center, self.missile.rect.center)  # type: ignore

    def test_draw_explosion(self):
        """Test the drawing of the explosion animation on the screen."""
        missile_ex = MissileEx(self.missile)
        missile_ex.screen = Mock()

        missile_ex.draw_explosion()

        missile_ex.screen.blit.assert_called_once_with(
            missile_ex.ex_image, missile_ex.ex_rect
        )


if __name__ == "__main__":
    unittest.main()
