"""
This module tests the ScreenManager class which manages screen behaviors
in the game.
"""

import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.managers.ui_managers.screen_manager import ScreenManager


class TestScreenManager(unittest.TestCase):
    """Test cases for the ScreenManager class."""

    def setUp(self):
        """Set up test environment."""
        with patch("src.managers.ui_managers.screen_manager.display_controls"), patch(
            "pygame.mouse"
        ), patch(
            "src.managers.ui_managers.screen_manager.ScreenManager.create_controls"
        ):
            self.game = MagicMock()
            self.settings = MagicMock()
            self.score_board = MagicMock()
            self.buttons_manager = MagicMock()
            self.screen = MagicMock()
            self.screen.get_size.return_value = (800, 600)
            self.singleplayer = MagicMock()
            self.screen_manager = ScreenManager(
                self.game,
                self.settings,
                self.score_board,
                self.buttons_manager,
                self.screen,
                self.singleplayer,
            )

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.screen_manager.game, self.game)
        self.assertEqual(self.screen_manager.settings, self.settings)
        self.assertEqual(self.screen_manager.buttons, self.buttons_manager)
        self.assertEqual(self.screen_manager.screen, self.screen)
        self.assertIsNotNone(self.screen_manager.player_controls)
        self.assertEqual(self.screen_manager.screen_flag, pygame.RESIZABLE)
        self.assertFalse(self.screen_manager.full_screen)
        self.assertEqual(self.screen_manager.singleplayer, self.singleplayer)
        self.assertIsNotNone(self.screen_manager.cursor_surface)

    def test_update_buttons(self):
        """Test the update_buttons method."""
        self.screen_manager.update_buttons()

        # Assert the expected position updates of the buttons
        self.screen_manager.buttons.play.update_pos.assert_called_once_with(
            self.screen.get_rect().center, y=-115
        )
        self.screen_manager.buttons.load_game.update_pos.assert_called_once_with(
            self.screen_manager.buttons.play.rect.centerx - 74,
            self.screen_manager.buttons.play.rect.bottom,
        )
        self.screen_manager.buttons.select_ship.update_pos.assert_called_once_with(
            self.screen_manager.buttons.load_game.rect.centerx - 74,
            self.screen_manager.buttons.load_game.rect.bottom,
        )
        self.screen_manager.buttons.difficulty.update_pos.assert_called_once_with(
            self.screen_manager.buttons.select_ship.rect.centerx - 74,
            self.screen_manager.buttons.select_ship.rect.bottom,
        )
        self.screen_manager.buttons.game_modes.update_pos.assert_called_once_with(
            self.screen_manager.buttons.difficulty.rect.centerx - 74,
            self.screen_manager.buttons.difficulty.rect.bottom,
        )
        self.screen_manager.buttons.high_scores.update_pos.assert_called_once_with(
            self.screen_manager.buttons.game_modes.rect.centerx - 74,
            self.screen_manager.buttons.game_modes.rect.bottom,
        )
        self.screen_manager.buttons.delete_scores.update_pos.assert_called_once_with(
            self.screen_manager.buttons.high_scores.rect.left - 85,
            self.screen_manager.buttons.high_scores.rect.y,
        )
        self.screen_manager.buttons.menu.update_pos.assert_called_once_with(
            self.screen_manager.buttons.high_scores.rect.centerx - 74,
            self.screen_manager.buttons.high_scores.rect.bottom,
        )
        self.screen_manager.buttons.quit.update_pos.assert_called_once_with(
            self.screen_manager.buttons.menu.rect.centerx - 74,
            self.screen_manager.buttons.menu.rect.bottom,
        )
        self.screen_manager.buttons.easy.update_pos.assert_called_once_with(
            self.screen_manager.buttons.difficulty.rect.right - 10,
            self.screen_manager.buttons.difficulty.rect.y,
        )
        self.screen_manager.buttons.medium.update_pos.assert_called_once_with(
            self.screen_manager.buttons.easy.rect.right - 5,
            self.screen_manager.buttons.difficulty.rect.y,
        )
        self.screen_manager.buttons.hard.update_pos.assert_called_once_with(
            self.screen_manager.buttons.medium.rect.right - 5,
            self.screen_manager.buttons.difficulty.rect.y,
        )
        self.screen_manager.buttons.normal.update_pos.assert_called_once_with(
            self.screen_manager.buttons.game_modes.rect.right - 8,
            self.screen_manager.buttons.game_modes.rect.y,
        )
        self.screen_manager.buttons.endless.update_pos.assert_called_once_with(
            self.screen_manager.buttons.normal.rect.right - 5,
            self.screen_manager.buttons.normal.rect.y,
        )
        self.screen_manager.buttons.slow_burn.update_pos.assert_called_once_with(
            self.screen_manager.buttons.endless.rect.right - 5,
            self.screen_manager.buttons.endless.rect.y,
        )
        self.screen_manager.buttons.cosmic_conflict.update_pos.assert_called_once_with(
            self.screen_manager.buttons.slow_burn.rect.right - 5,
            self.screen_manager.buttons.slow_burn.rect.y,
        )
        self.screen_manager.buttons.meteor_madness.update_pos.assert_called_once_with(
            self.screen_manager.buttons.normal.rect.left,
            self.screen_manager.buttons.slow_burn.rect.bottom,
        )
        self.screen_manager.buttons.boss_rush.update_pos.assert_called_once_with(
            self.screen_manager.buttons.meteor_madness.rect.right - 5,
            self.screen_manager.buttons.meteor_madness.rect.y,
        )
        self.screen_manager.buttons.last_bullet.update_pos.assert_called_once_with(
            self.screen_manager.buttons.boss_rush.rect.right - 5,
            self.screen_manager.buttons.boss_rush.rect.y,
        )
        self.screen_manager.buttons.one_life_reign.update_pos.assert_called_once_with(
            self.screen_manager.buttons.last_bullet.rect.right - 5,
            self.screen_manager.buttons.last_bullet.rect.y,
        )

        # Update Menu Buttons
        self.screen_manager.buttons.single.update_pos.assert_called_once_with(
            self.screen.get_rect().center, y=-80
        )
        self.screen_manager.buttons.multi.update_pos.assert_called_once_with(
            self.screen_manager.buttons.single.rect.centerx - 100,
            self.screen_manager.buttons.single.rect.bottom,
        )
        self.screen_manager.buttons.menu_quit.update_pos.assert_called_once_with(
            self.screen_manager.buttons.multi.rect.centerx - 100,
            self.screen_manager.buttons.multi.rect.bottom,
        )
        self.screen_manager.settings.game_title_rect.centerx = (
            self.screen.get_rect().centerx
        )

        # Update scoreboard
        self.screen_manager.score_board.prep_level.assert_called_once()
        self.screen_manager.score_board.render_scores.assert_called_once()
        self.screen_manager.score_board.render_missiles_num.assert_called_once()
        self.screen_manager.score_board.render_high_score.assert_called_once()
        self.screen_manager.score_board.create_health.assert_called_once()
        self.screen_manager.score_board.render_bullets_num.assert_called_once()

    @patch("pygame.mouse")
    @patch("pygame.Surface", return_value=MagicMock())
    def test__initialize_cursor(self, mock_surface, mock_mouse):
        """Test the initialize_cursor method."""
        self.screen.get_size.return_value = (100, 100)

        self.screen_manager._initialize_cursor()

        mock_mouse.set_visible.assert_called_once_with(False)
        mock_surface.assert_called_once_with((100, 100), pygame.SRCALPHA)

    @patch("pygame.mouse")
    @patch("pygame.Surface", return_value=pygame.Surface((50, 100)))
    def test_draw_cursor(self, mock_surface, mock_mouse):
        """Test the draw_cursor method."""
        mock_cursor_rect = MagicMock()
        self.screen_manager.cursor_surface = MagicMock()
        self.settings.cursor_img = mock_surface.return_value
        self.settings.cursor_rect = mock_cursor_rect

        self.screen_manager.draw_cursor()

        self.assertTrue(self.screen.blit.called)
        mock_mouse.get_pos.assert_called_once()
        self.screen_manager.cursor_surface.blit.assert_called_once_with(
            self.settings.cursor_img, (5, 10)
        )
        self.assertEqual(
            self.screen.blit.call_args[0],
            (self.screen_manager.cursor_surface, mock_cursor_rect),
        )

    def test_create_controls(self):
        """Test the create_controls method."""
        mock_display_controls = MagicMock(
            return_value=(
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
                [MagicMock()],
                [MagicMock()],
                [MagicMock()],
                [MagicMock()],
                MagicMock(),
                MagicMock(),
                [MagicMock()],
                [MagicMock()],
            )
        )

        with patch(
            "src.managers.ui_managers.screen_manager.display_controls",
            mock_display_controls,
        ):
            self.screen_manager.create_controls()

        self.assertTrue(mock_display_controls.called)
        self.assertIsNotNone(self.screen_manager.p1_controls_img)
        self.assertIsNotNone(self.screen_manager.p2_controls_img)
        self.assertIsNotNone(self.screen_manager.game_controls_img)
        self.assertIsNotNone(self.screen_manager.p1_controls_img_rect)
        self.assertIsNotNone(self.screen_manager.p2_controls_img_rect)
        self.assertIsNotNone(self.screen_manager.game_controls_img_rect)
        self.assertIsNotNone(self.screen_manager.p1_controls_text)
        self.assertIsNotNone(self.screen_manager.p2_controls_text)
        self.assertIsNotNone(self.screen_manager.game_controls_text)
        self.assertIsNotNone(self.screen_manager.p1_controls_text_rects)
        self.assertIsNotNone(self.screen_manager.p2_controls_text_rects)
        self.assertIsNotNone(self.screen_manager.game_controls_text_rects)

        self.assertIsInstance(self.screen_manager.p1_controls_text[0], MagicMock)
        self.assertIsInstance(self.screen_manager.p2_controls_text[0], MagicMock)
        self.assertIsInstance(self.screen_manager.game_controls_text[0], MagicMock)
        self.assertIsInstance(self.screen_manager.p1_controls_text_rects[0], MagicMock)
        self.assertIsInstance(self.screen_manager.p2_controls_text_rects[0], MagicMock)
        self.assertIsInstance(
            self.screen_manager.game_controls_text_rects[0], MagicMock
        )

    def test_draw_menu_objects(self):
        """Test the draw_menu_objects method."""
        mock_bg_img = MagicMock()
        mock_bg_img_rect = MagicMock()

        mock_display_controls = MagicMock(
            return_value=(
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
                [MagicMock()],
                [MagicMock()],
                [MagicMock()],
                [MagicMock()],
                MagicMock(),
                MagicMock(),
                [MagicMock()],
                [MagicMock()],
            )
        )
        with patch(
            "src.managers.ui_managers.screen_manager.display_controls",
            mock_display_controls,
        ):
            self.screen_manager.create_controls()

        self.screen_manager.draw_menu_objects(mock_bg_img, mock_bg_img_rect)

        expected_calls = (
            [
                call(mock_bg_img, mock_bg_img_rect),
                call(
                    self.screen_manager.p1_controls_img,
                    self.screen_manager.p1_controls_img_rect,
                ),
                call(
                    self.screen_manager.p2_controls_img,
                    self.screen_manager.p2_controls_img_rect,
                ),
                call(
                    self.screen_manager.game_controls_img,
                    self.screen_manager.game_controls_img_rect,
                ),
                call(self.settings.game_title, self.settings.game_title_rect),
            ]
            + [
                call(surface, rect)
                for surface, rect in zip(
                    self.screen_manager.p1_controls_text,
                    self.screen_manager.p1_controls_text_rects,
                )
            ]
            + [
                call(surface, rect)
                for surface, rect in zip(
                    self.screen_manager.p2_controls_text,
                    self.screen_manager.p2_controls_text_rects,
                )
            ]
            + [
                call(surface, rect)
                for surface, rect in zip(
                    self.screen_manager.game_controls_text,
                    self.screen_manager.game_controls_text_rects,
                )
            ]
        )

        self.assertEqual(self.screen.blit.call_args_list, expected_calls)
        self.buttons_manager.single.draw_button.assert_called_once()
        self.buttons_manager.multi.draw_button.assert_called_once()
        self.buttons_manager.menu_quit.draw_button.assert_called_once()

        self.assertTrue(self.screen.blit.called)
        self.assertEqual(self.screen.blit.call_count, 8)

    def test_display_high_scores_on_screen(self):
        """Test the display_high_scores method."""
        self.settings.game_modes.game_mode = "normal"
        mock_display_high_scores = MagicMock()
        with patch(
            "src.managers.ui_managers.screen_manager.display_high_scores",
            mock_display_high_scores,
        ):
            self.screen_manager.display_high_scores_on_screen()

            mock_display_high_scores.assert_called_once_with(
                self.screen_manager, self.screen, "high_scores"
            )

            mock_display_high_scores.reset_mock()
            self.settings.game_modes.game_mode = "endless_onslaught"

            self.screen_manager.display_high_scores_on_screen()

            mock_display_high_scores.assert_called_once_with(
                self.screen_manager, self.screen, "endless_scores"
            )

    def test_display_pause(self):
        """Test the display_pause method."""
        self.screen_manager.display_pause()

        self.screen.blit.assert_called_once_with(
            self.settings.pause, self.settings.pause.get_rect()
        )
        self.assertEqual(
            self.settings.pause.get_rect().centerx, self.screen.get_rect().centerx
        )
        self.assertEqual(
            self.settings.pause.get_rect().centery, self.screen.get_rect().centery
        )

    def test_update_window_mode_fullscreen(self):
        """Test the update_window_mode in fullscreen."""
        with patch("pygame.display"):
            mock_info = MagicMock()
            mock_info.current_w = 1920
            mock_info.current_h = 1080
            pygame.display.Info.return_value = mock_info
            self.screen_manager.full_screen = True
            self.screen_manager.game.ui_options.resizable = True

            self.screen_manager.update_window_mode()

            pygame.display.set_mode.assert_called_once_with(
                (1920, 1080), pygame.FULLSCREEN
            )
            self.assertFalse(self.screen_manager.game.ui_options.resizable)

    def test_update_window_mode_resizable(self):
        """Test the update window mode in resizable."""
        with patch("pygame.display"):
            mock_info = MagicMock()
            mock_info.current_w = 1920
            mock_info.current_h = 1080
            pygame.display.Info.return_value = mock_info
            self.screen_manager.full_screen = False
            self.screen_manager.game.ui_options.resizable = True

            self.screen_manager.update_window_mode()

            pygame.display.set_mode.assert_called_once_with(
                (1920, 1080), pygame.RESIZABLE
            )
            self.assertFalse(self.screen_manager.game.ui_options.resizable)

    def test_toggle_window_mode(self):
        """Test the toggle window mode method."""
        self.screen_manager.full_screen = True
        self.screen_manager.game.ui_options.resizable = True

        self.screen_manager.toggle_window_mode()

        self.assertFalse(self.screen_manager.full_screen)
        self.assertFalse(self.screen_manager.game.ui_options.resizable)

        self.screen_manager.toggle_window_mode()

        self.assertTrue(self.screen_manager.full_screen)
        self.assertTrue(self.screen_manager.game.ui_options.resizable)

    @patch("src.managers.ui_managers.screen_manager.resize_image")
    def test_resize_screen(self, mock_resize):
        """Test the resize_screen method."""
        pygame.display.set_mode = MagicMock()
        mock_ship = MagicMock()
        self.game.ships = [mock_ship]
        self.game.game_over_manager.set_game_end_position = MagicMock()

        new_size = (1600, 900)
        self.screen_manager.resize_screen(new_size)

        # Assertions
        self.assertEqual(
            self.settings.screen_width, self.screen_manager.screen.get_rect().width
        )
        self.assertEqual(
            self.settings.screen_height, self.screen_manager.screen.get_rect().height
        )

        self.assertEqual(mock_resize.call_count, 5)

        self.game.game_over_manager.set_game_end_position.assert_called_once()
        self.game.save_load_manager.update_rect_positions.assert_called_once()
        self.game.save_load_manager.set_screen_title_position.assert_called_once()

        mock_ship.screen_rect = self.screen.get_rect.return_value
        mock_ship.set_cosmic_conflict_pos.assert_called_once()


if __name__ == "__main__":
    unittest.main()
