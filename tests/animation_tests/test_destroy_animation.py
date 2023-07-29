"""
This module tests the DestroyAnim that is used to display
the destroy animation on entities in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.animations.entities_animations import DestroyAnim
from src.utils.animation_constants import destroy_frames


class DestroyAnimTests(unittest.TestCase):
    """Test cases for the DestroyAnim class."""

    def setUp(self):
        """Set up the test environment."""
        self.entity = pygame.sprite.Sprite()
        self.entity.rect = pygame.Rect(0, 0, 100, 100)  # type: ignore
        self.entity.screen = pygame.Surface((800, 600))  # type: ignore

    def test_init(self):
        """Test the initialization of DestroyAnim."""
        destroy_anim = DestroyAnim(self.entity)

        self.assertEqual(destroy_anim.entity, self.entity)
        self.assertIsNone(destroy_anim.image)
        self.assertEqual(destroy_anim.screen, self.entity.screen)  # type: ignore
        self.assertEqual(destroy_anim.destroy_frames, destroy_frames)
        self.assertEqual(destroy_anim.current_destroy_frame, 0)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[0])

    def test_update_destroy_animation(self):
        """Test the update of the destroy animation frames."""
        destroy_anim = DestroyAnim(self.entity)
        destroy_anim.current_destroy_frame = 0

        destroy_anim.update_destroy_animation()

        self.assertEqual(destroy_anim.current_destroy_frame, 1)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[1])
        self.assertEqual(destroy_anim.destroy_rect.center, self.entity.rect.center)  # type: ignore

        # Test wrapping around to the first frame
        destroy_anim.current_destroy_frame = len(destroy_frames) - 1

        destroy_anim.update_destroy_animation()

        self.assertEqual(destroy_anim.current_destroy_frame, 0)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[0])
        self.assertEqual(destroy_anim.destroy_rect.center, self.entity.rect.center)  # type: ignore

    def test_draw_animation(self):
        """Test the drawing of the destroy animation on the screen."""
        destroy_anim = DestroyAnim(self.entity)

        destroy_anim.screen = MagicMock()

        destroy_anim.draw_animation()

        destroy_anim.screen.blit.assert_called_once_with(
            destroy_anim.destroy_image, destroy_anim.destroy_rect
        )


if __name__ == "__main__":
    unittest.main()
