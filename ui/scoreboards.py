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
from utils.constants import BOSS_RUSH_IMAGE_MAP
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
        self.high_scores_file = 'high_score.json'

        # Font settings
        self.text_color = (238, 75, 43)
        self.level_color = 'blue'
        self.font = pygame.font.SysFont('', 27)
        self.bullets_num_font = pygame.font.SysFont('', 25)
        self.missiles_icon = pygame.image.load('images/other/missile_icon.png')
        self.phoenix_missiles_icon = pygame.image.load('images/other/phoenix_missile_icon.png')

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
        ship_scores = [("Thunderbird", self.stats.thunderbird_score),
                       ("Phoenix", self.second_stats.phoenix_score)]
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
                f"{getattr(self.game, f'{ship_name.lower()}_ship').missiles_num}")
            rend_missiles_num = self.font.render(missiles_str, True, (71,71,71,255), None)
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
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        # Set the position of the high score image.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.level_rect.centerx
        self.high_score_rect.top = self.thunderbird_score_rect.top

    def update_high_score(self):
        """Updates the high score if the current score is higher and,
        renders the new high score on screen."""
        if self.stats.thunderbird_score + self.second_stats.phoenix_score > self.stats.high_score:
            self.stats.high_score = self.stats.thunderbird_score + self.second_stats.phoenix_score
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
            "boss_rush": "Boss Rush: " + \
                BOSS_RUSH_IMAGE_MAP.get(self.stats.level, f'Level {str(self.stats.level)}').title()
        }

        level_str = level_map.get(self.settings.game_modes.game_mode, f"Level {str(self.stats.level)}")
        self.level_image = self.font.render(level_str, True, self.level_color, None)

        # Position the level image in the center of the screen.
        screen_width, _ = self.screen.get_size()
        _, level_height = self.level_image.get_size()
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = screen_width // 2
        self.level_rect.top = 25 + level_height

    def render_bullets_num(self):
        """Renders the remaining bullets number for Thunderbird and Pheonix
        and if they are out of bullets, displays an appropriate message.
        """
        screen_rect = self.screen.get_rect()
        bullets_num = {}
        ships = [("Thunderbird", self.game.thunderbird_ship),
                 ("Phoenix", self.game.phoenix_ship)]

        for ship_name, ship in ships:
            bullets = ship.remaining_bullets if ship.state.alive else 0
            bullets_str = f"Remaining bullets: {bullets}" if bullets else "Out of bullets!"
            bullets_num[ship_name] = self.bullets_num_font.render(bullets_str, True,
                                                                   self.text_color, None)

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
            thunderbird_heart.rect.x = 5 + thunderbird_heart_number  * (thunderbird_heart.rect.width + 5)
            thunderbird_heart.rect.y = 10
            self.thunderbird_health.add(thunderbird_heart)

        # Create heart sprites for the phoenix player.
        self.phoenix_health = Group()
        for phoenix_heart_num in range(self.stats.phoenix_hp):
            phoenix_heart = Heart(self.game)
            phoenix_heart.rect.x = (
                self.settings.screen_width -
                (5 + (phoenix_heart_num + 1) * (phoenix_heart.rect.width + 5)))
            phoenix_heart.rect.y = 10
            self.phoenix_health.add(phoenix_heart)

    def save_high_score(self, score_key):
        """Save the high score to a JSON file."""
        filename = self.high_scores_file
        if self.stats.thunderbird_score + self.second_stats.phoenix_score <= 0:
            return
        try:
            with open(filename, 'r', encoding='utf-8') as score_file:
                high_scores = json.load(score_file)
        except json.JSONDecodeError:
            high_scores = {'high_scores': []}

        scores = high_scores.get(score_key, [])
        new_score = self.stats.thunderbird_score + self.second_stats.phoenix_score

        while True:
            if self.game.return_to_menu:
                player_name = get_player_name(self.screen, self.game.bg_img)
            else:
                player_name = get_player_name(self.screen, self.game.bg_img, self.settings.game_over,
                                          self.game.game_over_rect)

            for i, score in enumerate(scores):
                if score['name'] == player_name:
                    message = f"A high score with the name '{player_name}' already exists."
                    display_message(self.screen, message, 2)
                    break
            else:
                break

        new_entry = {'name': player_name, 'score': new_score}

        # Check if new score matches an existing score
        for i, score in enumerate(scores):
            if score['score'] == new_score:
                scores[i] = new_entry
                break
        else:
            scores.append(new_entry)

        # Sort scores by score value in descending order
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
        high_scores[score_key] = scores

        with open(filename, 'w', encoding='utf-8') as score_file:
            json.dump(high_scores, score_file)


    def delete_high_scores(self, score_key):
        """Delete the high scores for a specified score key."""
        filename = self.high_scores_file
        try:
            with open(filename, 'r', encoding='utf-8') as score_file:
                high_scores = json.load(score_file)
        except json.JSONDecodeError:
            high_scores = {'high_scores': []}

        if score_key in high_scores:
            del high_scores[score_key]

        with open(filename, 'w', encoding='utf-8') as score_file:
            json.dump(high_scores, score_file)

    def show_score(self):
        """Draw various score-related elements to the screen,
        including player scores, the number of missiles remaining 
        for each player, the high score, the current
        level, and the remaining health of each player's ship.
        """
        if not any([self.settings.game_modes.meteor_madness, self.settings.game_modes.boss_rush]):
            self.screen.blit(self.thunderbird_score_image, self.thunderbird_score_rect)
            self.screen.blit(self.phoenix_score_image, self.phoenix_score_rect)
        if self.settings.game_modes.last_bullet:
            self.screen.blit(self.thunder_bullets_num_img, self.thunder_bullets_num_rect)
            self.screen.blit(self.phoenix_bullets_num_img, self.phoenix_bullets_num_rect)
        self.screen.blit(self.thunderbird_rend_missiles_num, self.thunderbird_missiles_rect)
        self.screen.blit(self.missiles_icon, self.thunderbird_missiles_img_rect)
        self.screen.blit(self.phoenix_rend_missiles_num, self.phoenix_missiles_rect)
        self.screen.blit(self.phoenix_missiles_icon, self.phoenix_missiles_img_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.game.thunderbird_ship.state.alive:
            self.thunderbird_health.draw(self.screen)
        if self.game.phoenix_ship.state.alive:
            self.phoenix_health.draw(self.screen)



class SingleScoreBoard(ScoreBoard):
    """A class to report scoring information for the single player mode."""
    def __init__(self, game):
        super().__init__(game)
        self.high_scores_file = 'single_high_score.json'

        self.prep_level()
        self.render_scores()
        self.render_high_score()
        self.create_health()
        self.render_bullets_num()

    def render_scores(self):
        """Render the scores and missiles number for the Thunderbird
        and display them on the screen.
        """
        screen_rect = self.screen.get_rect()
        rounded_thunderbird_score = round(self.stats.thunderbird_score)
        thunderbird_score_str = f"Score: {rounded_thunderbird_score:,}"
        thunderbird_missiles = f"{self.game.thunderbird_ship.missiles_num}"
        missiles_img_rect = self.missiles_icon.get_rect()
        missiles_img_rect.bottom = screen_rect.bottom - 5
        self.thunderbird_missiles_img_rect = missiles_img_rect

        self.thunderbird_score_image = self.font.render(thunderbird_score_str,
                                                        True,self.text_color, None)
        self.thunderbird_rend_missiles_num = self.font.render(thunderbird_missiles,
                                                        True, (71,71,71,255), None)

        # Display the score at the stop right of the screen.
        self.thunderbird_score_rect = self.thunderbird_score_image.get_rect()
        self.thunderbird_score_rect.right = self.level_rect.centerx + 250
        self.thunderbird_score_rect.top = 20

        self.thunderbird_missiles_rect = self.thunderbird_rend_missiles_num.get_rect()
        self.thunderbird_missiles_rect.left = screen_rect.left + 28
        self.thunderbird_missiles_rect.bottom = screen_rect.bottom - 10
        self.thunderbird_missiles_img_rect.left = screen_rect.left

    def update_high_score(self):
        """Updates the high score if the current score is higher and,
        renders the new high score on screen.
        """
        if self.stats.thunderbird_score  > self.stats.high_score:
            self.stats.high_score = self.stats.thunderbird_score
            self.render_high_score()

    def render_bullets_num(self):
        """Renders the remaining bullets number for Thunderbird and
        if they are out of bullets, displays an appropriate message."""
        thunder_alive = self.game.thunderbird_ship.state.alive

        thunder_bullets = self.game.thunderbird_ship.remaining_bullets if thunder_alive else 0

        thunder_bullets_str = (f"Remaining bullets: {thunder_bullets}"
                                if thunder_bullets else "Out of bullets!")

        self.thunder_bullets_num_img = self.bullets_num_font.render(thunder_bullets_str,
                                                            True, self.text_color, None)

        self.thunder_bullets_num_rect = self.thunder_bullets_num_img.get_rect()

        self.thunder_bullets_num_rect.top = 55
        self.thunder_bullets_num_rect.left = self.screen_rect.left + 10

    def show_score(self):
        """Draw scores, level number of remaining missiles 
        and health to the screen.
        """
        if not self.settings.game_modes.meteor_madness:
            self.screen.blit(self.thunderbird_score_image, self.thunderbird_score_rect)
        if self.settings.game_modes.last_bullet:
            self.screen.blit(self.thunder_bullets_num_img, self.thunder_bullets_num_rect)
        self.screen.blit(self.thunderbird_rend_missiles_num, self.thunderbird_missiles_rect)
        self.screen.blit(self.missiles_icon, self.thunderbird_missiles_img_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.game.thunderbird_ship.state.alive:
            self.thunderbird_health.draw(self.screen)
