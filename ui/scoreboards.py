"""The scoreboards module contains the class that reports the scoring information such as:
highscore, players score, health, level."""

import json
import pygame.font

from pygame.sprite import Group
from entities.player_health import Heart




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

        # Font settings
        self.text_color = 'red'
        self.level_color = 'blue'
        self.font = pygame.font.SysFont('', 27)

        # Prepare the initial score and player health images.
        self.prep_level()
        self.render_scores()
        self.render_high_score()
        self.create_health()

    def render_scores(self):
        """Render the scores for Thunderbird and Phoenix ships and display them on the screen."""
        # Calculate the rounded scores
        rounded_thunderbird_score = round(self.stats.thunderbird_score)
        rounded_phoenix_score = round(self.second_stats.phoenix_score)

        # Convert the scores into strings with proper formatting.
        thunderbird_score_str = f"Thunderbird: {rounded_thunderbird_score:,}"
        phoenix_score_str = f"Phoenix: {rounded_phoenix_score:,}"

        # Render the score images.
        self.thunderbird_score_image = self.font.render(thunderbird_score_str,
                                                         True, self.text_color, None)
        self.phoenix_score_image = self.font.render(phoenix_score_str, True, self.text_color, None)

        # Set the positions of the score images.
        self.thunderbird_score_rect = self.thunderbird_score_image.get_rect()
        self.thunderbird_score_rect.right = self.level_rect.centerx - 200
        self.thunderbird_score_rect.top = 20

        self.phoenix_score_rect = self.phoenix_score_image.get_rect()
        self.phoenix_score_rect.right = self.level_rect.centerx + 300
        self.phoenix_score_rect.top = 20

    def render_high_score(self):
        """Render the high score and display it at the center of the top of the screen."""
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
        """Render the current level as an image and position it at the center of the screen."""
        if self.settings.endless_onslaught:
            level_str =  "Endless Onslaught"
        elif self.settings.slow_burn:
            level_str = f"Slow Burn Level {str(self.stats.level)}"
        elif self.settings.meteor_madness:
            level_str = f"Meteor Madness Level {str(self.stats.level)}"
        else:
            level_str = f"Level {str(self.stats.level)}"

        self.level_image = self.font.render(level_str, True, self.level_color, None)

        # Position the level image in the center of the screen.
        screen_width, _ = self.screen.get_size()
        _, level_height = self.level_image.get_size()
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = screen_width // 2
        self.level_rect.top = 25 + level_height


    def create_health(self):
        """Creates heart sprites for both players based on their health points."""
        # Create heart sprites for the thunderbird player.
        self.thunderbird_health = Group()
        for thunderbird_heart_number in range(self.stats.thunderbird_hp):
            thunderbird_heart = Heart(self.game)
            thunderbird_heart.rect.x = 10 + thunderbird_heart_number * thunderbird_heart.rect.width
            thunderbird_heart.rect.y = 10
            self.thunderbird_health.add(thunderbird_heart)

        # Create heart sprites for the phoenix player.
        self.phoenix_health = Group()
        for phoenix_heart_num in range(self.stats.phoenix_hp):
            phoenix_heart = Heart(self.game)
            phoenix_heart.rect.x = (
                self.settings.screen_width -
                (10 + (phoenix_heart_num + 1) * phoenix_heart.rect.width))
            phoenix_heart.rect.y = 10
            self.phoenix_health.add(phoenix_heart)

    def save_high_score(self):
        """Save the high score to a JSON file."""
        filename = 'high_score.json'
        try:
            with open(filename, 'r', encoding='utf-8') as score_file:
                high_scores = json.load(score_file)
        except json.JSONDecodeError:
            high_scores = {'high_scores': [0] * 10}

        scores = high_scores['high_scores']
        new_score = self.stats.thunderbird_score + self.second_stats.phoenix_score

        if new_score not in scores:
            scores.append(new_score)
            scores.sort(reverse=True)
            scores = scores[:10]
            high_scores['high_scores'] = scores

            with open(filename, 'w', encoding='utf-8') as score_file:
                json.dump(high_scores, score_file)


    def show_score(self):
        """Draw scores, level and health to the screen."""
        if not self.settings.meteor_madness:
            self.screen.blit(self.thunderbird_score_image, self.thunderbird_score_rect)
            self.screen.blit(self.phoenix_score_image, self.phoenix_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.thunderbird_health.draw(self.screen)
        self.phoenix_health.draw(self.screen)


class SecondScoreBoard(ScoreBoard):
    """A class to report scoring information for the single player mode."""
    def __init__(self, game):
        super().__init__(game)

        self.prep_level()
        self.render_scores()
        self.render_high_score()
        self.create_health()

    def render_scores(self):
        """Turn the score into a rendered image."""
        rounded_thunderbird_score = round(self.stats.thunderbird_score)
        thunderbird_score_str = f"Score: {rounded_thunderbird_score:,}"
        self.thunderbird_score_image = self.font.render(thunderbird_score_str, True,
            self.text_color, None)

        # Display the score at the stop right of the screen.
        self.thunderbird_score_rect = self.thunderbird_score_image.get_rect()
        self.thunderbird_score_rect.right = self.level_rect.centerx + 250
        self.thunderbird_score_rect.top = 20

    def update_high_score(self):
        """Updates the high score if the current score is higher and,
        renders the new high score on screen."""
        if self.stats.thunderbird_score  > self.stats.high_score:
            self.stats.high_score = self.stats.thunderbird_score
            self.render_high_score()

    def show_score(self):
        """Draw scores, level and health to the screen."""
        if not self.settings.meteor_madness:
            self.screen.blit(self.thunderbird_score_image, self.thunderbird_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.thunderbird_health.draw(self.screen)
