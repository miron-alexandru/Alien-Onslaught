"""
The 'scoreboards' module contains the ScoreBoard class for
managing the score and the HUD of the game.
"""

import pygame.font

from pygame.sprite import Group
from src.entities.player_entities.player_health import Heart

from src.utils.game_utils import (
    load_single_image,
    get_boss_rush_title,
    draw_image,
    render_bullet_num,
)


class ScoreBoard:
    """A class to report scoring information."""

    def __init__(self, game):
        """Initialize scorekeeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

        # Font settings
        self.text_color = (238, 75, 43)
        self.level_color = "blue"
        self.font = pygame.font.SysFont("", 27)
        self.bullets_num_font = pygame.font.SysFont("", 25)
        self.missiles_icon = load_single_image("other/missile_icon.png")
        self.phoenix_missiles_icon = load_single_image("other/phoenix_missile_icon.png")

        # Prepare the initial score and player health images.
        self.prep_level()
        self.render_scores()
        self.render_missiles_num()
        self.render_high_score()
        self.create_health()

    def render_scores(self):
        """Render the scores for the ships and display them on the screen."""
        self._render_ship_scores("Thunderbird", self.stats.thunderbird_score, -200)
        self._render_ship_scores("Phoenix", self.stats.phoenix_score, 300)

    def _render_ship_scores(self, ship_name, score, offset_x):
        """Render the score for a ship and update the corresponding attributes."""
        rounded_score = round(score)
        score_str = f"{ship_name}: {rounded_score:,}"
        score_img = self.font.render(score_str, True, self.text_color, None)
        score_rect = score_img.get_rect()

        score_rect.right = self.level_rect.centerx + offset_x
        score_rect.top = 20

        if ship_name == "Thunderbird":
            self.thunderbird_score_image = score_img
            self.thunderbird_score_rect = score_rect
        else:
            self.phoenix_score_image = score_img
            self.phoenix_score_rect = score_rect

    def _get_missiles_to_render(self, ship):
        """Get a list of ship(s) for which to render the missile count."""
        missiles_to_render = []

        if ship is None:
            missiles_to_render.extend(self.game.ships)
        elif ship is self.thunderbird_ship or ship is self.phoenix_ship:
            missiles_to_render.append(ship)

        return missiles_to_render

    def update_missiles_attributes(
        self, ship, rend_missiles_num, missiles_rect, missiles_img_rect, screen_rect
    ):
        """Update the attributes related to the display of missiles for a ship."""
        if ship is self.thunderbird_ship:
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

    def render_missiles_num(self, ship=None):
        """Render the missiles number for the specified ship or all ships."""
        screen_rect = self.screen.get_rect()

        ship_missiles = self._get_missiles_to_render(ship)

        for missile in ship_missiles:
            missiles_str = str(missile.missiles_num)
            rend_missiles_num = self.font.render(
                missiles_str, True, (71, 71, 71, 255), None
            )
            missiles_rect = rend_missiles_num.get_rect()
            missiles_img_rect = self.missiles_icon.get_rect()
            missiles_img_rect.bottom = screen_rect.bottom - 5

            missiles_rect.left = screen_rect.left + 28
            missiles_rect.bottom = screen_rect.bottom - 10

            self.update_missiles_attributes(
                missile,
                rend_missiles_num,
                missiles_rect,
                missiles_img_rect,
                screen_rect,
            )

    def render_high_score(self):
        """Render the high score and display it at
        the center of the top of the screen.
        """
        high_score = round(self.stats.high_score)
        high_score_str = f"High Score: {high_score:,}"
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
        self.stats.high_score = self.stats.thunderbird_score + self.stats.phoenix_score

        self.render_high_score()

    def prep_level(self):
        """Render the current level as an image and position it
        at the center of the screen based on the game mode.
        """
        level_titles = {
            "endless_onslaught": "Endless Onslaught",
            "slow_burn": f"Slow Burn Level {self.stats.level}",
            "meteor_madness": f"Meteor Madness Level {self.stats.level}",
            "last_bullet": f"Last Bullet Level {self.stats.level}",
            "cosmic_conflict": "Cosmic Conflict",
            "one_life_reign": f"One Life Reign Level {self.stats.level}",
            "boss_rush": get_boss_rush_title(self.stats.level),
        }

        level_str = level_titles.get(
            self.settings.game_modes.game_mode, f"Level {str(self.stats.level)}"
        )
        self.level_image = self.font.render(level_str, True, self.level_color, None)
        self._position_level_image(self.level_image)

    def _position_level_image(self, level_image):
        """Position the level image in the center of the screen."""
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
        """Renders the remaining bullets number for Thunderbird and Phoenix
        and if they are out of bullets, displays an appropriate message.
        """
        screen_rect = self.screen.get_rect()

        self.thunder_bullets_num_img, self.thunder_bullets_num_rect = render_bullet_num(
            self.thunderbird_ship.remaining_bullets, screen_rect.left + 10, 55
        )
        self.phoenix_bullets_num_img, self.phoenix_bullets_num_rect = render_bullet_num(
            self.phoenix_ship.remaining_bullets,
            screen_rect.right - 10,
            55,
            right_aligned=True,
        )

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

    def show_score(self):
        """Draw various score-related elements to the screen,
        including player scores, remaining missiles and bullets,
        high score, current level, and remaining health of each player's ship.
        """
        self.draw_player_scores()
        self.draw_missiles_info()
        self.draw_level()
        self.draw_high_score()
        self.draw_player_health()
        self.draw_bullets_info()

    def draw_player_scores(self):
        """Draw player scores to the screen."""
        draw_image(
            self.screen, self.thunderbird_score_image, self.thunderbird_score_rect
        )
        if not self.game.singleplayer:
            draw_image(self.screen, self.phoenix_score_image, self.phoenix_score_rect)

    def draw_missiles_info(self):
        """Draw player missiles info to the screen."""
        draw_image(
            self.screen,
            self.thunderbird_rend_missiles_num,
            self.thunderbird_missiles_rect,
        )
        draw_image(self.screen, self.missiles_icon, self.thunderbird_missiles_img_rect)

        if not self.game.singleplayer:
            draw_image(
                self.screen, self.phoenix_rend_missiles_num, self.phoenix_missiles_rect
            )
            draw_image(
                self.screen, self.phoenix_missiles_icon, self.phoenix_missiles_img_rect
            )

    def draw_bullets_info(self):
        """Draw bullets info for the Last Bullet game mode."""
        if self.settings.game_modes.last_bullet:
            draw_image(
                self.screen, self.thunder_bullets_num_img, self.thunder_bullets_num_rect
            )

            if not self.game.singleplayer:
                draw_image(
                    self.screen,
                    self.phoenix_bullets_num_img,
                    self.phoenix_bullets_num_rect,
                )

    def draw_level(self):
        """Draw the current level to the screen."""
        draw_image(self.screen, self.level_image, self.level_rect)

    def draw_high_score(self):
        """Draw the high score to the screen, if applicable."""
        if not self.settings.game_modes.cosmic_conflict:
            draw_image(self.screen, self.high_score_image, self.high_score_rect)

    def draw_player_health(self):
        """Draw the remaining health of each player's ship to the screen."""
        if self.thunderbird_ship.state.alive:
            self.thunderbird_health.draw(self.screen)
        if self.phoenix_ship.state.alive and not self.game.singleplayer:
            self.phoenix_health.draw(self.screen)
