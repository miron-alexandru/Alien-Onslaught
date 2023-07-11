"""
This module tests the WeaponsManagers class which manages the
player weapons in the game.
"""

import time
import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.utils.constants import WEAPONS
from src.managers.player_managers.weapons_manager import WeaponsManager


class WeaponsManagerTest(unittest.TestCase):
    """Test cases for the WeaponsManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.thunderbird_ship = MagicMock()
        self.phoenix_ship = MagicMock()

        self.weapons_manager = WeaponsManager(self.game)

        self.weapons_manager.singleplayer_projectiles = [MagicMock(), MagicMock()]
        self.weapons_manager.multiplayer_projectiles = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]

    @patch("src.managers.player_managers.weapons_manager.load_single_image")
    def test_init(self, mock_load_single_image):
        """Test the initialization of the weapons manager."""
        mock_weapon_image1 = MagicMock()
        mock_weapon_image2 = MagicMock()
        mock_load_single_image.side_effect = [mock_weapon_image1, mock_weapon_image2]

        # Create an instance of WeaponsManager
        weapons_manager = WeaponsManager(self.game)

        # Assert that the attributes are set correctly
        self.assertEqual(self.weapons_manager.game, self.game)
        self.assertEqual(self.weapons_manager.settings, self.game.settings)
        self.assertEqual(self.weapons_manager.game_modes, self.game.settings.game_modes)
        self.assertEqual(self.weapons_manager.screen, self.game.screen)
        self.assertEqual(self.weapons_manager.sound_manager, self.game.sound_manager)
        self.assertFalse(self.weapons_manager.draw_laser_message)
        self.assertEqual(self.weapons_manager.display_time, 0)
        self.assertEqual(
            self.weapons_manager.thunderbird_ship, self.game.thunderbird_ship
        )
        self.assertEqual(self.weapons_manager.phoenix_ship, self.game.phoenix_ship)

        # Verify that the load_single_image function is called with the correct parameters
        mock_load_single_image.assert_any_call(WEAPONS["thunderbolt"])
        mock_load_single_image.assert_any_call(WEAPONS["firebird"])

        # Assert that the weapons dictionary is initialized correctly
        expected_weapons = {
            "thunderbird": {
                "weapon": mock_weapon_image1,
                "current": "thunderbolt",
            },
            "phoenix": {
                "weapon": mock_weapon_image2,
                "current": "firebird",
            },
        }
        self.assertDictEqual(weapons_manager.weapons, expected_weapons)

        # Assert that the lists of projectiles are initialized correctly

        expected_singleplayer_projectiles = [
            self.game.thunderbird_bullets,
            self.game.thunderbird_missiles,
            self.game.thunderbird_laser,
        ]

        expected_multiplayer_projectiles = [
            self.game.thunderbird_bullets,
            self.game.thunderbird_missiles,
            self.game.thunderbird_laser,
            self.game.phoenix_bullets,
            self.game.phoenix_missiles,
            self.game.phoenix_laser,
        ]

        self.assertEqual(
            weapons_manager.singleplayer_projectiles, expected_singleplayer_projectiles
        )
        self.assertEqual(
            weapons_manager.multiplayer_projectiles, expected_multiplayer_projectiles
        )

    def test_set_weapon_same_as_current(self):
        """Test the set_weapon methon when the weapon is the
        same as the current weapon.
        """
        self.weapons_manager.weapons["thunderbird"]["current"] = "blaster"
        self.weapons_manager.game_modes.last_bullet = False

        self.weapons_manager.set_weapon("thunderbird", "blaster")

        self.game.powers_manager.increase_bullet_count.assert_called_once_with(
            "thunderbird"
        )

    @patch("src.managers.player_managers.weapons_manager.load_single_image")
    def test_set_weapon_new_weapon(self, mock_load_image):
        """Test the set_weapon method when assigning a new weapon."""
        self.weapons_manager.weapons["thunderbird"]["current"] = "laser"

        self.weapons_manager.set_weapon("thunderbird", "blaster")

        self.game.powers_manager.increase_bullet_count.assert_not_called()
        mock_load_image.assert_called_once_with(WEAPONS["blaster"])
        self.assertEqual(
            self.weapons_manager.weapons["thunderbird"]["current"], "blaster"
        )

    @patch("src.managers.player_managers.weapons_manager.load_single_image")
    def test_reset_weapons(self, mock_load_image):
        """Test the reset_weapons method."""
        self.weapons_manager.weapons["thunderbird"]["current"] = "blaster"
        self.weapons_manager.weapons["phoenix"]["current"] = "laser"

        self.weapons_manager.reset_weapons()

        self.assertEqual(
            self.weapons_manager.weapons["thunderbird"]["current"], "thunderbolt"
        )
        self.assertEqual(self.weapons_manager.weapons["phoenix"]["current"], "firebird")

        mock_load_image.called_once_with(WEAPONS["thunderbolt"])
        mock_load_image.called_once_with(WEAPONS["firebird"])

    def test_update_projectiles_singleplayer(self):
        """Test the update of the projectiles in singleplayer."""
        self.game.singleplayer = True

        self.weapons_manager.update_projectiles()

        self.weapons_manager.singleplayer_projectiles[0].update.assert_called_once()
        self.weapons_manager.multiplayer_projectiles[0].update.assert_not_called()

    def test_update_projectiles_multiplayer(self):
        """Test the update of the projectiles in multiplayer."""
        self.game.singleplayer = False

        self.weapons_manager.update_projectiles()

        self.weapons_manager.multiplayer_projectiles[0].update.assert_called_once()
        self.weapons_manager.singleplayer_projectiles[0].update.assert_not_called()

    def test_remove_out_of_screen_projectiles_singleplayer(self):
        """Test if projectiles that went off screen are removed
        in singleplayer.
        """
        self.game.singleplayer = True
        projectile_mock1 = MagicMock()
        projectile_mock2 = MagicMock()
        self.weapons_manager.singleplayer_projectiles[0].copy.return_value = [
            projectile_mock1,
            projectile_mock2,
        ]

        self.weapons_manager.update_projectiles()

        self.weapons_manager.singleplayer_projectiles[0].update.assert_called()

        self.assertTrue(self.weapons_manager.singleplayer_projectiles[0].copy.called)
        self.assertTrue(
            self.weapons_manager.singleplayer_projectiles[0].remove.called_with(
                projectile_mock1
            )
        )

        self.assertFalse(self.weapons_manager.multiplayer_projectiles[0].copy.called)
        self.assertFalse(self.weapons_manager.multiplayer_projectiles[0].remove.called)

    def test_remove_out_of_screen_projectiles_multiplayer(self):
        """Test if projectiles that went off screen are removed
        in multiplayer.
        """
        self.game.singleplayer = False

        self.weapons_manager.update_projectiles()

        self.weapons_manager.multiplayer_projectiles[0].update.assert_called()

        self.assertTrue(self.weapons_manager.multiplayer_projectiles[0].copy.called)
        self.assertTrue(
            self.weapons_manager.multiplayer_projectiles[0].remove.called_once()
        )

        self.assertFalse(self.weapons_manager.singleplayer_projectiles[0].copy.called)
        self.assertFalse(self.weapons_manager.singleplayer_projectiles[0].remove.called)

    def test_fire_bullet_ship_disarmed(self):
        """Test the fire_bullet method when the ship is disarmed."""
        bullets_mock = MagicMock()
        bullets_allowed = 5
        bullet_class_mock = MagicMock()
        num_bullets = 1
        ship_mock = MagicMock()
        ship_mock.remaining_bullets = 0
        ship_mock.state.disarmed = True

        self.weapons_manager.fire_bullet(
            bullets_mock, bullets_allowed, bullet_class_mock, num_bullets, ship_mock
        )

        bullets_mock.add.assert_not_called()
        bullet_class_mock.assert_not_called()
        self.game.sound_manager.game_sounds.assert_not_called()

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_fire_bullet_max_bullets_reached(self, mock_play_sound):
        """Test the fire_bullet method when the ship fired the maximum
        number of bullets allowed on screen.
        """
        bullets_mock = MagicMock()
        bullets_mock.__len__.return_value = 5
        bullets_allowed = 5
        bullet_class_mock = MagicMock()
        num_bullets = 1
        ship_mock = MagicMock()
        ship_mock.remaining_bullets = 5
        ship_mock.state.disarmed = False

        self.weapons_manager.fire_bullet(
            bullets_mock, bullets_allowed, bullet_class_mock, num_bullets, ship_mock
        )

        bullets_mock.add.assert_not_called()
        bullet_class_mock.assert_not_called()
        mock_play_sound.assert_not_called()

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_fire_bullet(self, mock_play_sound):
        """Test the fire_bullet method when the ship successfully
        fires bullets.
        """
        # General bullet fire
        bullets_mock = MagicMock()
        bullets_mock.__len__.return_value = 3
        bullets_allowed = 5
        bullet_class_mock = MagicMock()
        num_bullets = 1
        ship_mock = MagicMock()
        ship_mock.remaining_bullets = 5
        ship_mock.state.disarmed = False
        ship_mock.state.scaled_weapon = False
        ship_mock.remaining_bullets = 2
        self.weapons_manager.game_modes.last_bullet = False

        self.weapons_manager.fire_bullet(
            bullets_mock, bullets_allowed, bullet_class_mock, num_bullets, ship_mock
        )

        self.game.score_board.render_bullets_num.assert_not_called()
        bullet_class_mock.assert_called_once_with(self.weapons_manager, ship_mock)
        bullets_mock.add.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "bullet"
        )

        # Case when last_bullet game mode is active.
        self.weapons_manager.game_modes.last_bullet = True

        self.weapons_manager.fire_bullet(
            bullets_mock, bullets_allowed, bullet_class_mock, num_bullets, ship_mock
        )

        self.assertEqual(ship_mock.remaining_bullets, 1)
        self.game.score_board.render_bullets_num.assert_called_once()

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_fire_missile_no_missiles(self, mock_play_sound):
        """Test the fire_missile method when the player has no
        missiles left.
        """
        missiles_mock = MagicMock()
        ship_mock = MagicMock()
        ship_mock.missiles_num = 0
        missile_class_mock = MagicMock()

        self.weapons_manager.fire_missile(missiles_mock, ship_mock, missile_class_mock)

        missiles_mock.add.assert_not_called()
        mock_play_sound.assert_not_called()

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_fire_missile(self, mock_play_sound):
        """Test the fire_missile method when the player successfully
        launches a missile.
        """
        missiles_mock = MagicMock()
        ship_mock = MagicMock()
        ship_mock.missiles_num = 2
        missile_class_mock = MagicMock()

        self.weapons_manager.fire_missile(missiles_mock, ship_mock, missile_class_mock)

        missile_class_mock.assert_called_once_with(self.weapons_manager, ship_mock)
        missiles_mock.add.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "missile_launch"
        )
        self.assertEqual(ship_mock.missiles_num, 1)
        self.game.score_board.render_missiles_num.assert_called_once_with(ship_mock)

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    @patch("src.managers.player_managers.weapons_manager.time.time")
    def test_timed_laser(self, mock_time, mock_play_sound):
        """Test the timed_laser method."""
        # Laser ready (the player successfully fires the laser.)
        lasers_mock = MagicMock()
        ship_mock = MagicMock()
        laser_class_mock = MagicMock()
        self.game.pause_time = pygame.time.get_ticks()
        self.game.settings.laser_cooldown = 5
        ship_mock.last_laser_time = 0
        mock_time.return_value = 5

        self.weapons_manager._timed_laser(lasers_mock, ship_mock, laser_class_mock)

        laser_class_mock.assert_called_once_with(self.weapons_manager, ship_mock)
        lasers_mock.add.assert_called_once()
        self.assertEqual(ship_mock.last_laser_time, mock_time.return_value)
        self.assertEqual(self.game.pause_time, 0)
        self.assertFalse(ship_mock.laser_ready)
        self.assertFalse(self.weapons_manager.draw_laser_message)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "fire_laser"
        )

        # Laser not ready, the player does not fire the laser because
        # not enought time has passed.
        mock_play_sound.reset_mock()
        self.weapons_manager.draw_laser_message = False
        self.weapons_manager._timed_laser(lasers_mock, ship_mock, laser_class_mock)

        self.assertTrue(self.weapons_manager.draw_laser_message)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "laser_not_ready"
        )

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_normal_laser(self, mock_play_sound):
        """Test the normal_laser method."""
        lasers_mock = MagicMock()
        ship_mock = MagicMock()
        laser_class_mock = MagicMock()
        self.game.settings.game_modes.last_bullet = False
        self.weapons_manager.draw_laser_message = False
        ship_mock.aliens_killed = 5
        self.game.settings.required_kill_count = 5

        # Case when the ship fires the laser
        self.weapons_manager._normal_laser(lasers_mock, ship_mock, laser_class_mock)

        laser_class_mock.assert_called_once_with(self.weapons_manager, ship_mock)
        lasers_mock.add.assert_called_once()
        self.assertEqual(ship_mock.aliens_killed, 0)
        self.assertFalse(ship_mock.laser_ready)
        self.assertFalse(self.weapons_manager.draw_laser_message)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "fire_laser"
        )

        # Case when ship tries to fire the laser and is not ready yet.
        mock_play_sound.reset_mock()
        ship_mock.aliens_killed = 4
        self.weapons_manager.draw_laser_message = False

        self.weapons_manager._normal_laser(lasers_mock, ship_mock, laser_class_mock)

        self.assertTrue(self.weapons_manager.draw_laser_message)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "laser_not_ready"
        )

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    def test_normal_laser_last_bullet(self, mock_play_sound):
        """Test the functionality of the normal laser in the last_bullet game mode."""
        lasers_mock = MagicMock()
        ship_mock = MagicMock()
        laser_class_mock = MagicMock()
        self.game.settings.game_modes.last_bullet = True
        self.weapons_manager.draw_laser_message = False

        self.weapons_manager.fire_laser(lasers_mock, ship_mock, laser_class_mock)

        self.assertTrue(self.weapons_manager.draw_laser_message)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "laser_not_ready"
        )
        lasers_mock.add.assert_not_called()

    def test_fire_laser(self):
        """Test the fire_laser method."""
        # Fire timed laser case
        lasers_mock = MagicMock()
        ship_mock = MagicMock()
        laser_class_mock = MagicMock()
        self.game.settings.game_modes.game_mode = ["timed_laser_mode"]
        self.game.settings.timed_laser_modes = ["timed_laser_mode"]
        self.weapons_manager._timed_laser = MagicMock()
        self.weapons_manager._normal_laser = MagicMock()

        self.weapons_manager.fire_laser(lasers_mock, ship_mock, laser_class_mock)

        self.weapons_manager._timed_laser.assert_called_once_with(
            lasers_mock, ship_mock, laser_class_mock
        )
        self.weapons_manager._normal_laser.assert_not_called()

        # Fire normal laser case
        self.weapons_manager._timed_laser.reset_mock()
        self.game.settings.game_modes.game_mode = ["normal_laser_mode"]

        self.weapons_manager.fire_laser(lasers_mock, ship_mock, laser_class_mock)

        self.weapons_manager._normal_laser.assert_called_once_with(
            lasers_mock, ship_mock, laser_class_mock
        )
        self.weapons_manager._timed_laser.assert_not_called()

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    @patch("src.managers.player_managers.weapons_manager.time.time")
    def test_update_normal_laser_status_laser_ready(self, mock_time, mock_play_sound):
        """Test the update of the laser status when the laser is available."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        self.game.settings.required_kill_count = 10
        mock_time.return_value = 10
        ship_mock.aliens_killed = 10
        ship_mock.laser_ready = False
        ship_mock.laser_ready_msg = False

        self.weapons_manager.update_normal_laser_status()

        self.assertTrue(ship_mock.laser_ready)
        self.assertTrue(ship_mock.laser_ready_msg)
        self.assertEqual(ship_mock.laser_ready_start_time, time.time())
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "laser_ready"
        )

    def test_update_normal_laser_status_laser_not_ready(self):
        """Test the update of the laser status when the laser is not ready."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        self.game.settings.required_kill_count = 5
        ship_mock.aliens_killed = 4
        ship_mock.laser_ready = False
        ship_mock.laser_ready_msg = False
        ship_mock.laser_ready_start_time = 5

        self.weapons_manager.update_normal_laser_status()

        self.assertFalse(ship_mock.laser_ready)
        self.assertFalse(ship_mock.laser_ready_msg)

    @patch("src.managers.player_managers.weapons_manager.play_sound")
    @patch("src.managers.player_managers.weapons_manager.time.time")
    def test_update_timed_laser_status_laser_ready(self, mock_time, mock_play_sound):
        """Test the update of the timed laser status when the laser is ready."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        self.game.settings.laser_cooldown = 5
        mock_time.return_value = 5
        ship_mock.last_laser_usage = 0
        ship_mock.laser_ready = False

        self.weapons_manager.update_timed_laser_status()

        self.assertTrue(ship_mock.laser_ready)
        self.assertEqual(ship_mock.laser_ready_start_time, time.time())
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "laser_ready"
        )

    @patch("src.managers.player_managers.weapons_manager.time.time")
    def test_update_timed_laser_status_laser_not_ready(self, mock_time):
        """Test the update of the timed laser status when the laser is not ready."""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        self.game.settings.laser_cooldown = 5
        mock_time.return_value = 5
        ship_mock.laser_ready_start_time = 2
        ship_mock.last_laser_usage = 0
        ship_mock.laser_ready = True

        self.weapons_manager.update_timed_laser_status()

        self.assertFalse(ship_mock.laser_ready)
        self.assertEqual(ship_mock.last_laser_usage, mock_time.return_value)

    def test_update_laser_status(self):
        """Test the update_laser_status method."""
        # Case when the timed laser is used.
        self.game.settings.game_modes.game_mode = ["timed_laser_mode"]
        self.game.settings.timed_laser_modes = ["timed_laser_mode"]

        self.weapons_manager.update_timed_laser_status = MagicMock()
        self.weapons_manager.update_normal_laser_status = MagicMock()

        self.weapons_manager.update_laser_status()

        self.weapons_manager.update_timed_laser_status.assert_called_once()
        self.weapons_manager.update_normal_laser_status.assert_not_called()

        # Case when the normal laser is used.
        self.game.settings.game_modes.game_mode = ["normal"]
        self.game.settings.game_modes.last_bullet = False

        self.weapons_manager.update_timed_laser_status.reset_mock()
        self.weapons_manager.update_normal_laser_status.reset_mock()

        self.weapons_manager.update_laser_status()

        self.weapons_manager.update_timed_laser_status.assert_not_called()
        self.weapons_manager.update_normal_laser_status.assert_called_once()

    @patch("pygame.time.get_ticks")
    @patch("src.managers.player_managers.weapons_manager.display_custom_message")
    def test_check_laser_availability_laser_ready_cosmic_conflict(
        self, mock_display_laser, mock_get_ticks
    ):
        """Test the check_laser_availability method when in cosmic conflict."""
        # Mock the necessary attributes and methods
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        mock_get_ticks.return_value = 2500
        self.weapons_manager.draw_laser_message = True
        self.weapons_manager.display_time = 500
        self.game.settings.game_modes.cosmic_conflict = True
        ship_mock.laser_ready = True
        ship_mock.laser_fired = False

        self.weapons_manager.check_laser_availability()

        mock_display_laser.assert_called_once_with(
            self.game.screen, "Ready!", ship_mock, cosmic=True
        )
        self.assertFalse(self.weapons_manager.draw_laser_message)
        self.assertEqual(self.weapons_manager.display_time, mock_get_ticks.return_value)

    @patch("pygame.time.get_ticks")
    @patch("src.managers.player_managers.weapons_manager.display_custom_message")
    def test_check_laser_availability_laser_not_ready(
        self, mock_display_laser, mock_get_ticks
    ):
        """Test the check_laser availability when the laser is not ready"""
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        mock_get_ticks.return_value = 2500
        self.weapons_manager.draw_laser_message = True
        self.weapons_manager.display_time = 500
        self.game.settings.game_modes.cosmic_conflict = False
        self.game.settings.game_modes.last_bullet = False
        ship_mock.laser_ready = False
        ship_mock.laser_fired = True

        self.weapons_manager.check_laser_availability()

        mock_display_laser.assert_called_once_with(
            self.game.screen, "Not Ready!", ship_mock
        )
        self.assertFalse(self.weapons_manager.draw_laser_message)
        self.assertEqual(self.weapons_manager.display_time, mock_get_ticks.return_value)

    @patch("pygame.time.get_ticks")
    @patch("src.managers.player_managers.weapons_manager.display_custom_message")
    def test_check_laser_availability_laser_not_ready_last_bullet(
        self, mock_display_laser, mock_get_ticks
    ):
        """Test the check_laser availability when the laser is not ready in the
        last bullet game mode.
        """
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        mock_get_ticks.return_value = 2500
        self.weapons_manager.draw_laser_message = True
        self.weapons_manager.display_time = 500
        self.game.settings.game_modes.cosmic_conflict = False
        self.game.settings.game_modes.last_bullet = True
        ship_mock.laser_ready = False
        ship_mock.laser_fired = True

        self.weapons_manager.check_laser_availability()

        mock_display_laser.assert_called_once_with(
            self.game.screen, "Not available!", ship_mock
        )
        self.assertFalse(self.weapons_manager.draw_laser_message)
        self.assertEqual(self.weapons_manager.display_time, mock_get_ticks.return_value)

    @patch("pygame.time.get_ticks")
    @patch("src.managers.player_managers.weapons_manager.display_custom_message")
    def test_check_laser_availability_laser_not_ready_cosmic(
        self, mock_display_laser, mock_get_ticks
    ):
        """Test the check_laser availability when the laser is not ready in the
        cosmic_conflict game mode.
        """
        ship_mock = MagicMock()
        self.game.ships = [ship_mock]
        mock_get_ticks.return_value = 2500
        self.weapons_manager.draw_laser_message = True
        self.weapons_manager.display_time = 500
        self.game.settings.game_modes.cosmic_conflict = True
        self.game.settings.game_modes.last_bullet = False
        ship_mock.laser_ready = False
        ship_mock.laser_fired = True

        self.weapons_manager.check_laser_availability()

        mock_display_laser.assert_called_once_with(
            self.game.screen, "Not Ready!", ship_mock, cosmic=True
        )
        self.assertFalse(self.weapons_manager.draw_laser_message)
        self.assertEqual(self.weapons_manager.display_time, mock_get_ticks.return_value)


if __name__ == "__main__":
    unittest.main()
