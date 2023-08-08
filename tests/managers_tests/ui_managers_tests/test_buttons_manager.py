"""
This module tests the GameButtonsManager that is used to manage
the buttons in the game.
"""

import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.utils.constants import GAME_MODES_DESCRIPTIONS, DIFFICULTIES
from src.managers.ui_managers.buttons_manager import GameButtonsManager


class GameButtonsManagerTest(unittest.TestCase):
    """Test cases for the GameButtonsManager."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.game.screen = MagicMock(spec=pygame.Surface)
        self.game.screen.get_rect.return_value = pygame.Rect(0, 0, 800, 600)

        self.manager = GameButtonsManager(
            self.game,
            self.game.screen,
            self.game.ui_options,
            self.game.gm_options,
        )

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.manager.screen, self.game.screen)
        self.assertEqual(self.manager.settings, self.game.settings)
        self.assertEqual(self.manager.ui_options, self.game.ui_options)
        self.assertEqual(self.manager.gm_options, self.game.gm_options)
        self.assertIsNotNone(self.manager.button_imgs)
        self.assertIsNotNone(self.manager.game_buttons)
        self.assertIsNotNone(self.manager.difficulty_buttons)
        self.assertIsNotNone(self.manager.game_mode_buttons)

    @patch("src.managers.ui_managers.buttons_manager.Button")
    def test__create_game_buttons(self, mock_button):
        """Test the create_game_buttons method."""
        # Assert that all buttons were created successfully.
        self.assertEqual(len(self.manager.game_buttons), 8)
        self.assertEqual(len(self.manager.difficulty_buttons), 3)
        self.assertEqual(len(self.manager.game_mode_buttons), 8)

        self.manager._create_game_buttons()
        expected_calls = [
            call(
                self.manager,
                self.manager.button_imgs["play_button"],
                (0, 0),
                center=True,
            ),
            call(
                self.manager,
                self.manager.button_imgs["load_game"],
                (self.manager.play.rect.centerx - 74, self.manager.play.rect.bottom),
            ),
            call(
                self.manager,
                self.manager.button_imgs["select_ship"],
                (
                    self.manager.load_game.rect.centerx - 74,
                    self.manager.load_game.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["difficulty"],
                (
                    self.manager.select_ship.rect.centerx - 74,
                    self.manager.select_ship.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["easy"],
                (
                    self.manager.difficulty.rect.right - 10,
                    self.manager.difficulty.rect.y,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["medium"],
                (self.manager.easy.rect.right - 5, self.manager.easy.rect.y),
            ),
            call(
                self.manager,
                self.manager.button_imgs["hard"],
                (self.manager.medium.rect.right - 5, self.manager.medium.rect.y),
            ),
            call(
                self.manager,
                self.manager.button_imgs["game_modes"],
                (
                    self.manager.difficulty.rect.centerx - 74,
                    self.manager.difficulty.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["normal"],
                (
                    self.manager.game_modes.rect.right - 8,
                    self.manager.game_modes.rect.y,
                ),
                GAME_MODES_DESCRIPTIONS[0],
            ),
            call(
                self.manager,
                self.manager.button_imgs["endless"],
                (self.manager.normal.rect.right - 5, self.manager.normal.rect.y),
                GAME_MODES_DESCRIPTIONS[1],
            ),
            call(
                self.manager,
                self.manager.button_imgs["slow_burn"],
                (self.manager.endless.rect.right - 5, self.manager.endless.rect.y),
                GAME_MODES_DESCRIPTIONS[2],
            ),
            call(
                self.manager,
                self.manager.button_imgs["meteor_madness"],
                (self.manager.normal.rect.left, self.manager.slow_burn.rect.bottom),
                GAME_MODES_DESCRIPTIONS[3],
            ),
            call(
                self.manager,
                self.manager.button_imgs["boss_rush"],
                (
                    self.manager.meteor_madness.rect.right - 5,
                    self.manager.meteor_madness.rect.y,
                ),
                GAME_MODES_DESCRIPTIONS[4],
            ),
            call(
                self.manager,
                self.manager.button_imgs["last_bullet"],
                (self.manager.boss_rush.rect.right - 5, self.manager.boss_rush.rect.y),
                GAME_MODES_DESCRIPTIONS[5],
            ),
            call(
                self.manager,
                self.manager.button_imgs["cosmic_conflict"],
                (self.manager.slow_burn.rect.right - 5, self.manager.slow_burn.rect.y),
                GAME_MODES_DESCRIPTIONS[6],
            ),
            call(
                self.manager,
                self.manager.button_imgs["one_life_reign"],
                (
                    self.manager.last_bullet.rect.right - 5,
                    self.manager.last_bullet.rect.y,
                ),
                GAME_MODES_DESCRIPTIONS[7],
            ),
            call(
                self.manager,
                self.manager.button_imgs["high_scores"],
                (
                    self.manager.game_modes.rect.centerx - 74,
                    self.manager.game_modes.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["delete_scores"],
                (
                    self.manager.high_scores.rect.left - 85,
                    self.manager.high_scores.rect.y,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["menu_button"],
                (
                    self.manager.high_scores.rect.centerx - 74,
                    self.manager.high_scores.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["quit_button"],
                (
                    self.manager.menu.rect.centerx - 74,
                    self.manager.menu.rect.bottom,
                ),
            ),
        ]

        self.assertEqual(mock_button.call_args_list, expected_calls)

    @patch("src.managers.ui_managers.buttons_manager.Button")
    def test__create_menu_buttons(self, mock_button):
        """Test the create_menu_buttons method."""
        self.manager._create_menu_buttons()

        expected_calls = [
            call(
                self.manager,
                self.manager.button_imgs["single_player"],
                (0, 0),
                center=False,
                menu_button=True,
            ),
            call(
                self.manager,
                self.manager.button_imgs["multiplayer"],
                (
                    self.manager.single.rect.centerx - 100,
                    self.manager.single.rect.bottom,
                ),
            ),
            call(
                self.manager,
                self.manager.button_imgs["menu_quit_button"],
                (self.manager.multi.rect.centerx - 100, self.manager.multi.rect.bottom),
            ),
        ]

        self.assertEqual(mock_button.call_args_list, expected_calls)

    @patch("pygame.mouse.get_pos")
    def test_display_description(self, _):
        """Test the display_description method."""
        button = MagicMock()

        self.manager.game_mode_buttons = [button]  # type: ignore

        self.manager.display_description()

        button.show_button_info.assert_called_once()

    def test_draw_difficulty_buttons(self):
        """Test the drawing of the difficulty buttons."""
        button1 = MagicMock()
        button2 = MagicMock()
        button3 = MagicMock()

        self.manager.difficulty_buttons = [button1, button2, button3]  # type: ignore

        self.manager.draw_difficulty_buttons()

        # Assert that the draw_button method is called for each button
        button1.draw_button.assert_called_once()
        button2.draw_button.assert_called_once()
        button3.draw_button.assert_called_once()

    def test_draw_game_mode_buttons(self):
        """Test the draw_game_mode_buttons method."""
        button1 = MagicMock()
        button2 = MagicMock()
        button3 = MagicMock()

        self.manager.game_mode_buttons = [button1, button2, button3]  # type: ignore

        # Mock the display_description method
        with patch.object(
            self.manager, "display_description"
        ) as mock_display_description:
            self.manager.draw_game_mode_buttons()

            # Assert that the draw_button method is called for each button
            button1.draw_button.assert_called_once()
            button2.draw_button.assert_called_once()
            button3.draw_button.assert_called_once()

            mock_display_description.assert_called_once()

    def test_draw_buttons(self):
        """Test the draw_buttons method."""
        button1 = MagicMock()
        button2 = MagicMock()

        self.manager.game_buttons = [button1, button2]  # type: ignore

        self.manager.draw_buttons()

        # Assert that the draw_button method is called for each button
        button1.draw_button.assert_called_once()
        button2.draw_button.assert_called_once()

    def test_handle_buttons_visibility(self):
        """Test the handle_buttons_visibility method."""
        # Test when show_difficulty is True
        self.game.ui_options.show_difficulty = True
        for button in self.manager.difficulty_buttons:
            button.visible = True

        self.manager.handle_buttons_visibility()

        for button in self.manager.difficulty_buttons:
            self.assertFalse(button.visible)
        self.assertFalse(self.manager.delete_scores.visible)

        # Test when show_game_modes is True
        for button in self.manager.game_mode_buttons:
            button.visible = True

        self.game.ui_options.show_game_modes = True

        self.manager.handle_buttons_visibility()

        for button in self.manager.game_mode_buttons:
            self.assertFalse(button.visible)
        self.assertFalse(self.manager.delete_scores.visible)

    def test_handle_play_button(self):
        """Test the handle_play_button method."""
        reset_game_mock = MagicMock()
        self.game.ui_options.show_difficulty = True
        self.game.ui_options.show_high_scores = True
        self.game.ui_options.show_game_modes = True

        self.manager.handle_play_button(reset_game_mock)

        reset_game_mock.assert_called_once()
        self.assertFalse(self.game.ui_options.show_difficulty)
        self.assertFalse(self.game.ui_options.show_high_scores)
        self.assertFalse(self.game.ui_options.show_game_modes)

    @patch("src.managers.ui_managers.buttons_manager.pygame")
    @patch("src.managers.ui_managers.buttons_manager.sys")
    def test_handle_quit_button(self, mock_sys, mock_pygame):
        """Test the handle_quit_button mthod."""
        sound_mock = MagicMock()
        self.game.sound_manager.game_sounds = {"quit_effect": sound_mock}

        self.manager.handle_quit_button()

        sound_mock.play.assert_called_once()
        mock_pygame.quit.assert_called_once()
        mock_sys.exit.assert_called_once()
        mock_pygame.time.delay.assert_called_once_with(800)

    def test_handle_high_scores_button(self):
        """Test the handle_high_scores_button method."""
        # Toggle show_high_scores from False to True
        self.game.ui_options.show_high_scores = False
        self.manager.handle_high_scores_button()
        self.assertTrue(self.game.ui_options.show_high_scores)

        # Toggle show_high_scores from True to False
        self.game.ui_options.show_high_scores = True
        self.manager.handle_high_scores_button()
        self.assertFalse(self.game.ui_options.show_high_scores)

    def test_handle_game_modes_button(self):
        """Test the handle_game_modes_button method."""
        # Toggle show_game_modes from False to True
        self.game.ui_options.show_game_modes = False
        self.manager.handle_game_modes_button()
        self.assertTrue(self.game.ui_options.show_game_modes)

        # Toggle show_game_modes from True to False
        self.game.ui_options.show_game_modes = True
        self.manager.handle_game_modes_button()
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_load_game_button(self):
        """Test the handle_load_game_button."""
        self.manager.handle_load_game_button()

        self.game.save_load_manager.handle_save_load_menu.assert_called_once()

    def test_set_game_mode_settings(self):
        """Test the set_game_mode_settings method."""
        # Set up initial state
        self.game.gm_options.endless_onslaught = True
        self.game.gm_options.slow_burn = True
        self.game.gm_options.meteor_madness = True

        self.set_game_mode_settings_helper(None)
        self.set_game_mode_settings_helper("boss_rush")
        self.assertTrue(self.game.gm_options.boss_rush)

        self.set_game_mode_settings_helper("one_life_reign")
        self.assertTrue(self.game.gm_options.one_life_reign)

    def set_game_mode_settings_helper(self, arg0):
        """Helper function used to test for different game moders."""
        self.manager._set_game_mode_settings(arg0)
        self.assertFalse(self.game.gm_options.endless_onslaught)
        self.assertFalse(self.game.gm_options.slow_burn)
        self.assertFalse(self.game.gm_options.meteor_madness)

    def test_handle_normal_button(self):
        """Test the handle_normal_button method."""
        # Set up initial state
        self.game.gm_options.game_mode = "endless_onslaught"
        self.game.ui_options.show_game_modes = True

        self.manager.handle_normal_button()

        # Assert updated state
        self.assertEqual(self.game.gm_options.game_mode, "normal")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_endless_button(self):
        """Test the handle_endless_button method."""
        # Set up initial state
        self.game.gm_options.endless_onslaught = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_endless_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.endless_onslaught)
        self.assertEqual(self.game.gm_options.game_mode, "endless_onslaught")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_slow_burn_button(self):
        """Test the handle_slow_buton_button method."""
        # Set up initial state
        self.game.gm_options.slow_burn = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_slow_burn_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.slow_burn)
        self.assertEqual(self.game.gm_options.game_mode, "slow_burn")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_meteor_madness_button(self):
        """Test the handle_meteor_madness_button method."""
        # Set up initial state.
        self.game.gm_options.meteor_madness = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_meteor_madness_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.meteor_madness)
        self.assertEqual(self.game.gm_options.game_mode, "meteor_madness")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_boss_rush_button(self):
        """Test the handle_boss_rush_button method."""
        # Set up initial state
        self.game.gm_options.boss_rush = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_boss_rush_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.boss_rush)
        self.assertEqual(self.game.gm_options.game_mode, "boss_rush")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_last_bullet_button(self):
        """Test the handle_last_bullet_button method."""
        # Set up initial state
        self.game.gm_options.last_bullet = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_last_bullet_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.last_bullet)
        self.assertEqual(self.game.gm_options.game_mode, "last_bullet")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_one_life_reign_button(self):
        """Test the handle_one_life_reigh_button method."""
        # Set up initial state
        self.game.gm_options.one_life_reign = False
        self.game.gm_options.game_mode = "normal"

        self.manager.handle_one_life_reign_button()

        # Assert updated state
        self.assertTrue(self.game.gm_options.one_life_reign)
        self.assertEqual(self.game.gm_options.game_mode, "one_life_reign")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_cosmic_conflict_button(self):
        """Test the handle_cosmic_conflict_button method in multiplayer."""
        # Set up initial state
        self.game.gm_options.cosmic_conflict = False
        self.game.singleplayer = False

        # Set ship states to not alive
        for ship in self.game.ships:
            ship.state.alive = False

        self.manager.handle_cosmic_conflict_button()

        # Assert updated state
        for ship in self.game.ships:
            self.assertTrue(ship.state.alive)

        self.assertTrue(self.game.gm_options.cosmic_conflict)
        self.assertEqual(self.game.gm_options.game_mode, "cosmic_conflict")
        self.assertFalse(self.game.ui_options.show_game_modes)

    def test_handle_cosmic_conflict_button_single(self):
        """Test the handle_cosmic_conflict_button method in singleplayer."""
        self.game.gm_options.cosmic_conflict = False
        self.game.singleplayer = True
        self.manager._set_game_mode_settings = MagicMock()

        self.manager.handle_cosmic_conflict_button()

        self.assertFalse(self.game.gm_options.cosmic_conflict)
        self.manager._set_game_mode_settings.assert_not_called()

    def test_handle_difficulty_button(self):
        """Test the handle_difficulty_button method."""
        # Set up initial state
        speedup_scale = 1.5
        max_alien_speed = 10
        self.game.settings.speedup_scale = 1.0
        self.game.settings.max_alien_speed = 5
        self.game.ui_options.show_difficulty = True

        handle_function = self.manager.handle_difficulty_button(
            speedup_scale, max_alien_speed
        )

        handle_function()

        # Assert updated state
        self.assertEqual(self.game.settings.speedup_scale, speedup_scale)
        self.assertEqual(self.game.settings.max_alien_speed, max_alien_speed)
        self.assertFalse(self.game.ui_options.show_difficulty)

    def test_handle_difficulty_toggle(self):
        """Test the handle_difficulty_toggle method."""
        # Toggle show_difficulty from False to True
        self.game.ui_options.show_difficulty = False
        self.manager.handle_difficulty_toggle()
        self.assertTrue(self.game.ui_options.show_difficulty)

        # Toggle show_difficulty from True to False
        self.game.ui_options.show_difficulty = True
        self.manager.handle_difficulty_toggle()
        self.assertFalse(self.game.ui_options.show_difficulty)

    def test_handle_delete_button(self):
        """Test the handle_delete_button method."""
        # Endless Onslaught game mode
        self.game.settings.game_modes.game_mode = "endless_onslaught"
        self.game.ui_options.show_high_scores = True

        self.manager.handle_delete_button()

        # Assert updated state
        self.game.high_score_manager.delete_high_scores.assert_called_once_with(
            "endless_scores"
        )
        self.assertFalse(self.game.ui_options.show_high_scores)

        # Normal game mode
        self.game.high_score_manager.delete_high_scores.reset_mock()
        self.game.settings.game_modes.game_mode = "normal"

        self.manager.handle_delete_button()
        self.game.high_score_manager.delete_high_scores.assert_called_once_with(
            "high_scores"
        )

    def test_create_button_actions_dict(self):
        """Test the create_button_actions_dict method."""
        # Set up initial state
        reset_game = MagicMock()
        menu_method = MagicMock()

        # Call the method to create the dictionary
        actions_dict = self.manager.create_button_actions_dict(menu_method, reset_game)
        self.assertEqual(len(actions_dict), 20)

        # Assert button-action mappings
        self.assertEqual(
            actions_dict[self.manager.play](),
            self.manager.handle_play_button(reset_game),
        )
        self.assertEqual(actions_dict[self.manager.menu], menu_method)
        self.assertEqual(
            actions_dict[self.manager.quit], self.manager.handle_quit_button
        )
        self.assertEqual(
            actions_dict[self.manager.high_scores],
            self.manager.handle_high_scores_button,
        )
        self.assertEqual(
            actions_dict[self.manager.game_modes], self.manager.handle_game_modes_button
        )
        self.assertEqual(
            actions_dict[self.manager.endless], self.manager.handle_endless_button
        )
        self.assertEqual(
            actions_dict[self.manager.meteor_madness],
            self.manager.handle_meteor_madness_button,
        )
        self.assertEqual(
            actions_dict[self.manager.boss_rush], self.manager.handle_boss_rush_button
        )
        self.assertEqual(
            actions_dict[self.manager.last_bullet],
            self.manager.handle_last_bullet_button,
        )
        self.assertEqual(
            actions_dict[self.manager.slow_burn], self.manager.handle_slow_burn_button
        )
        self.assertEqual(
            actions_dict[self.manager.cosmic_conflict],
            self.manager.handle_cosmic_conflict_button,
        )
        self.assertEqual(
            actions_dict[self.manager.one_life_reign],
            self.manager.handle_one_life_reign_button,
        )
        self.assertEqual(
            actions_dict[self.manager.normal], self.manager.handle_normal_button
        )
        self.assertEqual(
            actions_dict[self.manager.easy](),
            self.manager.handle_difficulty_button(
                DIFFICULTIES["EASY"], DIFFICULTIES["MAX_EASY"]
            )(),
        )
        self.assertEqual(
            actions_dict[self.manager.medium](),
            self.manager.handle_difficulty_button(
                DIFFICULTIES["MEDIUM"], DIFFICULTIES["MAX_MEDIUM"]
            )(),
        )
        self.assertEqual(
            actions_dict[self.manager.hard](),
            self.manager.handle_difficulty_button(
                DIFFICULTIES["HARD"], DIFFICULTIES["MAX_HARD"]
            )(),
        )
        self.assertEqual(
            actions_dict[self.manager.difficulty], self.manager.handle_difficulty_toggle
        )
        self.assertEqual(
            actions_dict[self.manager.delete_scores], self.manager.handle_delete_button
        )

    def test_handle_quit_event(self):
        """Test the handle_quit_event method."""
        with self.assertRaises(SystemExit):
            self.manager.handle_quit_event()

    @patch("src.managers.ui_managers.buttons_manager.play_sound")
    def test_handle_single_player_button_click(self, mock_play_sound):
        """Test the handle_single_player_button_click method."""
        start_single = MagicMock()

        self.manager.handle_single_player_button_click(start_single)

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.menu_sounds, "click_menu"
        )
        start_single.assert_called_once()

    @patch("src.managers.ui_managers.buttons_manager.play_sound")
    def test_handle_multiplayer_button_click(self, mock_play_sound):
        """Test the handle multiplayer button click method."""
        start_multi = MagicMock()

        self.manager.handle_multiplayer_button_click(start_multi)

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.menu_sounds, "click_menu"
        )
        start_multi.assert_called_once()

    @patch("src.managers.ui_managers.buttons_manager.play_sound")
    def test_handle_quit_button_click(self, mock_play_sound):
        """Test the handle_quit_button_click method."""
        pygame.time.delay = MagicMock()
        self.manager.handle_quit_event = MagicMock()

        self.manager.handle_quit_button_click()

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.menu_sounds, "quit_effect"
        )
        pygame.time.delay.assert_called_once_with(800)
        self.manager.handle_quit_event.assert_called_once()


if __name__ == "__main__":
    unittest.main()
