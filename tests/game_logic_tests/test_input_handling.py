"""
This module tests the PlayerInput class which manages the player
input events in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.game_logic.input_handling import PlayerInput
from src.entities.projectiles.missile import Missile
from src.entities.projectiles.laser import Laser
from src.entities.projectiles.player_bullets import Thunderbolt


class TestPlayerInput(unittest.TestCase):
    """Test cases for the PlayerInput class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.player_input = PlayerInput(self.game, self.game.ui_options)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.player_input.game, self.game)
        self.assertEqual(self.player_input.settings, self.game.settings)
        self.assertEqual(self.player_input.ui_options, self.game.ui_options)
        self.assertEqual(self.player_input.thunderbird, self.game.thunderbird_ship)
        self.assertEqual(self.player_input.phoenix, self.game.phoenix_ship)

    @patch("src.game_logic.input_handling.play_sound")
    @patch("src.game_logic.input_handling.pygame.quit")
    @patch("src.game_logic.input_handling.sys.exit")
    @patch("src.game_logic.input_handling.pygame.time.delay")
    def test_check_keydown_events_quit(
        self, mock_delay, mock_exit, mock_quit, mock_play_sound
    ):
        """Test the Q keypress event."""
        event_mock = MagicMock()
        event_mock.key = pygame.K_q
        self.game.ui_options.paused = True

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_quit.assert_called_once()
        mock_exit.assert_called_once()
        mock_delay.assert_called_once_with(800)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "quit_effect"
        )

    @patch("src.game_logic.input_handling.play_sound")
    def test_check_keydown_events_pause(self, mock_play_sound):
        """Test the P keypress event."""
        self.game.ui_options.paused = False
        event_mock = MagicMock()
        event_mock.key = pygame.K_p

        self.player_input.check_keydown_events(
            event_mock, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        )

        self.assertEqual(self.game.ui_options.paused, True)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "keypress"
        )

    @patch("src.game_logic.input_handling.play_sound")
    def test_check_keydown_events_reset_game(self, mock_play_sound):
        """Test the R keypress event."""
        event_mock = MagicMock()
        event_mock.key = pygame.K_r
        self.game.ui_options.paused = True

        reset_game_mock = MagicMock()

        self.player_input.check_keydown_events(
            event_mock,
            reset_game_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        reset_game_mock.assert_called_once()
        self.assertEqual(self.game.ui_options.paused, False)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "keypress"
        )
        self.assertIsNone(self.game.sound_manager.current_sound)

    @patch("src.game_logic.input_handling.play_music")
    @patch("src.game_logic.input_handling.play_sound")
    def test_check_keydown_events_game_menu(self, mock_play_sound, mock_play_music):
        """Test the ESC keypress event."""
        event_mock = MagicMock()
        event_mock.key = pygame.K_ESCAPE
        self.game.ui_options.paused = True

        game_menu_mock = MagicMock()

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            game_menu_mock,
            MagicMock(),
            MagicMock(),
        )

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "keypress"
        )
        mock_play_music.assert_called_once_with(
            self.game.sound_manager.menu_music, "menu"
        )
        self.assertEqual(self.game.sound_manager.current_sound, "menu")
        game_menu_mock.assert_called_once()
        self.assertEqual(self.game.ui_options.paused, False)

    @patch("src.game_logic.input_handling.play_sound")
    def test_check_keydown_events_run_menu(self, mock_play_sound):
        """Test the M keypress event."""
        event_mock = MagicMock()
        event_mock.key = pygame.K_m
        self.game.ui_options.paused = True

        run_menu_mock = MagicMock()

        with patch(
            "src.game_logic.input_handling.pygame.time.delay"
        ) as time_delay_mock:
            self.player_input.check_keydown_events(
                event_mock,
                MagicMock(),
                run_menu_mock,
                MagicMock(),
                MagicMock(),
                MagicMock(),
            )

            time_delay_mock.assert_called_with(300)
            self.assertEqual(self.game.stats.game_active, False)
            run_menu_mock.assert_called_once()
            mock_play_sound.assert_called_once_with(
                self.game.sound_manager.game_sounds, "keypress"
            )

    @patch("src.game_logic.input_handling.play_sound")
    def test_check_keydown_events_save_data(self, mock_play_sound):
        """Test the M keypress event."""
        event_mock = MagicMock()
        event_mock.key = pygame.K_s
        self.game.ui_options.paused = True

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "keypress"
        )

        self.game.save_load_manager.get_current_game_stats.assert_called_once()
        self.game.save_load_manager.handle_save_load_menu.assert_called_once_with(
            save=True
        )
        self.assertFalse(self.game.ui_options.paused)

    def test_check_keydown_events_player_controls(self):
        """Test if the appropriate functions for the player
        controls are called."""
        # Multiplayer and not paused test case
        self.game.singleplayer = False
        self.game.ui_options.paused = False

        event_mock = MagicMock()
        fire_missile_method = MagicMock()
        fire_laser_method = MagicMock()

        self.player_input._handle_thunderbird_controls = MagicMock()
        self.player_input._handle_phoenix_controls = MagicMock()

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            fire_missile_method,
            fire_laser_method,
        )

        self.player_input._handle_thunderbird_controls.assert_called_once_with(
            event_mock, fire_missile_method, fire_laser_method
        )
        self.player_input._handle_phoenix_controls.assert_called_once_with(
            event_mock, fire_missile_method, fire_laser_method
        )

        # Paused test case
        self.player_input._handle_phoenix_controls.reset_mock()
        self.player_input._handle_thunderbird_controls.reset_mock()
        self.game.ui_options.paused = True

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            fire_missile_method,
            fire_laser_method,
        )

        self.player_input._handle_thunderbird_controls.assert_not_called()
        self.player_input._handle_phoenix_controls.assert_not_called()

        # Singleplayer test case
        self.player_input._handle_phoenix_controls.reset_mock()
        self.player_input._handle_thunderbird_controls.reset_mock()
        self.game.ui_options.paused = False
        self.game.singleplayer = True

        self.player_input.check_keydown_events(
            event_mock,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            fire_missile_method,
            fire_laser_method,
        )

        self.player_input._handle_thunderbird_controls.assert_called_once_with(
            event_mock, fire_missile_method, fire_laser_method
        )
        self.player_input._handle_phoenix_controls.assert_not_called()

    def test_check_keyup_events_thunderbird_controls(self):
        """Test the keyup events for the thunderbird controls."""
        self.game.thunderbird_ship.moving_flags = {
            "right": True,
            "left": True,
            "up": True,
            "down": True,
        }
        self.game.singleplayer = True
        self.game.thunderbird_ship.state.firing = True
        self.game.thunderbird_ship.state.laser_fired = True
        self.game.thunderbird_ship.state.alive = True

        event_mock = MagicMock()

        # Simulate releasing different keys
        keys_to_release = [
            pygame.K_d,
            pygame.K_a,
            pygame.K_w,
            pygame.K_s,
            pygame.K_SPACE,
            pygame.K_c,
        ]
        for key in keys_to_release:
            event_mock.key = key
            self.player_input.check_keyup_events(event_mock)

            # Add assertions to verify the corresponding flags/state are updated correctly
            if key == pygame.K_d:
                self.assertFalse(self.game.thunderbird_ship.moving_flags["right"])
            elif key == pygame.K_a:
                self.assertFalse(self.game.thunderbird_ship.moving_flags["left"])
            elif key == pygame.K_w:
                self.assertFalse(self.game.thunderbird_ship.moving_flags["up"])
            elif key == pygame.K_s:
                self.assertFalse(self.game.thunderbird_ship.moving_flags["down"])
            elif key == pygame.K_SPACE:
                self.assertFalse(self.game.thunderbird_ship.state.firing)
            elif key == pygame.K_c:
                self.assertFalse(self.game.thunderbird_ship.laser_fired)

    def test_check_keyup_events_phoenix_controls(self):
        """Test the keyup events for the Phoenix controls."""
        self.game.phoenix_ship.moving_flags = {
            "right": True,
            "left": True,
            "up": True,
            "down": True,
        }

        self.player_input.game.singleplayer = False
        self.game.phoenix_ship.state.alive = True
        self.game.phoenix_ship.state.firing = True
        self.game.phoenix_ship.state.laser_fired = True

        event_mock = MagicMock()

        # Simulate releasing different keys
        keys_to_release = [
            pygame.K_RIGHT,
            pygame.K_LEFT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_RETURN,
            pygame.K_RSHIFT,
        ]
        for key in keys_to_release:
            event_mock.key = key
            self.player_input.check_keyup_events(event_mock)

            # Add assertions to verify the corresponding flags/state are updated correctly
            if key == pygame.K_RIGHT:
                self.assertFalse(self.game.phoenix_ship.moving_flags["right"])
            elif key == pygame.K_LEFT:
                self.assertFalse(self.game.phoenix_ship.moving_flags["left"])
            elif key == pygame.K_UP:
                self.assertFalse(self.game.phoenix_ship.moving_flags["up"])
            elif key == pygame.K_DOWN:
                self.assertFalse(self.game.phoenix_ship.moving_flags["down"])
            elif key == pygame.K_RETURN:
                self.assertFalse(self.game.phoenix_ship.state.firing)
            elif key == pygame.K_RSHIFT:
                self.assertFalse(self.game.phoenix_ship.laser_fired)

    @patch("src.game_logic.input_handling.pygame.time.get_ticks")
    def test_handle_ship_firing(self, mock_get_ticks):
        """Test the handle_ship_firing."""
        fire_bullet_method_mock = MagicMock()
        mock_get_ticks.return_value = 201

        self.game.thunderbird_ship.state.firing = True
        self.game.thunderbird_ship.last_bullet_time = 0

        self.game.phoenix_ship.state.firing = False
        self.game.phoenix_ship.last_bullet_time = 0

        # Test case when one ship is firing a bullet and the other is not.
        self.player_input.handle_ship_firing(fire_bullet_method_mock)

        # Assertions for Thunderbird ship firing
        fire_bullet_method_mock.assert_called_once_with(
            self.player_input.game.thunderbird_bullets,
            self.player_input.game.settings.thunderbird_bullets_allowed,
            bullet_class=Thunderbolt,
            num_bullets=self.player_input.game.settings.thunderbird_bullet_count,
            ship=self.game.thunderbird_ship,
        )

        self.assertEqual(
            self.game.thunderbird_ship.last_bullet_time, mock_get_ticks.return_value
        )
        self.assertEqual(self.game.phoenix_ship.last_bullet_time, 0)

        # Test case when one ship is not firing and the other ship
        # tries to fire too fast.
        fire_bullet_method_mock.reset_mock()
        mock_get_ticks.return_value = 300
        self.game.thunderbird_ship.state.firing = True
        self.game.thunderbird_ship.last_bullet_time = 200

        self.game.phoenix_ship.state.firing = False
        self.game.phoenix_ship.last_bullet_time = 0

        self.player_input.handle_ship_firing(fire_bullet_method_mock)

        fire_bullet_method_mock.assert_not_called()

    def test_handle_thunderbird_controls(self):
        """Test the handle_thunderbird_controls."""
        self.game.thunderbird_ship.moving_flags = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }
        event_mock = MagicMock()
        fire_missile_method_mock = MagicMock()
        fire_laser_method_mock = MagicMock()

        self.game.thunderbird_ship.state.alive = True
        self.game.thunderbird_ship.state.warping = False
        self.game.thunderbird_ship.state.exploding = False
        self.game.thunderbird_ship.state.firing = False
        self.game.thunderbird_ship.laser_firing = False

        # Simulate different keypresses
        keys_to_press = [
            pygame.K_SPACE,
            pygame.K_d,
            pygame.K_a,
            pygame.K_w,
            pygame.K_s,
            pygame.K_x,
            pygame.K_c,
        ]
        for key in keys_to_press:
            event_mock.key = key
            self.player_input._handle_thunderbird_controls(
                event_mock, fire_missile_method_mock, fire_laser_method_mock
            )

        # Assertions
        self.assertTrue(self.game.thunderbird_ship.state.firing)
        self.assertTrue(self.game.thunderbird_ship.moving_flags["right"])
        self.assertTrue(self.game.thunderbird_ship.moving_flags["left"])
        self.assertTrue(self.game.thunderbird_ship.moving_flags["up"])
        self.assertTrue(self.game.thunderbird_ship.moving_flags["down"])

        fire_missile_method_mock.assert_called_once_with(
            self.player_input.game.thunderbird_missiles,
            self.game.thunderbird_ship,
            missile_class=Missile,
        )
        fire_laser_method_mock.assert_called_once_with(
            self.player_input.game.thunderbird_laser,
            self.game.thunderbird_ship,
            laser_class=Laser,
        )
        self.assertTrue(self.game.thunderbird_ship.laser_fired)

    def test_handle_phoenix_controls(self):
        """Test the handle_phoenix_controls method."""
        self.game.phoenix_ship.moving_flags = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }
        event_mock = MagicMock()
        fire_missile_method_mock = MagicMock()
        fire_laser_method_mock = MagicMock()

        self.game.phoenix_ship.state.alive = True
        self.game.phoenix_ship.state.warping = False
        self.game.phoenix_ship.state.exploding = False
        self.game.phoenix_ship.state.firing = False
        self.game.phoenix_ship.laser_firing = False

        keys_to_press = [
            pygame.K_RETURN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_RCTRL,
            pygame.K_RSHIFT,
        ]
        for key in keys_to_press:
            event_mock.key = key
            self.player_input._handle_phoenix_controls(
                event_mock, fire_missile_method_mock, fire_laser_method_mock
            )

        # Assertions
        self.assertTrue(self.game.phoenix_ship.state.firing)
        self.assertTrue(self.game.phoenix_ship.moving_flags["right"])
        self.assertTrue(self.game.phoenix_ship.moving_flags["left"])
        self.assertTrue(self.game.phoenix_ship.moving_flags["up"])
        self.assertTrue(self.game.phoenix_ship.moving_flags["down"])

        fire_missile_method_mock.assert_called_once_with(
            self.player_input.game.phoenix_missiles,
            self.game.phoenix_ship,
            missile_class=Missile,
        )
        fire_laser_method_mock.assert_called_once_with(
            self.player_input.game.phoenix_laser,
            self.game.phoenix_ship,
            laser_class=Laser,
        )

        self.assertTrue(self.game.phoenix_ship.laser_fired)

    def test_reset_ship_flags(self):
        """Test the reset_ship_flags method."""
        self.game.thunderbird_ship.moving_flags = {
            "right": True,
            "left": True,
            "up": True,
            "down": True,
        }
        self.game.phoenix_ship.moving_flags = {
            "right": True,
            "left": True,
            "up": True,
            "down": True,
        }
        self.game.thunderbird_ship.state.firing = True
        self.game.phoenix_ship.state.firing = True

        self.player_input.reset_ship_flags()

        self.assertFalse(self.game.thunderbird_ship.moving_flags["right"])
        self.assertFalse(self.game.thunderbird_ship.moving_flags["left"])
        self.assertFalse(self.game.thunderbird_ship.moving_flags["up"])
        self.assertFalse(self.game.thunderbird_ship.moving_flags["down"])
        self.assertFalse(self.game.phoenix_ship.moving_flags["right"])
        self.assertFalse(self.game.phoenix_ship.moving_flags["left"])
        self.assertFalse(self.game.phoenix_ship.moving_flags["up"])
        self.assertFalse(self.game.phoenix_ship.moving_flags["down"])
        self.assertFalse(self.game.phoenix_ship.state.firing)
        self.assertFalse(self.game.thunderbird_ship.state.firing)


if __name__ == "__main__":
    unittest.main()
