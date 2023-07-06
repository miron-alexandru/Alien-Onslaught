"""
This module tests the functions from the game_utils module that are
related to the high scores.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.utils.game_utils import (
    load_high_scores,
    display_high_scores,
    get_player_name,
    render_label,
    draw_buttons,
)
from src.utils.constants import DEFAULT_HIGH_SCORES


class HighScoreFunctionsTests(unittest.TestCase):
    """Test cases for high score functions."""

    def setUp(self):
        """Set up test_environment."""
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.game = MagicMock()

    def tearDown(self):
        pygame.quit()

    @patch("builtins.open")
    @patch("json.load")
    def test_load_high_scores_existing_file(self, mock_json_load, mock_open):
        """Test loading high scores from an existing file."""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        expected_scores = {"score_key": [10, 20, 30]}

        mock_json_load.return_value = expected_scores

        scores = load_high_scores(self.game)

        mock_open.assert_called_once_with(
            "single_high_score.json", "r", encoding="utf-8"
        )
        mock_json_load.assert_called_once_with(mock_file)

        self.assertEqual(scores, expected_scores)

    @patch("builtins.open")
    @patch("json.load")
    def test_load_high_scores_non_existing_file(self, mock_json_load, mock_open):
        """Test loading high scores from a non-existing file."""
        mock_open.side_effect = FileNotFoundError
        expected_scores = DEFAULT_HIGH_SCORES

        self.game.singleplayer = False

        scores = load_high_scores(self.game)

        mock_open.assert_called_once_with("high_score.json", "r", encoding="utf-8")
        mock_json_load.assert_not_called()

        self.assertEqual(scores, expected_scores)

    @patch("src.utils.game_utils.load_high_scores")
    @patch("src.utils.game_utils.render_text")
    @patch("pygame.font.SysFont")
    def test_display_high_scores(
        self, mock_sysfont, mock_render_text, mock_load_high_scores
    ):
        """Test the display_high_scores function."""
        # Set up mock objects and test data
        screen = MagicMock()
        screen.get_size.return_value = (800, 600)
        score_key = "score_key"
        scores = [{"name": "Player1", "score": 10}, {"name": "Player2", "score": 20}]
        mock_load_high_scores.return_value = {score_key: scores}

        # mock_render_text side effects
        title_text_surfaces = [MagicMock()]
        title_text_rects = [MagicMock()]
        rank_text_surfaces = [MagicMock(), MagicMock()]
        rank_text_rects = [MagicMock(), MagicMock()]
        score_text_surfaces = [MagicMock(), MagicMock()]
        score_text_rects = [MagicMock(), MagicMock()]
        mock_render_text.side_effect = [
            (title_text_surfaces, title_text_rects),
            (rank_text_surfaces, rank_text_rects),
            (score_text_surfaces, score_text_rects),
        ]

        display_high_scores(self.game, screen, score_key)

        # Assertions
        self.assertEqual(mock_sysfont.call_count, 2)

        mock_render_text.assert_any_call(
            "HIGH SCORES",
            mock_sysfont.return_value,
            (255, 215, 0),
            (screen.get_size()[0] // 2 - 520, screen.get_size()[1] // 2 - 150),
            int(screen.get_size()[1] * 0.06),
        )
        mock_render_text.assert_any_call(
            "1st Player1\n2nd Player2",
            mock_sysfont.return_value,
            "red",
            (screen.get_size()[0] // 2 - 550, screen.get_size()[1] // 2 - 50),
            int(screen.get_size()[1] * 0.05),
        )
        mock_render_text.assert_any_call(
            "10\n20",
            mock_sysfont.return_value,
            "red",
            (screen.get_size()[0] // 2 - 270, screen.get_size()[1] // 2 - 50),
            int(screen.get_size()[1] * 0.05),
        )
        screen.blit.assert_any_call(title_text_surfaces[0], title_text_rects[0])
        screen.blit.assert_any_call(rank_text_surfaces[0], rank_text_rects[0])
        screen.blit.assert_any_call(rank_text_surfaces[1], rank_text_rects[1])
        screen.blit.assert_any_call(score_text_surfaces[0], score_text_rects[0])
        screen.blit.assert_any_call(score_text_surfaces[1], score_text_rects[1])

        mock_load_high_scores.assert_called_with(self.game)

    @patch("pygame.font.SysFont")
    def test_get_player_name(self, mock_sysfont):
        """Test the get_player_name function."""
        # Set up mock objects and test data
        background_image = pygame.Surface((800, 600))
        cursor = MagicMock()
        high_score = 1000

        mock_font = MagicMock()
        mock_render = MagicMock(return_value=pygame.Surface((100, 20)))
        mock_font.render = mock_render
        mock_sysfont.return_value = mock_font

        pygame.event.get = MagicMock(return_value=[])

        # Simulate user input and events
        with patch("pygame.display.flip"), patch.object(sys, "exit"):
            # Simulate the user deleting the default name and then
            # entering a name and pressing Enter
            pygame.event.get.side_effect = [
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="A")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="k")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="e")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)],
            ]
            player_name = get_player_name(
                self.screen, background_image, cursor, high_score
            )

            # Assertions
            self.assertEqual(player_name, "Ake")
            self.assertEqual(pygame.display.flip.call_count, 9)
            self.assertEqual(cursor.call_count, 9)

            mock_sysfont.assert_any_call("verdana", 19)
            mock_sysfont.assert_any_call("verdana", 23)

            # Simulate the user clicking the Save button
            pygame.event.get.side_effect = [
                [MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(425, 320))],
            ]
            player_name = get_player_name(
                self.screen, background_image, cursor, high_score
            )

            # Assertions
            self.assertEqual(player_name, "Player")

            # Simulate the user clicking the Close button
            pygame.event.get.side_effect = [
                [MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(520, 320))],
            ]
            player_name = get_player_name(
                self.screen, background_image, cursor, high_score
            )

            # Assertions
            self.assertIsNone(player_name)

            # Simulate the user exceeding the character limit and pressing Enter
            pygame.event.get.side_effect = [
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="a")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="b")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_c, unicode="c")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_d, unicode="d")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_e, unicode="e")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_f, unicode="f")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_g, unicode="g")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_h, unicode="h")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_i, unicode="i")],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)],
            ]
            player_name = get_player_name(
                self.screen, background_image, cursor, high_score
            )

            # Assertions
            self.assertEqual(player_name, "Playerabcd")

            # Simulate the user pressing Backspace
            pygame.event.get.side_effect = [
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)],
            ]
            player_name = get_player_name(
                self.screen, background_image, cursor, high_score
            )

            # Assertions
            self.assertEqual(player_name, "Playe")

    def test_draw_buttons(self):
        """Test the draw_buttons function."""
        font = pygame.font.SysFont("verdana", 19)
        text_color = pygame.Color("white")

        button_info = [
            {
                "label": "Close",
                "rect": pygame.Rect(400, 300, 65, 24),
            },
            {
                "label": "Save",
                "rect": pygame.Rect(335, 300, 50, 24),
            },
        ]

        draw_buttons(self.screen, button_info, font, text_color)

        for button in button_info:
            self.assertTrue(self.screen.get_rect().colliderect(button["rect"]))

    def test_render_label(self):
        """Test the render_label function."""
        screen = MagicMock()
        font = pygame.font.SysFont("verdana", 19)
        text = "Test Label"
        pos = (400, 300)
        text_color = pygame.Color("white")

        render_label(screen, text, pos, font, text_color)

        # Assert that screen.blit was called once
        screen.blit.assert_called_once()

        # Retrieve the arguments used in the blit call
        blit_args = screen.blit.call_args[0]

        # Verify the first argument is a Surface
        self.assertIsInstance(blit_args[0], pygame.Surface)

        # Verify the second argument is a tuple representing the position (text_x, text_y)
        self.assertIsInstance(blit_args[1], tuple)
        self.assertEqual(len(blit_args[1]), 2)


if __name__ == "__main__":
    unittest.main()
