"""
This module tests the Immune class that is used to display the
alien immune animation in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.animations.entities_animations import Immune
from src.utils.animation_constants import alien_immune_frames


class ImmuneTests(unittest.TestCase):
    """Test cases for the Immune class."""

    def setUp(self):
        """Set up the test environment."""
        self.alien = pygame.sprite.Sprite()
        self.alien.rect = pygame.Rect(0, 0, 100, 100)  # type: ignore
        self.alien.screen = pygame.Surface((800, 600))  # type: ignore

    def test_init(self):
        """Test the initialization of the Immune class."""
        immune = Immune(self.alien)

        # Assertions
        self.assertEqual(immune.alien, self.alien)
        self.assertEqual(immune.screen, self.alien.screen)  # type: ignore
        self.assertEqual(immune.immune_frames, alien_immune_frames)
        self.assertEqual(immune.current_immune_frame, 0)
        self.assertEqual(immune.immune_image, alien_immune_frames[0])

    def test_update_immune_anim(self):
        """Test the update of the immune animation frames."""
        immune = Immune(self.alien)
        immune.current_immune_frame = 0

        immune.update_immune_anim()

        # Assertions
        self.assertEqual(immune.current_immune_frame, 1)
        self.assertEqual(immune.immune_image, alien_immune_frames[1])
        self.assertEqual(immune.immune_rect.center, self.alien.rect.center)  # type: ignore

        # Test wrapping around to the first frame
        immune.current_immune_frame = len(alien_immune_frames) - 1

        immune.update_immune_anim()

        self.assertEqual(immune.current_immune_frame, 0)
        self.assertEqual(immune.immune_image, alien_immune_frames[0])
        self.assertEqual(immune.immune_rect.center, self.alien.rect.center)  # type: ignore

    def test_draw_immune_anim(self):
        """Test the drawing of the immune animation on the screen."""
        immune = Immune(self.alien)
        immune.screen = MagicMock()

        immune.draw_immune_anim()

        immune.screen.blit.assert_called_once_with(
            immune.immune_image, immune.immune_rect
        )


if __name__ == "__main__":
    unittest.main()
