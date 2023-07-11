"""
This module tests the GameStats class which is used to 
manage the statistics that change during the game.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.game_logic.game_stats import GameStats
from src.utils.constants import MAX_HP


class GameStatsTestCase(unittest.TestCase):
    """Test cases for the GameStats class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.game.settings = MagicMock()
        self.game.settings.starting_phoenix_hp = 3
        self.game.settings.starting_thunder_hp = 3
        self.phoenix_ship = MagicMock()
        self.thunderbird_ship = MagicMock()
        self.stats = GameStats(self.game, self.phoenix_ship, self.thunderbird_ship)

    def test_init(self):
        """Test the initialization of the class."""
        self.game.settings.game_modes.one_life_reign = False
        self.stats = GameStats(self.game, self.phoenix_ship, self.thunderbird_ship)

        self.assertEqual(self.stats.game, self.game)
        self.assertEqual(self.stats.settings, self.game.settings)
        self.assertEqual(self.stats.phoenix_hp, 3)
        self.assertEqual(self.stats.thunderbird_hp, 3)
        self.assertEqual(self.stats.max_hp, 5)
        self.assertEqual(self.stats.game_active, False)
        self.assertEqual(self.stats.high_score, 0)

        # Test the one one life reign case
        self.game.settings.game_modes.one_life_reign = True

        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)

        self.assertEqual(self.stats.phoenix_hp, 0)
        self.assertEqual(self.stats.thunderbird_hp, 0)
        self.assertEqual(self.stats.max_hp, 1)

    def test_reset_stats(self):
        """Test the reset_stats method."""
        self.game.settings.game_modes.one_life_reign = False
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)

        self.assertTrue(self.phoenix_ship.state.alive)
        self.assertTrue(self.thunderbird_ship.state.alive)
        self.assertEqual(self.stats.phoenix_hp, 3)
        self.assertEqual(self.stats.thunderbird_hp, 3)
        self.assertEqual(self.stats.max_hp, MAX_HP)
        self.assertEqual(
            self.stats.thunder_bullets, self.game.settings.thunderbird_bullet_count
        )
        self.assertEqual(
            self.stats.fire_bullets, self.game.settings.phoenix_bullet_count
        )
        self.assertEqual(self.stats.thunderbird_score, 0)
        self.assertEqual(self.stats.phoenix_score, 0)
        self.assertEqual(self.stats.level, 1)
        self.assertEqual(self.stats.high_score, 0)

        self.game.settings.game_modes.one_life_reign = True
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)

        self.assertEqual(self.stats.phoenix_hp, 0)
        self.assertEqual(self.stats.thunderbird_hp, 0)
        self.assertEqual(self.stats.max_hp, 1)

    def test_increase_level(self):
        """Test the increase_level method."""
        initial_level = self.stats.level
        self.stats.increase_level()
        new_level = self.stats.level

        self.assertEqual(new_level, initial_level + 1)

    def test_set_one_life_reign_stats(self):
        """Test the setting of the stats for the one life reign."""
        self.stats._set_one_life_reign_stats()

        self.assertEqual(self.stats.phoenix_hp, 0)
        self.assertEqual(self.stats.thunderbird_hp, 0)
        self.assertEqual(self.stats.max_hp, 1)

    @patch("src.game_logic.game_stats.play_sound")
    def test_revive_thunderbird(self, mock_play_sound):
        """Test the revive of the thunderbird ship."""
        self.stats.revive_thunderbird(self.thunderbird_ship)

        self.assertEqual(self.stats.thunderbird_hp, 1)
        self.assertTrue(self.thunderbird_ship.state.alive)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "warp"
        )

    @patch("src.game_logic.game_stats.play_sound")
    def test_revive_phoenix(self, mock_play_sound):
        """Test the revive of the phoenix ship."""
        self.stats.revive_phoenix(self.phoenix_ship)

        self.assertEqual(self.stats.phoenix_hp, 1)
        self.assertTrue(self.phoenix_ship.state.alive)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "warp"
        )

    @patch("src.game_logic.game_stats.play_sound")
    def test_revive_ship(self, mock_play_sound):
        """Test the revive_ship method."""
        self.game.settings.game_modes.last_bullet = False
        ship = self.thunderbird_ship
        self.stats._revive_ship(ship)

        self.assertTrue(self.phoenix_ship.state.alive)
        ship.reset_ship_state.assert_called_once()
        ship.center_ship.assert_called_once()
        ship.start_warp.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "warp"
        )
        self.game.score_board.render_bullets_num.assert_not_called()

        # Test case for the last_bullet
        self.game.settings.game_modes.last_bullet = True

        self.stats._revive_ship(ship)

        self.game.score_board.render_bullets_num.assert_called_once()


if __name__ == "__main__":
    unittest.main()
