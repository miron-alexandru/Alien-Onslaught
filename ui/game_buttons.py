"""
This module provides a class `GameButtons` that creates and manages
the buttons and displays the controls used in the game.
"""

import sys
import pygame

from utils.constants import (
    BUTTON_NAMES, GAME_MODE_SCORE_KEYS,
    DIFFICULTIES, GAME_MODES_DESCRIPTIONS
)
from utils.game_utils import load_button_imgs, display_controls, display_game_modes_description


class Button:
    """A class that represents a button on the screen."""
    def __init__(self, game, image_loc, pos, description='', center=False):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.visible = False  # variable used for buttons that need to be visible
        self.description = description

        # Load button image and scale it to the desired size.
        self.image = pygame.image.load(image_loc)

        # Build the button's rect object and set its position.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        if center:
            self.rect.center = self.screen_rect.center
            self.rect.y -= 50
        else:
            self.rect.x, self.rect.y = pos

    def update_pos(self, *args, x=0, y=0):
        """Update the button's position."""
        if len(args) == 1:
            self.rect.center = args[0]
        elif len(args) == 2:
            self.rect.topleft = args
        self.rect.move_ip(x, y)

    def draw_button(self):
        """Draws the button if it's visible."""
        self.screen.blit(self.image, self.rect)

    def show_button_info(self):
        """Display the information about the button on the screen.
        This method is mainly used for displaying
        the description for the game modes.
        """
        display_game_modes_description(self.screen, self.description)


