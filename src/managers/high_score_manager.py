"""
The 'high_score_manager' module contains the HighScoreManager class
that is used to manage the saving and deletion of the high scores.
"""

import json

from src.utils.constants import SINGLE_PLAYER_FILE, MULTI_PLAYER_FILE
from src.utils.game_utils import display_message, get_player_name


class HighScoreManager:
    """A class that manages the saving and deletion of the high scores."""

    def __init__(self, game):
        self.game = game
        self.stats = game.stats
        self.screen = game.screen
        self.high_scores_file = (
            SINGLE_PLAYER_FILE if self.game.singleplayer else MULTI_PLAYER_FILE
        )

    def save_high_score(self, score_key):
        """Save the high score to a JSON file."""
        filename = self.high_scores_file
        if self.stats.high_score <= 0:
            return
        try:
            with open(filename, "r", encoding="utf-8") as score_file:
                high_scores = json.load(score_file)
        except json.JSONDecodeError:
            high_scores = {"high_scores": []}

        scores = high_scores.get(score_key, [])
        new_score = self.stats.high_score

        while True:
            player_name = get_player_name(
                self.screen,
                self.game.bg_img,
                self.game.screen_manager.draw_cursor,
                self.stats.high_score,
                self.game.settings.game_end_img,
                self.game.settings.game_end_rect,
            )

            if player_name is None:
                return
            if player_name == "":
                player_name = "Player"

            for i, score in enumerate(scores):
                if score["name"] == player_name:
                    message = (
                        f"A high score with the name '{player_name}' already exists."
                    )
                    display_message(self.screen, message, 2)
                    break
            else:
                break

        new_entry = {"name": player_name, "score": new_score}

        # Check if new score matches an existing score
        for i, score in enumerate(scores):
            if score["score"] == new_score:
                scores[i] = new_entry
                break
        else:
            scores.append(new_entry)

        # Sort scores by score value in descending order
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
        high_scores[score_key] = scores

        with open(filename, "w", encoding="utf-8") as score_file:
            json.dump(high_scores, score_file)

    def delete_high_scores(self, score_key):
        """Delete the high scores for a specified score key."""
        filename = self.high_scores_file
        try:
            with open(filename, "r", encoding="utf-8") as score_file:
                high_scores = json.load(score_file)
        except json.JSONDecodeError:
            high_scores = {"high_scores": []}

        if score_key in high_scores:
            del high_scores[score_key]

        with open(filename, "w", encoding="utf-8") as score_file:
            json.dump(high_scores, score_file)

    def update_high_score_filename(self):
        """Update highscore filename based on the game."""
        if self.game.singleplayer:
            self.high_scores_file = SINGLE_PLAYER_FILE
        else:
            self.high_scores_file = MULTI_PLAYER_FILE
