"""
This module tests the Button class that is used to create
the buttons in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.ui.button import Button


class ButtonTest(unittest.TestCase):
    """Test cases for the Button class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.image_loc = "button_img_path"
        self.pos = (100, 100)
        self.description = "Test Button"
        with patch(
            "src.ui.button.pygame.image.load", return_value=pygame.Surface((50, 50))
        ):
            self.button = Button(self.game, self.image_loc, self.pos, self.description)

    def test_button_initialization(self):
        """Test class initialization."""
        self.assertEqual(self.button.screen, self.game.screen)
        self.assertEqual(self.button.screen_rect, self.game.screen.get_rect())
        self.assertFalse(self.button.visible)
        self.assertEqual(self.button.description, "Test Button")
        self.assertIsInstance(self.button.image, pygame.Surface)
        self.assertIsInstance(self.button.rect, pygame.Rect)
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)

    def test_button_update_pos_with_args(self):
        """Test the update_button_pos with *args passed in."""
        self.button.update_pos(15, 55)

        self.assertEqual(self.button.rect.topleft, (15, 55))

    def test_button_update_pos_with_x_y(self):
        """Test the update_button_pos with x and y passed."""
        self.button.update_pos(x=50, y=-50)

        self.assertEqual(self.button.rect.x, 150)
        self.assertEqual(self.button.rect.y, 50)

    def test_button_update_pos_with_center(self):
        """Test the update_button_pos with center passed in."""
        self.button.update_pos((300, 200))

        self.assertEqual(self.button.rect.center, (300, 200))

    def test_button_update_pos_with_center_and_offset(self):
        """Test the update_button_pos with center and also x, y passed."""
        self.button.update_pos((300, 200), x=10, y=-10)

        self.assertEqual(self.button.rect.center, (310, 190))
        self.assertEqual(self.button.rect.x, 285)
        self.assertEqual(self.button.rect.y, 165)

    def test_button_draw_button(self):
        """Test the drawing of the button."""
        self.button.draw_button()

        self.game.screen.blit.assert_called_once_with(
            self.button.image, self.button.rect
        )

    @patch("src.ui.button.display_description")
    def test_button_show_button_info(self, mock_description):
        """Test the show_button_info method."""
        self.game.screen.get_size.return_value = (800, 600)
        screen_width, screen_height = self.game.screen.get_size()

        self.button.show_button_info()

        mock_description.assert_called_with(
            self.game.screen,
            "Test Button",
            screen_width // 2 + 74,
            screen_height // 2 + 180,
        )


if __name__ == "__main__":
    unittest.main()
