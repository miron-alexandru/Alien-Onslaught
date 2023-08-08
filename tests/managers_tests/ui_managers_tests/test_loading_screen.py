"""
This module tests the LoadingScreen class which is used to display
the loading screen in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.managers.ui_managers.loading_screen import LoadingScreen


class LoadingScreenTest(unittest.TestCase):
    """Test cases for the LoadingScreen class."""

    def setUp(self):
        """Set up test environment."""
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)

        with patch("pygame.font.Font"):
            self.loading_screen = LoadingScreen(self.screen)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.loading_screen.screen, self.screen)
        self.assertEqual(self.loading_screen.load_bar_width, 400)
        self.assertEqual(self.loading_screen.load_bar_height, 25)
        self.assertEqual(self.loading_screen.load_percent, 0)
        self.assertIsNotNone(self.loading_screen.font)
        self.assertIsNotNone(self.loading_screen.text)

    def test_update(self):
        """Test the update method."""
        self.loading_screen.draw = MagicMock()

        # Initial load percent
        self.assertEqual(self.loading_screen.load_percent, 0)

        self.update_test_helper(50)
        self.update_test_helper(100)

    def update_test_helper(self, percent):
        """Helper function to call the update method with different percents."""
        self.loading_screen.update(percent)

        self.assertEqual(self.loading_screen.load_percent, percent)
        self.loading_screen.draw.assert_called()

    def test_draw(self):
        """Test the draw method."""
        with patch("pygame.draw.rect"), patch("pygame.display.update"):
            self.loading_screen.draw()

            # Assert method calls
            self.screen.fill.assert_called_once_with((2, 24, 49, 255))
            self.assertEqual(pygame.draw.rect.call_count, 2)
            pygame.display.update.assert_called_once()
            self.screen.blit.assert_called_once_with(
                self.loading_screen.text,
                (
                    (
                        self.loading_screen.screen.get_size.return_value[0]
                        - self.loading_screen.text.get_width()
                    )
                    // 2,
                    (
                        self.loading_screen.screen.get_size.return_value[1]
                        - self.loading_screen.text.get_height()
                    )
                    // 2
                    - 40,
                ),
            )


if __name__ == "__main__":
    unittest.main()
