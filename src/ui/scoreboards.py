"""
The 'scoreboards' module contains the ScoreBoard and SingleScoreboard
class for managing the score and other UI aspects of the game such as:
scoring, player health, available missiles.
It also manages the saving of the highscores.
"""

import json
import pygame.font

from pygame.sprite import Group
from entities.player_health import Heart
from utils.constants import BOSS_RUSH
from utils.game_utils import get_player_name, display_message


class ScoreBoard:
    """A class to report scoring information."""

    def __init__(self, game):
        """Initialize scorekeeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.second_stats = game.stats
        self.high_scores_file = (
            "single_high_score.json" if self.game.singleplayer else "high_score.json"
        )

        # Font settings
        self.text_color = (238, 75, 43)
        self.level_color = "blue"
        self.font = pygame.font.SysFont("", 27)
        self.bullets_num_font = pygame.font.SysFont("", 25)
        self.missiles_icon = pygame.image.load(
            "../game_assets/images/other/missile_icon.png"
        )
        self.phoenix_missiles_icon = pygame.image.load(
            "../game_assets/images/other/phoenix_missile_icon.png"
        )

        # Prepare the initial score and player health images.
        self.prep_level()
        self.render_scores()
        self.render_high_score()
        self.create_health()
        self.render_bullets_num()

    def render_scores(self):
        """Render the scores and missiles number for the ships
        and display them on the screen.
        """
        screen_rect = self.screen.get_rect()
        ship_scores = [
            ("Thunderbird", self.stats.thunderbird_score),
            ("Phoenix", self.second_stats.phoenix_score),
        ]
        y_pos = 20

        for i, (ship_name, score) in enumerate(ship_scores):
            # Calculate the rounded score and convert it into a string with proper formatting.
            rounded_score = round(score)
            score_str = f"{ship_name}: {rounded_score:,}"
            score_img = self.font.render(score_str, True, self.text_color, None)
            score_rect = score_img.get_rect()

            # Set the position of the score image.
            if i == 0:
                score_rect.right = self.level_rect.centerx - 200
            else:
                score_rect.right = self.level_rect.centerx + 300
            score_rect.top = y_pos

            if ship_name == "Thunderbird":
                self.thunderbird_score_image = score_img
                self.thunderbird_score_rect = score_rect
            else:
                self.phoenix_score_image = score_img
                self.phoenix_score_rect = score_rect

            missiles_str = (
                f"{getattr(self.game, f'{ship_name.lower()}_ship').missiles_num}"
            )
            rend_missiles_num = self.font.render(
                missiles_str, True, (71, 71, 71, 255), None
            )
            missiles_img_rect = self.missiles_icon.get_rect()
            missiles_rect = rend_missiles_num.get_rect()
            missiles_rect.left = screen_rect.left + 28
            missiles_rect.bottom = screen_rect.bottom - 10
            missiles_img_rect.bottom = screen_rect.bottom - 5

            if ship_name == "Thunderbird":
                self.thunderbird_rend_missiles_num = rend_missiles_num
                self.thunderbird_missiles_rect = missiles_rect
                self.thunderbird_missiles_img_rect = missiles_img_rect
                self.thunderbird_missiles_img_rect.left = screen_rect.left
            else:
                self.phoenix_rend_missiles_num = rend_missiles_num
                self.phoenix_missiles_rect = missiles_rect
                self.phoenix_missiles_rect.right = screen_rect.right - 28
                self.phoenix_missiles_img_rect = missiles_img_rect
                self.phoenix_missiles_img_rect.right = screen_rect.right

    def render_high_score(self):
        """Render the high score and display it at
        the center of the top of the screen.
        """
        # Calculate the rounded high score.
        high_score = round(self.stats.high_score)

        # Convert the high score into a string
        high_score_str = f"High Score: {high_score:,}"

        # Render the high score image.
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, None
        )

        # Set the position of the high score image.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.level_rect.centerx
        self.high_score_rect.top = self.thunderbird_score_rect.top

    def update_high_score(self):
        """Updates the high score if the current score is higher and,
        renders the new high score on screen."""
        self.stats.high_score = (
            self.stats.thunderbird_score + self.second_stats.phoenix_score
        )
        self.render_high_score()

    def prep_level(self):
        """Render the current level as an image and position it
        at the center of the screen based on the game mode.
        """
        level_map = {
            "endless_onslaught": "Endless Onslaught",
            "slow_burn": f"Slow Burn Level {str(self.stats.level)}",
            "meteor_madness": f"Meteor Madness Level {str(self.stats.level)}",
            "last_bullet": f"Last Bullet Level {str(self.stats.level)}",
            "cosmic_conflict": "Cosmic Conflict",
            "boss_rush": "Boss Rush: "
            + BOSS_RUSH.get(
                f"boss{str(self.stats.level)}", f"Level {str(self.stats.level)}"
            ).split("/")[-1].split(".png")[0].title(),
        }

        level_str = level_map.get(
            self.settings.game_modes.game_mode, f"Level {str(self.stats.level)}"
        )
        self.level_image = self.font.render(level_str, True, self.level_color, None)

        # Position the level image in the center of the screen.
        screen_width, _ = self.screen.get_size()
        _, level_height = self.level_image.get_size()
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = screen_width // 2
        self.level_rect.top = (
            level_height
            if self.settings.game_modes.cosmic_conflict
            else level_height + 25
        )

    def render_bullets_num(self):
        """Renders the remaining bullets number for Thunderbird and Pheonix
        and if they are out of bullets, displays an appropriate message.
        """
        screen_rect = self.screen.get_rect()
        bullets_num = {}
        ships = [
            ("Thunderbird", self.game.thunderbird_ship),
            ("Phoenix", self.game.phoenix_ship),
        ]

        for ship_name, ship in ships:
            bullets = ship.remaining_bullets if ship.state.alive else 0
            bullets_str = (
                f"Remaining bullets: {bullets}" if bullets else "Out of bullets!"
            )
            bullets_num[ship_name] = self.bullets_num_font.render(
                bullets_str, True, self.text_color, None
            )

        self.thunder_bullets_num_rect = bullets_num["Thunderbird"].get_rect()
        self.phoenix_bullets_num_rect = bullets_num["Phoenix"].get_rect()

        self.thunder_bullets_num_rect.top = self.phoenix_bullets_num_rect.top = 55
        self.thunder_bullets_num_rect.left = screen_rect.left + 10
        self.phoenix_bullets_num_rect.right = screen_rect.right - 10

        self.thunder_bullets_num_img = bullets_num["Thunderbird"]
        self.phoenix_bullets_num_img = bullets_num["Phoenix"]

    def create_health(self):
        """Creates heart sprites for both players based on their health points."""
        # Create heart sprites for the thunderbird player.
        self.thunderbird_health = Group()
        for thunderbird_heart_number in range(self.stats.thunderbird_hp):
            thunderbird_heart = Heart(self.game)
            thunderbird_heart.rect.x = 5 + thunderbird_heart_number * (
                thunderbird_heart.rect.width + 5
            )
            thunderbird_heart.rect.y = 10
            self.thunderbird_health.add(thunderbird_heart)

        # Create heart sprites for the phoenix player.
        self.phoenix_health = Group()
        for phoenix_heart_num in range(self.stats.phoenix_hp):
            phoenix_heart = Heart(self.game)
            phoenix_heart.rect.x = self.settings.screen_width - (
                5 + (phoenix_heart_num + 1) * (phoenix_heart.rect.width + 5)
            )
            phoenix_heart.rect.y = 10
            self.phoenix_health.add(phoenix_heart)

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
                self.settings.game_end_img,
                self.settings.game_end_rect,
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

    def show_score(self):
        """Draw various score-related elements to the screen,
        including player scores, remaining missiles and bullets,
        high score, current level, and remaining health of each player's ship.
        """

        def draw_score(image, rect):
            self.screen.blit(image, rect)

        def draw_missiles(image, rect):
            self.screen.blit(image, rect)

        draw_score(self.thunderbird_score_image, self.thunderbird_score_rect)

        if not self.game.singleplayer:
            draw_score(self.phoenix_score_image, self.phoenix_score_rect)

        if self.settings.game_modes.last_bullet:
            draw_score(self.thunder_bullets_num_img, self.thunder_bullets_num_rect)

            if not self.game.singleplayer:
                draw_score(self.phoenix_bullets_num_img, self.phoenix_bullets_num_rect)

        draw_missiles(self.thunderbird_rend_missiles_num, self.thunderbird_missiles_rect)
        draw_missiles(self.missiles_icon, self.thunderbird_missiles_img_rect)

        if not self.game.singleplayer:
            draw_missiles(self.phoenix_rend_missiles_num, self.phoenix_missiles_rect)
            draw_missiles(self.phoenix_missiles_icon, self.phoenix_missiles_img_rect)

        draw_score(self.level_image, self.level_rect)

        if not self.settings.game_modes.cosmic_conflict:
            draw_score(self.high_score_image, self.high_score_rect)

        if self.game.thunderbird_ship.state.alive:
            self.thunderbird_health.draw(self.screen)
        if self.game.phoenix_ship.state.alive and not self.game.singleplayer:
            self.phoenix_health.draw(self.screen)

    def update_high_score_filename(self):
        """Update highscore filename based on the game."""
        if self.game.singleplayer:
            self.high_scores_file = "single_high_score.json"
        else:
            self.high_scores_file = "high_score.json"
