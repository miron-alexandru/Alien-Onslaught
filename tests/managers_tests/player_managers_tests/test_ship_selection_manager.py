"""This module tests the ShipSelection class that is used for
choosing the ship in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.managers.player_managers.ship_selection_manager import ShipSelection


class ShipSelectionTest(unittest.TestCase):
    """Unit tests for the ShipSelection class."""

    def setUp(self):
        """Set up the test environment."""
        pygame.init()
        self.game = MagicMock()
        self.ship_images = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        self.ship_selection = ShipSelection(
            self.game, self.game.screen, self.ship_images, self.game.settings
        )
        self.ship_selection.font = MagicMock()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.ship_selection.screen, self.game.screen)
        self.assertEqual(self.ship_selection.game, self.game)
        self.assertEqual(self.ship_selection.settings, self.game.settings)
        self.assertEqual(self.ship_selection.ship_images, self.ship_images)
        self.assertEqual(
            self.ship_selection.thunderbird_ship, self.game.thunderbird_ship
        )
        self.assertEqual(self.ship_selection.phoenix_ship, self.game.phoenix_ship)
        self.assertIsNotNone(self.ship_selection.font)
        self.assertEqual(self.ship_selection.clickable_regions, [])
        self.assertIsInstance(self.ship_selection.ship_selection_functions, dict)
        self.assertEqual(len(self.ship_selection.ship_selection_functions), 6)

    def test_draw_ship_type_text(self):
        """Test the draw_ship_type_text method."""
        self.ship_selection.draw_ship_type_text(1, 25, 50)
        self.ship_selection.font.render.assert_called_with(
            "Thunderbird", True, (255, 255, 255)
        )
        self.game.screen.blit.assert_called_with(
            self.ship_selection.font.render.return_value, (50, 25)
        )

    @patch("src.managers.player_managers.ship_selection_manager.pygame.mouse.get_pos")
    @patch("src.managers.player_managers.ship_selection_manager.display_description")
    def test_draw_ships(self, mock_display_description, _):
        """Test the draw_ships method."""
        y_position = 100
        x_position = 200

        # Call the method being tested
        self.ship_selection.draw_ships(1, y_position, x_position)

        # Assert the expected behavior
        self.assertEqual(len(self.ship_selection.clickable_regions), 3)
        self.assertEqual(mock_display_description.call_count, 3)

        self.ship_selection.draw_ships(2, x_position, y_position)

        self.assertEqual(len(self.ship_selection.clickable_regions), 6)
        self.assertEqual(mock_display_description.call_count, 6)

    @patch("src.managers.player_managers.ship_selection_manager.play_sound")
    @patch("src.managers.player_managers.ship_selection_manager.pygame.Rect")
    def test_handle_ship_selection(self, _, mock_play_sound):
        """Test the handle_ship_selection method."""
        mouse_pos = (60, 100)
        self.game.ui_options.ship_selection = True
        self.ship_selection.clickable_regions = [(pygame.Rect(50, 75, 10, 10), 1, 0)]

        self.ship_selection.handle_ship_selection(mouse_pos)

        self.game.settings.regular_thunder_ship.assert_called()
        mock_play_sound.assert_called_with(
            self.game.sound_manager.game_sounds, "select_ship"
        )

    @patch("src.managers.player_managers.ship_selection_manager.play_sound")
    @patch("src.managers.player_managers.ship_selection_manager.pygame.Rect")
    def test_handle_ship_selection_singleplayer(self, _, mock_play_sound):
        """Test the handle_ship_selection method in singleplayer mode."""
        mouse_pos = (60, 100)
        self.ship_selection.clickable_regions = [(pygame.Rect(50, 75, 10, 10), 1, 0)]
        self.game.singleplayer = True
        self.ship_selection.thunderbird_ship.ship_selected = False

        self.ship_selection.handle_ship_selection(mouse_pos)

        self.assertTrue(self.ship_selection.thunderbird_ship.ship_selected)
        self.assertFalse(self.game.ui_options.ship_selection)
        mock_play_sound.assert_called_with(
            self.game.sound_manager.game_sounds, "select_ship"
        )

    @patch("src.managers.player_managers.ship_selection_manager.play_sound")
    @patch("src.managers.player_managers.ship_selection_manager.pygame.Rect")
    def test_handle_ship_selection_multiplayer(self, _, mock_play_sound):
        """Test the handle_ship_selection method in multiplayer mode."""
        mouse_pos = (60, 100)
        self.ship_selection.clickable_regions = [
            (pygame.Rect(50, 75, 15, 15), 2, 1),
            (pygame.Rect(70, 85, 15, 15), 1, 2),
        ]
        self.ship_selection.ship_selection_functions = {
            (1, 2): ("artillery_thunder", self.game.settings.heavy_artillery_thunder),
            (2, 1): ("fast_phoenix", self.game.settings.fast_phoenix),
        }
        self.game.singleplayer = False
        self.game.ui_options.ship_selection = True
        self.ship_selection.thunderbird_ship.ship_selected = False
        self.ship_selection.phoenix_ship.ship_selected = False

        self.ship_selection.handle_ship_selection(mouse_pos)

        self.game.settings.fast_phoenix.assert_called_once()
        self.game.settings.heavy_artillery_thunder.assert_called_once()
        mock_play_sound.assert_called_with(
            self.game.sound_manager.game_sounds, "select_ship"
        )

        self.assertTrue(self.ship_selection.thunderbird_ship.ship_selected)
        self.assertFalse(self.game.ui_options.ship_selection)


if __name__ == "__main__":
    unittest.main()
