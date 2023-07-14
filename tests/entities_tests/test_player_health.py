"""
This module tests the Hearth class that is used to display the
player health in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.entities.player_entities.player_health import Heart


class TestHeart(unittest.TestCase):
    """Test cases for the Heart class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.heart = Heart(self.game)

    def test_init(self):
        """Test the initialization of the Heart."""
        self.assertEqual(self.heart.screen, self.game.screen)
        self.assertEqual(self.heart.settings, self.game.settings)
        self.assertIsInstance(self.heart.image, pygame.Surface)
        self.assertIsInstance(self.heart.rect, pygame.Rect)
        self.assertEqual(self.heart.rect.topleft, (0, 0))

    def test_blitme(self):
        """Test the blitting of the Heart."""
        self.heart.blitme()

        self.game.screen.blit.assert_called_once_with(self.heart.image, self.heart.rect)

    def test_blitme_screen_rect(self):
        """Test if the heart is blitted at the correct position on the screen."""
        self.heart.rect.topleft = (100, 200)

        self.heart.blitme()

        self.game.screen.blit.assert_called_once_with(self.heart.image, self.heart.rect)

    def test_blitme_screen_rect_updated(self):
        """Test if the heart is blitted at the correct position
        on the screen after updating the rect.
        """
        self.heart.rect.topleft = (100, 200)
        self.heart.rect.move_ip(10, 20)

        self.heart.blitme()

        self.game.screen.blit.assert_called_once_with(self.heart.image, self.heart.rect)


if __name__ == "__main__":
    unittest.main()
