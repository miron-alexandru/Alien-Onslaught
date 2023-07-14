"""
This module tests the Phoenix class which represents the
Phoenix player in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.entities.player_entities.player_ships import Phoenix


class TestPhoenix(unittest.TestCase):
    """Test cases for the Phoenix class."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.game.screen.get_rect.return_value = pygame.Rect(0, 0, 800, 600)
        self.ship = Phoenix(self.game)

    def test_init(self):
        """Test the initialization of the ship."""
        self.assertEqual(
            self.ship.missiles_num, self.game.settings.phoenix_missiles_num
        )
        self.assertEqual(self.ship.ship_type, "phoenix")
        self.assertEqual(self.ship.offset, 200)

    @patch("pygame.transform")
    def test_set_cosmic_conflict_pos(self, mock_transform):
        """Test the positioning in the cosmic conflict game mode."""
        # Cosmic conflict game mode active
        self.game.settings.game_modes.cosmic_conflict = True

        self.ship.set_cosmic_conflict_pos()

        self.assertTrue(self.game.screen.get_rect.called)
        self.assertEqual(self.ship.image, pygame.transform.rotate.return_value)
        self.assertEqual(
            self.ship.cosmic_conflict_pos,
            self.game.screen.get_rect.return_value.right - 50,
        )

        # Cosmic conflict game mode not active
        self.game.settings.game_modes.cosmic_conflict = False
        mock_transform.reset_mock()

        self.ship.set_cosmic_conflict_pos()

        self.assertFalse(pygame.transform.rotate.called)
        self.assertEqual(self.ship.image, pygame.transform.rotate.return_value)
        self.assertEqual(
            self.ship.cosmic_conflict_pos,
            self.game.screen.get_rect.return_value.right - 50,
        )


if __name__ == "__main__":
    unittest.main()
