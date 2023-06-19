"""
This module tests the Ship class which is the base class for
creating ships in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.entities.ship import Ship
from src.game_logic.game_settings import Settings


class ShipTestCase(unittest.TestCase):
    """Test cases for the Ship class."""

    def setUp(self):
        """Set up the test environment."""
        self.screen = MagicMock()
        self.settings = Settings()
        self.game = MagicMock()
        self.game.settings = self.settings
        self.image = MagicMock()

        with patch("pygame.image.load", return_value=self.image):
            self.ship = Ship(self.game, "ship.png", (400, 300))
        self.ship.ship_type = "thunderbird"

    def test_ship_initialization(self):
        """Test case for the initialization of the ship."""
        self.assertEqual(self.ship.screen, self.game.screen)
        self.assertEqual(self.ship.settings, self.game.settings)
        self.assertEqual(self.ship.game, self.game)
        self.assertEqual(self.ship.screen_rect, self.game.screen.get_rect())
        self.assertEqual(self.ship.image_path, "ship.png")
        self.assertEqual(self.ship.offset, 0)
        self.assertEqual(self.ship.starting_missiles, 3)
        self.assertEqual(self.ship.missiles_num, 0)
        self.assertEqual(self.ship.aliens_killed, self.settings.required_kill_count)
        self.assertEqual(self.ship.remaining_bullets, 17)
        self.assertIsNotNone(self.ship.image)
        self.assertIsNotNone(self.ship.rect)
        self.assertEqual(self.ship.cosmic_conflict_pos, (400, 300))
        self.assertIsNotNone(self.ship.anims)
        self.assertIsNotNone(self.ship.state)
        self.assertEqual(self.ship.immune_start_time, 0)
        self.assertEqual(self.ship.small_ship_time, 0)
        self.assertEqual(self.ship.last_bullet_time, 0)
        self.assertEqual(self.ship.scale_counter, 0)
        self.assertFalse(self.ship.laser_fired)
        self.assertFalse(self.ship.laser_ready)
        self.assertFalse(self.ship.laser_ready_msg)
        self.assertEqual(self.ship.last_laser_time, 0)
        self.assertEqual(self.ship.laser_ready_start_time, 0.0)
        self.assertEqual(self.ship.last_laser_usage, 0.0)
        self.assertIsNotNone(self.ship.ship_type)
        self.assertIsNone(self.ship.last_reverse_power_down_time)
        self.assertIsNone(self.ship.last_disarmed_power_down_time)
        self.assertIsNone(self.ship.last_scaled_weapon_power_down_time)
        self.assertFalse(self.ship.moving_flags["right"])
        self.assertFalse(self.ship.moving_flags["left"])
        self.assertFalse(self.ship.moving_flags["up"])
        self.assertFalse(self.ship.moving_flags["down"])
        self.assertEqual(self.ship.x_pos, float(self.ship.rect.x))
        self.assertEqual(self.ship.y_pos, float(self.ship.rect.y - 10))
        self.assertTrue(self.ship.ship_speed, 3.5)

    def test_ship_speed_setter(self):
        """Test case for the ship speed setter."""
        self.settings.thunderbird_ship_speed = 7
        self.assertEqual(self.ship.ship_speed, 7)

    @patch("src.entities.ship.Ship.reset_ship_size")
    @patch("pygame.time.get_ticks")
    @patch("src.animations.ship_animations.pygame.image.load")
    @patch("src.entities.ship.time.time")
    def test_update_state(
        self, mock_time, mock_load_image, mock_get_ticks, mock_reset_ship_size
    ):
        """Test case for the update_state method."""
        mock_image = MagicMock()
        mock_load_image.return_value = mock_image
        mock_time.return_value = 10
        mock_get_ticks.return_value = 10

        # Set up initial state and values
        self.ship.state.immune = True
        self.ship.settings.immune_time = 0
        self.ship.immune_start_time = 0

        self.ship.state.scaled = True
        self.ship.settings.scaled_time = 0
        self.ship.small_ship_time = 0

        self.ship.state.exploding = True
        self.ship.anims.update_explosion_animation = MagicMock()

        self.ship.state.warping = True
        self.ship.anims.update_warp_animation = MagicMock()

        self.ship.state.shielded = True
        self.ship.anims.update_shield_animation = MagicMock()

        self.ship.state.immune = True
        self.ship.anims.update_immune_animation = MagicMock()

        self.ship.state.empowered = True
        self.ship.anims.update_empower_animation = MagicMock()

        self.ship._update_position = MagicMock()
        self.ship.rect = MagicMock()
        self.ship.x_pos = 200.0
        self.ship.y_pos = 300.0

        self.ship.update_state()

        # Assert state changes
        self.assertFalse(self.ship.state.immune)
        mock_reset_ship_size.assert_called_once()
        self.ship.anims.update_explosion_animation.assert_called_once()
        self.ship.anims.update_shield_animation.assert_called_once()
        self.ship.anims.update_empower_animation.assert_called_once()

        self.assertEqual(self.ship.rect.x, 200)
        self.assertEqual(self.ship.rect.y, 300)

        self.ship.state.exploding = False

        self.ship.update_state()

        self.ship.anims.update_warp_animation.assert_called_once()

        self.ship.state.warping = False

        self.ship.update_state()

        self.ship._update_position.assert_called_once()

        self.ship.state.immune = True
        self.ship.settings.immune_time = 1000

        self.ship.update_state()

        self.ship.anims.update_immune_animation.assert_called_once()

    def test_update_position(self):
        """Test the _update_position method."""
        # Set up initial state and values
        self.ship.state.reverse = False
        self.ship.moving_flags = {
            "right": True,
            "left": False,
            "up": False,
            "down": False,
        }
        self.ship.x_pos = 100.0
        self.ship.y_pos = 200.0
        self.ship.rect.width = 46
        self.ship.rect.height = 48

        self.ship.screen_rect = pygame.Rect(0, 0, 800, 600)

        self._update_position_assert_helper(103.5, 200.0)
        self.settings.thunderbird_ship_speed = 1
        self._update_position_movement_helper(False, 200.0)
        self.settings.thunderbird_ship_speed = 3

        self._update_position_assert_helper(102.5, 197.0)
        # Set up different movement flags and ship speed
        self.ship.moving_flags = {
            "right": False,
            "left": False,
            "up": False,
            "down": True,
        }
        self.settings.thunderbird_ship_speed = 5

        self._update_position_assert_helper(102.5, 202.0)
        self._update_position_movement_helper(True, 202.0)
        self._update_position_assert_helper(107.5, 197.0)
        # Set up movement flags to keep ship within screen boundaries
        self.ship.moving_flags = {
            "right": False,
            "left": True,
            "up": False,
            "down": True,
        }

        self._update_position_assert_helper(102.5, 202.0)

    def _update_position_movement_helper(self, arg0, arg1):
        self.ship.moving_flags = {
            "right": arg0,
            "left": True,
            "up": arg0,
            "down": arg0,
        }
        self._update_position_assert_helper(102.5, arg1)
        # Set up different movement flags and ship speed
        self.ship.moving_flags = {
            "right": arg0,
            "left": False,
            "up": True,
            "down": False,
        }

    def _update_position_assert_helper(self, arg0, arg1):
        # Call the _update_position method
        self.ship._update_position()

        # Assert the updated position
        self.assertEqual(self.ship.x_pos, arg0)
        self.assertEqual(self.ship.y_pos, arg1)

    def test_blitme(self):
        """Test the blitme method."""
        # Create separate MagicMock objects for the surface and rect
        surface_mock = MagicMock()
        # Assign the surface mock to self.screen
        self.ship.screen = surface_mock

        # Set up initial state and values
        self.ship.state.warping = False
        self.ship.state.exploding = False
        self.ship.state.shielded = True
        self.ship.state.immune = True
        self.ship.state.empowered = True

        # Set up the animation and image mocks
        self.ship.anims.warp_frames = [MagicMock()]
        self.ship.anims.warp_index = 0
        self.ship.anims.explosion_image = MagicMock()
        self.ship.anims.explosion_rect = MagicMock()
        self.ship.anims.shield_image = MagicMock()
        self.ship.anims.shield_rect = MagicMock()
        self.ship.anims.immune_image = MagicMock()
        self.ship.anims.immune_rect = MagicMock()
        self.ship.anims.empower_image = MagicMock()
        self.ship.anims.empower_rect = MagicMock()

        self.ship.blitme()

        # Assert the correct blitting calls
        surface_mock.blit.assert_any_call(
            self.ship.anims.shield_image, self.ship.anims.shield_rect
        )
        surface_mock.blit.assert_any_call(
            self.ship.anims.immune_image, self.ship.anims.immune_rect
        )
        surface_mock.blit.assert_any_call(
            self.ship.anims.empower_image, self.ship.anims.empower_rect
        )

        # Reset the blit mock
        surface_mock.blit.reset_mock()

        self.ship.state.exploding = True

        self.ship.blitme()

        surface_mock.blit.assert_any_call(
            self.ship.anims.explosion_image, self.ship.anims.explosion_rect
        )

        self.ship.state.exploding = False
        self.ship.state.warping = True

        self.ship.blitme()

        surface_mock.blit.assert_any_call(
            self.ship.anims.warp_frames[self.ship.anims.warp_index], self.ship.rect
        )

    def test_center_ship_cosmic_conflict_mode(self):
        """Test the center_ship method in cosmic conflict mode."""
        self.ship.settings.game_modes.cosmic_conflict = True

        self.ship.center_ship()

        # Assert the ship's position and rect updates
        self.assertAlmostEqual(self.ship.rect.bottom, self.ship.screen_rect.centery)
        self.assertEqual(self.ship.x_pos, self.ship.cosmic_conflict_pos)
        self.assertAlmostEqual(self.ship.y_pos, float(self.ship.rect.y - 10))

    def test_center_ship_singleplayer_mode(self):
        """Test the center_ship method in singleplayer mode."""
        # Set up the initial state and values
        self.ship.settings.game_modes.cosmic_conflict = False
        self.ship.game.singleplayer = True

        self.ship.center_ship()

        # Assert the ship's position and rect updates
        self.assertEqual(self.ship.rect.bottom, self.ship.screen_rect.bottom)
        self.assertAlmostEqual(self.ship.x_pos, self.ship.screen_rect.centerx)
        self.assertAlmostEqual(self.ship.y_pos, float(self.ship.rect.y - 10))

    def test_center_ship_offset(self):
        """Test the center_ship method with an offset."""
        self.ship.game.singleplayer = False
        self.ship.offset = 50

        self.ship.center_ship()

        # Assert the ship's position and rect updates
        self.assertEqual(self.ship.rect.bottom, self.ship.screen_rect.bottom)
        self.assertAlmostEqual(
            self.ship.x_pos, self.ship.screen_rect.centerx + self.ship.offset
        )
        self.assertAlmostEqual(self.ship.y_pos, float(self.ship.rect.y - 10))

    def test_explode(self):
        """Test the explode method."""
        self.ship.anims.explosion_rect = MagicMock()
        self.ship.rect = MagicMock()

        self.ship.explode()

        self.assertTrue(self.ship.state.exploding)
        self.assertEqual(self.ship.anims.explosion_rect.center, self.ship.rect.center)

    def test_start_warp(self):
        """Test the start_warp method."""
        self.ship.start_warp()
        self.assertTrue(self.ship.state.warping)

    def test_set_immune(self):
        """Test the set_immune method."""
        self.ship.anims.immune_rect = MagicMock()
        self.ship.rect = MagicMock()

        self.ship.set_immune()

        self.assertTrue(self.ship.state.immune)
        self.assertEqual(self.ship.anims.immune_rect.center, self.ship.rect.center)
        self.assertIsNotNone(self.ship.immune_start_time)

    def test_empower(self):
        """Test the empower method."""
        self.ship.empower()
        self.assertTrue(self.ship.state.empowered)

    def test_update_missiles_number_one_life_reign(self):
        """Test the update_missiles_number method in one_life_reign mode."""
        self.ship.settings.game_modes.one_life_reign = True
        self.ship.update_missiles_number()
        self.assertEqual(self.ship.missiles_num, 6)

    def test_update_missiles_number_last_bullet(self):
        """Test the update_missiles_number method in last_bullet mode."""
        self.ship.settings.game_modes.last_bullet = True
        self.ship.update_missiles_number()
        self.assertEqual(self.ship.missiles_num, 1)

    def test_update_missiles_number_default(self):
        """Test the update_missiles_number method with default settings."""
        self.ship.starting_missiles = 8
        self.ship.update_missiles_number()
        self.assertEqual(self.ship.missiles_num, 8)

    def test_scale_ship(self):
        """Test the scale_ship method."""
        self.ship.anims.change_ship_size = MagicMock()
        self.ship.scale_ship(1.5)
        self.ship.anims.change_ship_size.assert_called_once()
        self.assertTrue(self.ship.state.scaled)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_reset_ship_size(self, mock_load_image):
        """Test the reset_ship_size method."""
        self.ship.state.scaled = True
        self.ship.scale_counter = 1

        self.ship.reset_ship_size()

        mock_load_image.assert_called_once()
        self.assertFalse(self.ship.state.scaled)
        self.assertEqual(self.ship.scale_counter, 0)
        self.assertIsNotNone(self.ship.small_ship_time)

    def test_reset_ship_state(self):
        """Test the reset_ship_state method."""
        # Set up the initial state
        self.ship.state.disarmed = True
        self.ship.state.reverse = True
        self.ship.state.scaled_weapon = True
        self.ship.state.shielded = True
        self.ship.state.immune = True
        self.ship.aliens_killed = 10
        self.ship.last_laser_time = 100
        self.ship.laser_fired = True
        self.ship.laser_ready = True
        self.ship.laser_ready_start_time = 200.0
        self.ship.last_laser_usage = 50.0
        self.ship.laser_ready_msg = True

        # Call the reset_ship_state method
        self.ship.reset_ship_state()

        # Assert the ship's state and variables are reset
        self.assertFalse(self.ship.state.disarmed)
        self.assertFalse(self.ship.state.reverse)
        self.assertFalse(self.ship.state.scaled_weapon)
        self.assertFalse(self.ship.state.shielded)
        self.assertFalse(self.ship.state.immune)
        self.assertEqual(
            self.ship.aliens_killed, self.ship.settings.required_kill_count
        )
        self.assertEqual(self.ship.last_laser_time, 0)
        self.assertFalse(self.ship.laser_fired)
        self.assertFalse(self.ship.laser_ready)
        self.assertEqual(self.ship.laser_ready_start_time, 0.0)
        self.assertEqual(self.ship.last_laser_usage, 0.0)
        self.assertFalse(self.ship.laser_ready_msg)

    def test_update_speed_from_settings(self):
        """Test the update_speed_from_settings method."""
        player = "thunderbird"
        setattr(self.ship.settings, f"{player}_ship_speed", 5)
        self.ship.update_speed_from_settings(player)
        self.assertEqual(self.ship.ship_speed, 5)


if __name__ == "__main__":
    unittest.main()