class GameButtons:
    """This class creates the buttons for the game.
    Contains the methods for handling every button action.
    """
    def __init__(self, game, screen, ui_options, gm_options):
        self.screen = screen
        self.game = game
        self.ui_options = ui_options
        self.gm_options = gm_options
        self.screen_rect = self.screen.get_rect()

        self.button_imgs = load_button_imgs(BUTTON_NAMES)

        self._create_game_buttons()
        self._create_menu_buttons()

    def _create_game_buttons(self):
        """Create buttons for the game menu."""
        self.play = Button(self, self.button_imgs["play_button"], (0, 0), center=True)
        # Difficulty buttons
        self.difficulty = Button(self, self.button_imgs["difficulty"],
                                 (self.play.rect.centerx - 74, self.play.rect.bottom))
        self.easy = Button(self, self.button_imgs['easy'],
                           (self.difficulty.rect.right - 10, self.difficulty.rect.y))
        self.medium = Button(self, self.button_imgs['medium'],
                             (self.easy.rect.right - 5, self.easy.rect.y))
        self.hard = Button(self, self.button_imgs['hard'],
                           (self.medium.rect.right - 5, self.medium.rect.y))

        # Game mode buttons
        self.game_modes = Button(self, self.button_imgs["game_modes"],
                                 (self.difficulty.rect.centerx - 74, self.difficulty.rect.bottom))
        self.normal = Button(self, self.button_imgs["normal"],
                             (self.game_modes.rect.right - 10,
                              self.game_modes.rect.y),
                              GAME_MODES_DESCRIPTIONS[0])
        self.endless = Button(self, self.button_imgs["endless"],
                              (self.normal.rect.right - 5,
                               self.normal.rect.y),
                               GAME_MODES_DESCRIPTIONS[1])
        self.slow_burn = Button(self, self.button_imgs["slow_burn"],
                                (self.endless.rect.right - 5,
                                 self.endless.rect.y),
                                 GAME_MODES_DESCRIPTIONS[2])
        self.meteor_madness = Button(self, self.button_imgs['meteor_madness'],
                                     (self.slow_burn.rect.right - 5,
                                      self.slow_burn.rect.y),
                                      GAME_MODES_DESCRIPTIONS[3])
        self.boss_rush = Button(self, self.button_imgs['boss_rush'],
                                (self.meteor_madness.rect.right - 5,
                                 self.meteor_madness.rect.y),
                                 GAME_MODES_DESCRIPTIONS[4])
        self.last_bullet = Button(self, self.button_imgs['last_bullet'],
                                  (self.boss_rush.rect.right - 5,
                                   self.boss_rush.rect.y),
                                   GAME_MODES_DESCRIPTIONS[5])

        # High scores and other game menu buttons
        self.high_scores = Button(self, self.button_imgs['high_scores'],
                                  (self.game_modes.rect.centerx - 74, self.game_modes.rect.bottom))
        self.delete_scores = Button(self, self.button_imgs['delete_scores'],
                                    (self.high_scores.rect.right - 10, self.high_scores.rect.y))
        self.menu = Button(self, self.button_imgs["menu_button"],
                           (self.high_scores.rect.centerx - 74, self.high_scores.rect.bottom))
        self.quit = Button(self, self.button_imgs["quit_button"],
                           (self.menu.rect.centerx - 74, self.menu.rect.bottom))

        # Lists containing the game buttons, difficulty buttons and game mode buttons
        self.game_buttons = [self.play, self.quit, self.menu, self.difficulty, self.high_scores,
                             self.game_modes]
        self.difficulty_buttons = [self.easy, self.medium, self.hard]
        self.game_mode_buttons = [self.endless, self.normal, self.slow_burn, self.meteor_madness,
                                  self.boss_rush, self.last_bullet]

    def display_description(self):
        """Display the description of the game mode button currently
        hovered over by the mouse cursor.
        """
        for button in self.game_mode_buttons:
            # Create a smaller rectangle for collision detection
            # to avoid triggering for adjacent buttons
            collision_rect = button.rect.inflate(-10, -10)
            if collision_rect.collidepoint(pygame.mouse.get_pos()):
                button.show_button_info()

    def draw_difficulty_buttons(self):
        """Draw difficulty buttons on screen."""
        for button in self.difficulty_buttons:
            button.draw_button()

    def draw_game_mode_buttons(self):
        """Draw game mode buttons on screen."""
        for button in self.game_mode_buttons:
            button.draw_button()
        self.display_description()

    def draw_buttons(self):
        """Draw game menu buttons on screen."""
        for button in self.game_buttons:
            button.draw_button()

    def _create_menu_buttons(self):
        """Create the buttons for the main menu."""
        self.single = Button(self, self.button_imgs["single_player"], (0, 0), center=True)
        self.multi = Button(self, self.button_imgs["multiplayer"],
                            (self.single.rect.centerx - 100, self.single.rect.bottom))
        self.menu_quit = Button(self, self.button_imgs["menu_quit_button"],
                                (self.multi.rect.centerx - 100, self.multi.rect.bottom))

    def handle_buttons_visibility(self):
        """Handle the visibility of buttons based on the current ui options."""
        for button in self.difficulty_buttons:
            button.visible = not self.ui_options.show_difficulty
        for button in self.game_mode_buttons:
            button.visible = not self.ui_options.show_game_modes
        self.delete_scores.visible = not self.ui_options.show_high_scores

    def handle_play_button(self, reset_game):
        """Reset game and hide all buttons."""
        reset_game()
        self.ui_options.show_difficulty = False
        self.ui_options.show_high_scores = False
        self.ui_options.show_game_modes = False

    def handle_quit_button(self):
        """Play the quit sound effect and quit the game."""
        self.game.sound_manager.game_sounds['quit_effect'].play()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()

    def handle_high_scores_button(self):
        """Toggle the visibility of the high score."""
        self.ui_options.show_high_scores = not self.ui_options.show_high_scores

    def handle_game_modes_button(self):
        """Toggle the visibility of the game modes."""
        self.ui_options.show_game_modes = not self.ui_options.show_game_modes

    def _set_game_mode_settings(self, game_mode_setting):
        """Helper function to set the game mode settings based on the current mode."""
        self.gm_options.endless_onslaught = False
        self.gm_options.slow_burn = False
        self.gm_options.meteor_madness = False
        self.gm_options.boss_rush = False
        self.gm_options.last_bullet = False
        if game_mode_setting is not None:
            setattr(self.gm_options, game_mode_setting, True)

    def handle_endless_button(self):
        """Toggle the Endless game mode setting and hide game mode buttons."""
        self.gm_options.endless_onslaught = not self.gm_options.endless_onslaught
        self._set_game_mode_settings('endless_onslaught')
        self.gm_options.game_mode = 'endless_onslaught'
        self.ui_options.show_game_modes = False

    def handle_normal_button(self):
        """Turn all game modes off, play the normal game."""
        self._set_game_mode_settings(None)
        self.gm_options.game_mode = 'normal'
        self.ui_options.show_game_modes = False

    def handle_slow_burn_button(self):
        """Toggle the Slow Burn game mode and hide game mode buttons."""
        self.gm_options.slow_burn = not self.gm_options.slow_burn
        self._set_game_mode_settings('slow_burn')
        self.gm_options.game_mode = 'slow_burn'
        self.ui_options.show_game_modes = False

    def handle_meteor_madness_button(self):
        """Toggle the Meteor Madness game mode and hide all game mode buttons."""
        self.gm_options.meteor_madness = not self.gm_options.meteor_madness
        self._set_game_mode_settings('meteor_madness')
        self.gm_options.game_mode = 'meteor_madness'
        self.ui_options.show_game_modes = False

    def handle_boss_rush_button(self):
        """Toggle the Boss Rush game mode and hide all game mode buttons."""
        self.gm_options.boss_rush = not self.gm_options.boss_rush
        self._set_game_mode_settings('boss_rush')
        self.gm_options.game_mode = 'boss_rush'
        self.ui_options.show_game_modes = False

    def handle_last_bullet_button(self):
        """Toggle the Last Bullet game mode and hide all game mode buttons."""
        self.gm_options.last_bullet = not self.gm_options.last_bullet
        self._set_game_mode_settings('last_bullet')
        self.gm_options.game_mode = 'last_bullet'
        self.ui_options.show_game_modes = False

    def handle_difficulty_button(self, speedup_scale):
        """Set the game difficulty (speed-up scale)."""
        def handle():
            """Set the speedup scale and hide the difficulty options UI."""
            self.game.settings.speedup_scale = speedup_scale
            self.ui_options.show_difficulty = False
        return handle

    def handle_difficulty_toggle(self):
        """Toggle visibility of the difficulty buttons."""
        self.ui_options.show_difficulty = not self.ui_options.show_difficulty

    def handle_delete_button(self):
        """Delete all high scores for the current game mode."""
        game_mode = self.game.settings.game_modes.game_mode or 'normal'
        high_score_key = GAME_MODE_SCORE_KEYS.get(game_mode, 'high_scores')
        self.game.score_board.delete_high_scores(high_score_key)
        self.ui_options.show_high_scores = not self.ui_options.show_high_scores

    def create_button_actions_dict(self, menu_method, reset_method):
        """Create a dictionary mapping buttons to their corresponding actions."""
        return {
            self.play: lambda: self.handle_play_button(reset_method),
            self.menu: menu_method,
            self.quit: self.handle_quit_button,
            self.high_scores: self.handle_high_scores_button,
            self.game_modes: self.handle_game_modes_button,
            self.endless: self.handle_endless_button,
            self.meteor_madness: self.handle_meteor_madness_button,
            self.boss_rush: self.handle_boss_rush_button,
            self.last_bullet: self.handle_last_bullet_button,
            self.slow_burn: self.handle_slow_burn_button,
            self.normal: self.handle_normal_button,
            self.easy: self.handle_difficulty_button(DIFFICULTIES['EASY']),
            self.medium: self.handle_difficulty_button(DIFFICULTIES['MEDIUM']),
            self.hard: self.handle_difficulty_button(DIFFICULTIES['HARD']),
            self.difficulty: self.handle_difficulty_toggle,
            self.delete_scores: self.handle_delete_button,
        }
