"""
This module tests the Scoreboard class which is used to manage the HUD 
and the saving / deleting of the high scores.
"""

import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.ui.scoreboards import ScoreBoard
from src.entities.player_entities.player_health import Heart


class ScoreBoardTest(unittest.TestCase):
    """Test cases for the Scoreboard class."""

    def setUp(self):
        """Set up test environment."""
        pygame.init()
        self.game = MagicMock()
        self.game.screen = pygame.Surface((1260, 700))
        self.game.settings.screen_width = 1260
        self.game.stats.phoenix_score = 0
        self.game.stats.thunderbird_score = 0
        self.game.stats.high_score = 0
        self.game.singleplayer = False
        self.scoreboard = ScoreBoard(self.game)
        self.game.ships = [
            self.scoreboard.thunderbird_ship,
            self.scoreboard.phoenix_ship,
        ]

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.scoreboard.game, self.game)
        self.assertEqual(self.scoreboard.screen, self.game.screen)
        self.assertEqual(self.scoreboard.settings, self.game.settings)
        self.assertEqual(self.scoreboard.stats, self.game.stats)
        self.assertEqual(self.scoreboard.thunderbird_ship, self.game.thunderbird_ship)
        self.assertEqual(self.scoreboard.phoenix_ship, self.game.phoenix_ship)
        self.assertIsInstance(self.scoreboard.missiles_icon, pygame.Surface)
        self.assertIsInstance(self.scoreboard.phoenix_missiles_icon, pygame.Surface)
        self.assertEqual(self.scoreboard.text_color, (238, 75, 43))
        self.assertEqual(self.scoreboard.level_color, "blue")
        self.assertIsInstance(self.scoreboard.font, pygame.font.Font)
        self.assertIsInstance(self.scoreboard.bullets_num_font, pygame.font.Font)

    def test_render_scores(self):
        """Test the render_scores method."""
        self.scoreboard.stats.thunderbird_score = 1000
        self.scoreboard.stats.phoenix_score = 500

        self.scoreboard.render_scores()

        # Thunderbird score
        self.assertIsInstance(self.scoreboard.thunderbird_score_image, pygame.Surface)
        self.assertIsInstance(self.scoreboard.thunderbird_score_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.thunderbird_score_rect.right, 430)
        self.assertEqual(self.scoreboard.thunderbird_score_rect.top, 20)

        # Phoenix score
        self.assertIsInstance(self.scoreboard.phoenix_score_image, pygame.Surface)
        self.assertIsInstance(self.scoreboard.phoenix_score_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.phoenix_score_rect.right, 930)
        self.assertEqual(self.scoreboard.phoenix_score_rect.top, 20)

    def test_render_missiles_num(self):
        """Test the render_missiles_num method."""
        self.scoreboard.thunderbird_ship.missiles_num = 3
        self.scoreboard.phoenix_ship.missiles_num = 5

        self.scoreboard.render_missiles_num()

        # Thunderbird missiles
        self.assertIsInstance(
            self.scoreboard.thunderbird_rend_missiles_num, pygame.Surface
        )
        self.assertIsInstance(self.scoreboard.thunderbird_missiles_rect, pygame.Rect)
        self.assertIsInstance(
            self.scoreboard.thunderbird_missiles_img_rect, pygame.Rect
        )
        self.assertEqual(self.scoreboard.thunderbird_missiles_rect.left, 28)
        self.assertEqual(self.scoreboard.thunderbird_missiles_rect.bottom, 690)

        # Phoenix missiles
        self.assertIsInstance(self.scoreboard.phoenix_rend_missiles_num, pygame.Surface)
        self.assertIsInstance(self.scoreboard.phoenix_missiles_rect, pygame.Rect)
        self.assertIsInstance(self.scoreboard.phoenix_missiles_img_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.phoenix_missiles_rect.right, 1232)
        self.assertEqual(self.scoreboard.phoenix_missiles_img_rect.right, 1260)

    def test_render_high_score(self):
        """Test the render_high_score method."""
        self.scoreboard.stats.high_score = 10000

        self.scoreboard.render_high_score()

        self.assertIsInstance(self.scoreboard.high_score_image, pygame.Surface)
        self.assertIsInstance(self.scoreboard.high_score_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.high_score_rect.centerx, 630)
        self.assertEqual(self.scoreboard.high_score_rect.top, 20)

    def test_update_high_score(self):
        """Test the update_high_score method."""
        # First case
        self.scoreboard.stats.high_score = 500
        self.scoreboard.stats.thunderbird_score = 300
        self.scoreboard.stats.phoenix_score = 200
        self.scoreboard.render_high_score = MagicMock()

        self.scoreboard.update_high_score()

        self.assertEqual(self.scoreboard.stats.high_score, 500)
        self.assertIsInstance(self.scoreboard.high_score_image, pygame.Surface)
        self.scoreboard.render_high_score.assert_called_once()

        # Second case
        self.scoreboard.render_high_score.reset_mock()
        self.scoreboard.stats.thunderbird_score = 1000
        self.scoreboard.stats.phoenix_score = 800

        self.scoreboard.update_high_score()

        self.assertEqual(self.scoreboard.stats.high_score, 1800)
        self.scoreboard.render_high_score.assert_called_once()

    @patch("src.ui.scoreboards.get_boss_rush_title")
    def test_prep_level(self, mock_get_title):
        """Test the prep_level method."""
        # Test case when not in the cosmic conflict game mode.
        self.game.settings.game_modes.cosmic_conflict = False
        self.game.stats.level = 5

        self.scoreboard.prep_level()

        mock_get_title.assert_called_once_with(self.game.stats.level)
        self.assertIsInstance(self.scoreboard.level_image, pygame.Surface)
        self.assertIsInstance(self.scoreboard.level_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.level_rect.right, 661)
        self.assertEqual(self.scoreboard.level_rect.top, 43)

        # Test case when in the cosmic conflict game mode.
        self.game.settings.game_modes.cosmic_conflict = True

        self.scoreboard.prep_level()

        self.assertEqual(self.scoreboard.level_rect.top, 18)

    def test_render_bullets_num(self):
        """Test the render_bullets_num method."""
        self.scoreboard.thunderbird_ship.bullets_num = 30
        self.scoreboard.phoenix_ship.bullets_num = 40

        self.scoreboard.render_bullets_num()

        # Thunderbird bullets
        self.assertIsInstance(self.scoreboard.thunder_bullets_num_img, pygame.Surface)
        self.assertIsInstance(self.scoreboard.thunder_bullets_num_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.thunder_bullets_num_rect.left, 10)
        self.assertEqual(self.scoreboard.thunder_bullets_num_rect.bottom, 74)

        # Phoenix bullets
        self.assertIsInstance(self.scoreboard.phoenix_bullets_num_img, pygame.Surface)
        self.assertIsInstance(self.scoreboard.phoenix_bullets_num_rect, pygame.Rect)
        self.assertEqual(self.scoreboard.phoenix_bullets_num_rect.right, 1250)
        self.assertEqual(self.scoreboard.phoenix_bullets_num_rect.bottom, 74)

    def test_create_health(self):
        """Test the create_health method."""
        self.game.stats.thunderbird_hp = 3
        self.game.stats.phoenix_hp = 5

        self.scoreboard.create_health()

        # Thunderbird health sprites
        self.assertIsInstance(self.scoreboard.thunderbird_health, pygame.sprite.Group)
        self.assertEqual(len(self.scoreboard.thunderbird_health), 3)

        for index, health in enumerate(self.scoreboard.thunderbird_health):
            self.assertIsInstance(health, Heart)
            self.assertEqual(health.rect.y, 10)
            expected_x = 5 + index * (health.rect.width + 5)
            self.assertEqual(health.rect.x, expected_x)

        # Phoenix health sprites
        self.assertIsInstance(self.scoreboard.phoenix_health, pygame.sprite.Group)
        self.assertEqual(len(self.scoreboard.phoenix_health), 5)

        for index, health in enumerate(self.scoreboard.phoenix_health):
            self.assertIsInstance(health, Heart)
            self.assertEqual(health.rect.y, 10)
            expected_x = self.game.settings.screen_width - (
                5 + (index + 1) * (health.rect.width + 5)
            )
            self.assertEqual(health.rect.x, expected_x)

    def test_show_score(self):
        """Test the show_score method."""
        self.scoreboard.draw_player_scores = MagicMock()
        self.scoreboard.draw_missiles_info = MagicMock()
        self.scoreboard.draw_level = MagicMock()
        self.scoreboard.draw_high_score = MagicMock()
        self.scoreboard.draw_player_health = MagicMock()
        self.scoreboard.draw_bullets_info = MagicMock()

        self.scoreboard.show_score()

        self.scoreboard.draw_player_scores.assert_called_once()
        self.scoreboard.draw_missiles_info.assert_called_once()
        self.scoreboard.draw_level.assert_called_once()
        self.scoreboard.draw_high_score.assert_called_once()
        self.scoreboard.draw_player_health.assert_called_once()
        self.scoreboard.draw_bullets_info.assert_called_once()

    @patch("src.ui.scoreboards.draw_image")
    def test_draw_player_scores(self, mock_draw_img):
        """Test the draw_player_scores method."""
        # Multiplayer case
        self.game.singleplayer = False

        self.scoreboard.draw_player_scores()

        expected_calls = [
            call(
                self.scoreboard.screen,
                self.scoreboard.thunderbird_score_image,
                self.scoreboard.thunderbird_score_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.phoenix_score_image,
                self.scoreboard.phoenix_score_rect,
            ),
        ]
        mock_draw_img.assert_has_calls(expected_calls)

        # Singleplayer case
        mock_draw_img.reset_mock()
        self.game.singleplayer = True

        self.scoreboard.draw_player_scores()

        mock_draw_img.assert_called_once_with(
            self.scoreboard.screen,
            self.scoreboard.thunderbird_score_image,
            self.scoreboard.thunderbird_score_rect,
        )

    @patch("src.ui.scoreboards.draw_image")
    def test_draw_missiles_info(self, mock_draw_img):
        """Test the draw_missiles_info method."""
        # Multiplayer case
        self.game.singleplayer = False
        self.scoreboard.render_missiles_num()

        self.scoreboard.draw_missiles_info()

        expected_calls = [
            call(
                self.scoreboard.screen,
                self.scoreboard.thunderbird_rend_missiles_num,
                self.scoreboard.thunderbird_missiles_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.missiles_icon,
                self.scoreboard.thunderbird_missiles_img_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.phoenix_rend_missiles_num,
                self.scoreboard.phoenix_missiles_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.phoenix_missiles_icon,
                self.scoreboard.phoenix_missiles_img_rect,
            ),
        ]

        self.assertEqual(mock_draw_img.call_args_list, expected_calls)

        # Singleplayer case
        mock_draw_img.reset_mock()
        self.game.singleplayer = True

        self.scoreboard.draw_missiles_info()
        single_expected_calls = [
            call(
                self.scoreboard.screen,
                self.scoreboard.thunderbird_rend_missiles_num,
                self.scoreboard.thunderbird_missiles_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.missiles_icon,
                self.scoreboard.thunderbird_missiles_img_rect,
            ),
        ]
        self.assertEqual(mock_draw_img.call_args_list, single_expected_calls)

    @patch("src.ui.scoreboards.draw_image")
    def test_draw_bullets_info(self, mock_draw_img):
        """Test the draw_bullets_info method."""
        # Multiplayer case
        self.game.singleplayer = False
        self.game.settings.game_modes.last_bullet = True
        self.scoreboard.render_bullets_num()

        self.scoreboard.draw_bullets_info()

        expected_calls = [
            call(
                self.scoreboard.screen,
                self.scoreboard.thunder_bullets_num_img,
                self.scoreboard.thunder_bullets_num_rect,
            ),
            call(
                self.scoreboard.screen,
                self.scoreboard.phoenix_bullets_num_img,
                self.scoreboard.phoenix_bullets_num_rect,
            ),
        ]

        self.assertEqual(mock_draw_img.call_args_list, expected_calls)
        # Singleplayer case
        self.game.singleplayer = True
        mock_draw_img.reset_mock()

        self.scoreboard.draw_bullets_info()

        mock_draw_img.assert_called_once_with(
            self.scoreboard.screen,
            self.scoreboard.thunder_bullets_num_img,
            self.scoreboard.thunder_bullets_num_rect,
        )

        # Case when the last bullet game mode is not active
        self.game.settings.game_modes.last_bullet = False
        mock_draw_img.reset_mock()

        self.scoreboard.draw_bullets_info()

        mock_draw_img.assert_not_called()

    @patch("src.ui.scoreboards.draw_image")
    def test_draw_level(self, mock_draw_img):
        """Test the draw_level method."""
        self.scoreboard.draw_level()

        mock_draw_img.assert_called_once_with(
            self.scoreboard.screen,
            self.scoreboard.level_image,
            self.scoreboard.level_rect,
        )

    @patch("src.ui.scoreboards.draw_image")
    def test_draw_high_score(self, mock_draw_img):
        """Test the draw_high_score method."""
        # Cosmic conflict game mode is not active test case
        self.game.settings.game_modes.cosmic_conflict = False

        self.scoreboard.draw_high_score()

        mock_draw_img.assert_called_once_with(
            self.scoreboard.screen,
            self.scoreboard.high_score_image,
            self.scoreboard.high_score_rect,
        )

        # Cosmic conflict game mode is active test case
        mock_draw_img.reset_mock()
        self.game.settings.game_modes.cosmic_conflict = True

        self.scoreboard.draw_high_score()

        mock_draw_img.assert_not_called()

    def test_draw_player_health(self):
        """Test the draw_player_health method."""
        # Singleplayer case
        self.game.singleplayer = True
        self.game.thunderbird_ship.state.alive = True
        self.scoreboard.thunderbird_health = MagicMock()
        self.scoreboard.phoenix_health = MagicMock()

        self.scoreboard.draw_player_health()

        self.scoreboard.thunderbird_health.draw.assert_called_once_with(
            self.scoreboard.screen
        )
        self.scoreboard.phoenix_health.draw.assert_not_called()

        # Multiplayer case and the thunderbird ship is not alive
        self.game.singleplayer = False
        self.game.thunderbird_ship.state.alive = False
        self.scoreboard.thunderbird_health.draw.reset_mock()
        self.scoreboard.phoenix_health.draw.reset_mock()

        self.scoreboard.draw_player_health()

        self.scoreboard.phoenix_health.draw.assert_called_once_with(
            self.scoreboard.screen
        )
        self.scoreboard.thunderbird_health.draw.assert_not_called()


if __name__ == "__main__":
    unittest.main()
