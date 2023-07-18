"""
This module tests the EndGameManager which manages the endgame
behaviors.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.managers.game_over_manager import EndGameManager


class MockGame:
    """Mock game used to test the EndGameManager."""

    def __init__(self):
        self.thunderbird_ship = MagicMock()
        self.phoenix_ship = MagicMock()
        self.aliens = pygame.sprite.Group()
        self.ui_options = MagicMock()
        self.sound_manager = MagicMock()
        self.gameplay_manager = MagicMock()
        self.reset_bg = MagicMock()
        self.score_board = MagicMock()


class TestEndGameManager(unittest.TestCase):
    """Test cases for the EndGameManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MockGame()
        self.settings = MagicMock()
        self.stats = MagicMock()
        self.screen = MagicMock()
        self.end_game_manager = EndGameManager(
            self.game, self.settings, self.stats, self.screen
        )

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.end_game_manager.game, self.game)
        self.assertEqual(self.end_game_manager.settings, self.settings)
        self.assertEqual(self.end_game_manager.stats, self.stats)
        self.assertEqual(self.end_game_manager.screen, self.screen)
        self.assertEqual(self.end_game_manager.ending_music, "")

    def test_check_game_over_cosmic_conflict_phoenix_win(self):
        """Test the game ending scenario in cosmic conflict when
        the Phoenix player wins."""
        self.settings.game_modes.cosmic_conflict = True
        self.game.thunderbird_ship.state.alive = False
        self.game.phoenix_ship.state.alive = True

        with patch(
            "src.managers.game_over_manager.EndGameManager._display_endgame"
        ) as mock_display_endgame:
            self.end_game_manager.check_game_over()

            mock_display_endgame.assert_called_with("phoenix_win")

    def test_check_game_over_cosmic_conflict_thunder_win(self):
        """Test the game ending scenario in cosmic conflict
        when the Thunderbird player wins."""
        self.settings.game_modes.cosmic_conflict = True
        self.game.thunderbird_ship.state.alive = True
        self.game.phoenix_ship.state.alive = False

        with patch(
            "src.managers.game_over_manager.EndGameManager._display_endgame"
        ) as mock_display_endgame:
            self.end_game_manager.check_game_over()

            mock_display_endgame.assert_called_with("thunder_win")

    def test_check_game_over_boss_rush_victory(self):
        """Test the game ending in the boss rush game mode."""
        self.settings.game_modes.boss_rush = True
        self.stats.level = 15

        with patch(
            "src.managers.game_over_manager.EndGameManager._display_endgame"
        ) as mock_display_endgame:
            self.end_game_manager.check_game_over()

            mock_display_endgame.assert_called_with("victory")
            self.game.score_board.render_high_score.assert_called()

    def test_check_game_over_defeat(self):
        """Test the game ending when losing the game.
        (Both players are dead).
        """
        self.settings.game_modes.cosmic_conflict = False
        self.settings.game_modes.boss_rush = False
        self.game.thunderbird_ship.state.alive = False
        self.game.phoenix_ship.state.alive = False

        with patch(
            "src.managers.game_over_manager.EndGameManager._display_endgame"
        ) as mock_display_endgame:
            self.end_game_manager.check_game_over()

            mock_display_endgame.assert_called_with("gameover")

    @patch("src.managers.game_over_manager.EndGameManager.set_game_end_position")
    @patch("src.managers.game_over_manager.EndGameManager._play_game_over_sound")
    @patch("src.managers.game_over_manager.EndGameManager._check_high_score_saved")
    def test_display_game_over(
        self,
        mock_check_high_score_saved,
        mock_play_game_over_sound,
        mock_set_game_end_position,
    ):
        """Test the display game over method."""
        self.end_game_manager._display_game_over()

        self.game.score_board.update_high_score.assert_called_once()
        self.screen.blit.assert_called_once_with(
            self.settings.game_end_img, self.settings.game_end_rect
        )
        self.game.gameplay_manager.reset_game_objects.assert_called_once()
        mock_set_game_end_position.assert_called_once()
        mock_play_game_over_sound.assert_called_once()
        mock_check_high_score_saved.assert_called_once()

    def test_play_game_over_sound_already_played(self):
        """Test the play game over sound when the sound was
        already played before."""
        self.game.ui_options.game_over_sound_played = True

        with patch("src.managers.game_over_manager.play_music") as mock_play_music:
            self.end_game_manager._play_game_over_sound()

        mock_play_music.assert_not_called()

    def test_play_game_over_sound_first_time(self):
        """Test the play game over sound when the sound
        wasn't played.
        """
        self.game.ui_options.game_over_sound_played = False
        self.end_game_manager.ending_music = "game_over"

        with patch("src.managers.game_over_manager.play_music") as mock_play_music:
            self.end_game_manager._play_game_over_sound()

        mock_play_music.assert_called_with(
            self.game.sound_manager.menu_music, "game_over"
        )
        self.assertEqual(self.game.ui_options.game_over_sound_played, True)
        self.assertEqual(
            self.game.sound_manager.current_sound,
            self.game.sound_manager.menu_music["game_over"],
        )

    def test_set_game_end_position(self):
        """Test te positioning of the ending text on screen."""
        self.settings.screen_width = 800
        self.settings.screen_height = 600

        self.end_game_manager.set_game_end_position()

        self.assertEqual(self.settings.game_end_rect.centerx, 400)
        self.assertEqual(self.settings.game_end_rect.centery, 50)


if __name__ == "__main__":
    unittest.main()
