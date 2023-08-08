"""
This module tests the HighScoreManager class that is used to manage the saving and
deletion of the high scores in the game.
"""


import unittest
from unittest.mock import MagicMock, patch

from src.managers.high_score_manager import HighScoreManager


class HighScoreManagerTest(unittest.TestCase):
    """Test cases for the HighScoreManager class."""

    def setUp(self):
        self.game = MagicMock()
        self.game.singleplayer = False
        self.hs_manager = HighScoreManager(self.game)

    def test_init(self):
        """Test the initialization of the manager."""
        self.assertEqual(self.hs_manager.game, self.game)
        self.assertEqual(self.hs_manager.stats, self.game.stats)
        self.assertEqual(self.hs_manager.screen, self.game.screen)
        self.assertEqual(self.hs_manager.high_scores_file, "high_score.json")

    @patch("builtins.open")
    @patch("json.load")
    @patch("json.dump")
    @patch("src.managers.high_score_manager.get_player_name")
    def test_save_high_score(
        self, mock_get_player_name, mock_json_dump, mock_json_load, mock_open
    ):
        """Test the saving of the high score."""
        mock_get_player_name.return_value = "Ake"
        mock_open.return_value.__enter__.return_value = (
            mock_open  # Mock the file object
        )

        # Set up the necessary mock objects and values
        high_scores = {"score_key": []}
        mock_json_load.return_value = high_scores

        self.game.stats.high_score = 100
        self.hs_manager.save_high_score("score_key")

        # Verify that the file was opened and read
        mock_open.has_any_call(self.hs_manager.high_scores_file, "r", encoding="utf-8")

        # Verify that json.load was called with the opened file
        mock_json_load.assert_called_once_with(mock_open)

        # Verify that get_player_name was called
        mock_get_player_name.assert_called_once_with(
            self.game.screen,
            self.game.bg_img,
            self.game.screen_manager.draw_cursor,
            self.game.stats.high_score,
            self.game.settings.game_end_img,
            self.game.settings.game_end_rect,
        )

        # Verify that the high score entry was added or updated
        expected_entry = {"name": "Ake", "score": 100}
        self.assertIn(expected_entry, high_scores["score_key"])

        # Verify that the file was opened for writing and the data was dumped
        mock_open.assert_called_with(
            self.hs_manager.high_scores_file, "w", encoding="utf-8"
        )
        mock_json_dump.assert_called_once_with(high_scores, mock_open)

    @patch("builtins.open")
    @patch("json.load")
    @patch("json.dump")
    def test_delete_high_scores(self, mock_json_dump, mock_json_load, mock_open):
        """Test the delete_high_scores method."""
        mock_open.return_value.__enter__.return_value = (
            mock_open  # Mock the file object
        )

        # Set up the necessary mock objects
        high_scores = {"score_key1": [], "score_key2": []}
        mock_json_load.return_value = high_scores

        # Delete the high scores for the "score_key1"
        self.hs_manager.delete_high_scores("score_key1")

        # Verify that the file was opened and read
        mock_open.has_any_call(self.hs_manager.high_scores_file, "r", encoding="utf-8")

        # Verify that json.load was called with the opened file
        mock_json_load.assert_called_once_with(mock_open)

        # Verify that the high scores for "score_key1" were deleted
        self.assertNotIn("score_key1", high_scores)

        # Verify that the file was opened for writing and the data was dumped
        mock_open.assert_called_with(
            self.hs_manager.high_scores_file, "w", encoding="utf-8"
        )
        mock_json_dump.assert_called_once_with(high_scores, mock_open)

    def test_update_high_score_filename(self):
        """Test the update_high_score_filename method."""
        self.update_high_score_filename_helper(False, "high_score.json")
        self.update_high_score_filename_helper(True, "single_high_score.json")

    def update_high_score_filename_helper(self, singleplayer, high_score_filename):
        """Helper function for the test_update_high_score_filename."""
        self.game.singleplayer = singleplayer

        self.hs_manager.update_high_score_filename()

        self.assertEqual(self.hs_manager.high_scores_file, high_score_filename)


if __name__ == "__main__":
    unittest.main()
