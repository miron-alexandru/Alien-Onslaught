"""
This module tests the ShipsManager class that is used to
manage the ships in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.managers.player_managers.ships_manager import ShipsManager


class TestShipsManager(unittest.TestCase):
    """Test cases for the ShipsManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.game.stats.thunderbird_hp = 3
        self.game.stats.phoenix_hp = 3
        self.ships_manager = ShipsManager(
            self.game, self.game.settings, self.game.singleplayer
        )

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.ships_manager.game, self.game)
        self.assertEqual(self.ships_manager.settings, self.game.settings)
        self.assertEqual(self.ships_manager.singleplayer, self.game.singleplayer)
        self.assertEqual(self.ships_manager.screen, self.game.screen)
        self.assertIsNotNone(self.ships_manager.thunderbird_ship)
        self.assertIsNotNone(self.ships_manager.phoenix_ship)

    def test_thunderbird_ship_hit(self):
        """Test the thunderbird ship hit method."""
        # Case when hp is above 0
        self.game.stats.thunderbird_hp = 2
        self.ships_manager._destroy_ship = MagicMock()

        self.ships_manager.thunderbird_ship_hit()

        self.ships_manager._destroy_ship.assert_called_once_with(
            self.ships_manager.thunderbird_ship
        )

        # Case when hp is below 0
        self.ships_manager._destroy_ship.reset_mock()

        self.game.stats.thunderbird_hp = -1

        self.ships_manager.thunderbird_ship_hit()

        self.ships_manager._destroy_ship.assert_not_called()

    def test_phoenix_ship_hit(self):
        """Test the phoenix ship hit method."""
        # Case when hp is above 0
        self.game.stats.phoenix_hp = 1
        self.ships_manager._destroy_ship = MagicMock()

        self.ships_manager.phoenix_ship_hit()

        self.ships_manager._destroy_ship.assert_called_once_with(
            self.ships_manager.phoenix_ship
        )

        # Case when hp is below 0
        self.ships_manager._destroy_ship.reset_mock()

        self.game.stats.phoenix_hp = -1
        self.ships_manager.phoenix_ship_hit()
        self.ships_manager._destroy_ship.assert_not_called()

    @patch("src.managers.player_managers.ships_manager.play_sound")
    def test_destroy_ship_thunderbird(self, mock_play_sound):
        """Test the destroying of the Thunderbird ship."""
        self.game.settings.game_modes.last_bullet = False
        ship_mock = MagicMock()
        self.ships_manager.thunderbird_ship = ship_mock
        self.ships_manager._update_thunderbird_stats = MagicMock()

        self.ships_manager._destroy_ship(ship_mock)

        ship_mock.explode.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "explode"
        )
        self.assertEqual(self.ships_manager.thunderbird_ship.state.shielded, False)
        self.ships_manager._update_thunderbird_stats.assert_called_once()
        ship_mock.set_immune.assert_called_once()
        ship_mock.center_ship.assert_called_once()
        self.game.score_board.create_health.assert_called_once()
        self.game.gameplay_manager.check_remaining_bullets.assert_not_called()

        self.game.settings.game_modes.last_bullet = True

        self.ships_manager._destroy_ship(ship_mock)

        self.game.gameplay_manager.check_remaining_bullets.assert_called_once()

    @patch("src.managers.player_managers.ships_manager.play_sound")
    def test_destroy_ship_phoenix(self, mock_play_sound):
        """Test the destroying of the Phoenix ship."""
        self.game.settings.game_modes.last_bullet = False
        ship_mock = MagicMock()
        self.ships_manager.phoenix_ship = ship_mock
        self.ships_manager._update_phoenix_stats = MagicMock()

        self.ships_manager._destroy_ship(ship_mock)

        ship_mock.explode.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "explode"
        )
        self.assertEqual(self.ships_manager.phoenix_ship.state.shielded, False)
        self.ships_manager._update_phoenix_stats.assert_called_once()
        ship_mock.set_immune.assert_called_once()
        ship_mock.center_ship.assert_called_once()
        self.game.score_board.create_health.assert_called_once()
        self.game.gameplay_manager.check_remaining_bullets.assert_not_called()

        self.game.settings.game_modes.last_bullet = True

        self.ships_manager._destroy_ship(ship_mock)

        self.game.gameplay_manager.check_remaining_bullets.assert_called_once()

    def test_update_thunderbird_stats(self):
        """Test the update of the Thunderbird ship stats."""
        self.game.settings.thunderbird_bullet_count = 4
        self.game.settings.thunderbird_bullets_allowed = 6
        self.game.stats.thunderbird_hp = 3
        self.ships_manager._update_thunderbird_stats()

        self.assertEqual(self.game.settings.thunderbird_bullet_count, 2)
        self.assertEqual(self.game.settings.thunderbird_bullets_allowed, 5)
        self.assertEqual(self.game.stats.thunderbird_hp, 2)

    def test_update_phoenix_stats(self):
        """Test the update of the Phoenix ship stats."""
        self.game.settings.phoenix_bullet_count = 4
        self.game.settings.phoenix_bullets_allowed = 6
        self.game.stats.phoenix_hp = 3
        self.ships_manager._update_phoenix_stats()

        self.assertEqual(self.game.settings.phoenix_bullet_count, 2)
        self.assertEqual(self.game.settings.phoenix_bullets_allowed, 5)
        self.assertEqual(self.game.stats.phoenix_hp, 2)

    def test_update_ship_alive_states_thunderbird_alive(self):
        """Test case for when the Thunderbird ship has more than 0 hp."""
        self.game.stats.thunderbird_hp = 2
        self.ships_manager.thunderbird_ship.state.exploding = False

        self.ships_manager.update_ship_alive_states()

        self.assertTrue(self.ships_manager.thunderbird_ship.state.alive)

    def test_update_ship_alive_states_thunderbird_dead(self):
        """Test case for when the Thunderbird ship has less than 0 hp."""
        self.game.stats.thunderbird_hp = -1
        self.ships_manager.thunderbird_ship.state.exploding = False

        self.ships_manager.update_ship_alive_states()

        self.assertFalse(self.ships_manager.thunderbird_ship.state.alive)

    def test_update_ship_alive_states_phoenix_alive(self):
        """Test case for when the Phoenix ship has more than 0 hp."""
        self.game.stats.phoenix_hp = 2
        self.ships_manager.phoenix_ship.state.exploding = False

        self.ships_manager.update_ship_alive_states()

        self.assertTrue(self.ships_manager.phoenix_ship.state.alive)

    def test_update_ship_alive_states_phoenix_dead(self):
        """Test case for when the Phoenix ship has less than 0 hp."""
        self.game.stats.phoenix_hp = -1
        self.ships_manager.phoenix_ship.state.exploding = False

        self.ships_manager.update_ship_alive_states()

        self.assertFalse(self.ships_manager.phoenix_ship.state.alive)

    @patch("src.managers.player_managers.ships_manager.play_sound")
    def test_reset_ships(self, mock_play_sound):
        """Test the reset ships method."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        self.game.game_loaded = False

        self.ships_manager.reset_ships()

        ship_mock.reset_ship_state.assert_called_once()
        ship_mock.reset_ship_size.assert_called_once()
        ship_mock.center_ship.assert_called_once()
        ship_mock.start_warp.assert_called_once()
        ship_mock.update_missiles_number.assert_called_once()
        ship_mock.set_cosmic_conflict_pos.assert_called_once()

        self.game.weapons_manager.reset_weapons.assert_called_once()

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "warp"
        )

    def test_update_ship_state(self):
        """Test the update ship state method."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]

        self.ships_manager.update_ship_state()

        ship_mock.update_state.assert_called_once()


if __name__ == "__main__":
    unittest.main()
