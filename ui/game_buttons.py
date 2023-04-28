"""
This module provides a class `GameButtons` that creates and manages
the buttons and displays the controls used in the game.
"""
import sys
import pygame
import pygame.font

from utils.constants import BUTTON_NAMES, GAME_MODE_SCORE_KEYS, DIFFICULTIES
from utils.game_utils import load_button_imgs, display_controls


class Button:
    """A class that manages the button"""
    def __init__(self, game, image_loc, pos, center=False):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.visible = False  # variable used for buttons that need to be visible

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
        """Draws the button if it is visible."""
        self.screen.blit(self.image, self.rect)



class GameButtons:
    """This class creates the buttons for the game.
    Contains the methods for handling every button action, 
    and displays the controls in the game menu"""
    def __init__(self, game, screen, ui_options, gm_options):
        self.screen = screen
        self.game = game
        self.ui_options = ui_options
        self.gm_options = gm_options
        self.screen_rect = self.screen.get_rect()

        self.button_imgs = load_button_imgs(BUTTON_NAMES)

        self._create_controls()
        self._create_game_buttons()
        self._create_menu_buttons()

    def _create_game_buttons(self):
        """Create buttons for the game"""
        self.play = Button(self, self.button_imgs["play_button"],(0, 0), center=True)
        self.difficulty = Button(self, self.button_imgs["difficulty"],
                            (self.play.rect.centerx - 74, self.play.rect.bottom))
        self.game_modes = Button(self, self.button_imgs["game_modes"],
                            (self.difficulty.rect.centerx - 74, self.difficulty.rect.bottom))
        self.normal = Button(self, self.button_imgs["normal"],
                            (self.game_modes.rect.right - 10, self.game_modes.rect.y))
        self.endless = Button(self, self.button_imgs["endless"],
                            (self.normal.rect.right - 5, self.normal.rect.y))
        self.slow_burn = Button(self, self.button_imgs["slow_burn"],
                            (self.endless.rect.right - 5, self.endless.rect.y))
        self.meteor_madness = Button(self, self.button_imgs['meteor_madness'],
                            (self.slow_burn.rect.right - 5, self.slow_burn.rect.y))
        self.boss_rush = Button(self, self.button_imgs['boss_rush'],
                            (self.meteor_madness.rect.right - 5, self.meteor_madness.rect.y))
        self.last_bullet = Button(self, self.button_imgs['last_bullet'],
                            (self.boss_rush.rect.right - 5, self.boss_rush.rect.y))
        self.high_scores = Button(self, self.button_imgs['high_scores'],
                            (self.game_modes.rect.centerx - 74, self.game_modes.rect.bottom))
        self.delete_scores = Button(self, self.button_imgs['delete_scores'],
                            (self.high_scores.rect.right - 10, self.high_scores.rect.y))
        self.menu = Button(self, self.button_imgs["menu_button"],
                            (self.high_scores.rect.centerx - 74, self.high_scores.rect.bottom))
        self.quit = Button(self, self.button_imgs["quit_button"],
                            (self.menu.rect.centerx - 74, self.menu.rect.bottom))
        self.easy = Button(self, self.button_imgs['easy'], (self.difficulty.rect.right - 10,
                                                            self.difficulty.rect.y))
        self.medium = Button(self, self.button_imgs['medium'], (self.easy.rect.right - 5,
                                                            self.easy.rect.y))
        self.hard = Button(self, self.button_imgs['hard'], (self.medium.rect.right - 5,
                                                            self.medium.rect.y))
        self.game_buttons = [self.play, self.quit, self.menu, self.difficulty, self.high_scores,
                            self.game_modes]
        self.difficulty_buttons = [self.easy, self.medium, self.hard]
        self.game_mode_buttons = [self.endless, self.normal, self.slow_burn, self.meteor_madness,
                                self.boss_rush, self.last_bullet]

    def draw_difficulty_buttons(self):
        """Draw difficulty buttons on screen."""
        for button in self.difficulty_buttons:
            button.draw_button()

    def draw_game_mode_buttons(self):
        """Draw game mode buttons on screen."""
        for button in self.game_mode_buttons:
            button.draw_button()

    def draw_buttons(self):
        """Draw buttons on screen."""
        for button in self.game_buttons:
            button.draw_button()

    def _create_menu_buttons(self):
        """Create the buttons for the game menu"""
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

    def _create_controls(self):
        """This method creates the images and positions
        for the controls that will be displayed on the game menu."""
        (self.p1_controls, self.p1_controls_rect,
         self.p2_controls, self.p2_controls_rect,
         self.t1_surfaces, self.t1_rects,
         self.t2_surfaces, self.t2_rects) = display_controls(self.button_imgs, self.screen)

    def handle_play_button(self, reset_game):
        """Reset game and hide all buttons"""
        reset_game()
        self.ui_options.show_difficulty = False
        self.ui_options.show_high_scores = False
        self.ui_options.show_game_modes = False

    def handle_quit_button(self):
        """Quit game"""
        self.game.game_sounds['quit_effect'].play()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()

    def handle_high_scores_button(self):
        """Toggle the visibility of the high score"""
        self.ui_options.show_high_scores = not self.ui_options.show_high_scores

    def handle_game_modes_button(self):
        """Toggle the visibility of the game modes"""
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
        """Toggle the Endless game mode setting and hide game mode buttons"""
        self.gm_options.endless_onslaught = not self.gm_options.endless_onslaught
        self._set_game_mode_settings('endless_onslaught')
        self.gm_options.game_mode = 'endless_onslaught'
        self.ui_options.show_game_modes = False

    def handle_normal_button(self):
        """Turn all game modes off, play the normal game"""
        self._set_game_mode_settings(None)
        self.gm_options.game_mode = 'normal'
        self.ui_options.show_game_modes = False

    def handle_slow_burn_button(self):
        """Toggle the Slow Burn game mode and hide game mode buttons"""
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
        """Set the game difficulty (speed-up scale)"""
        def handle():
            self.game.settings.speedup_scale = speedup_scale
            self.ui_options.show_difficulty = False
        return handle

    def handle_difficulty_toggle(self):
        """Toggle visibility of the difficulty buttons"""
        self.ui_options.show_difficulty = not self.ui_options.show_difficulty

    def handle_delete_button(self):
        """Delete all high scores for the current game mode."""
        game_mode = self.game.settings.gm.game_mode or 'normal'
        high_score_key = GAME_MODE_SCORE_KEYS.get(game_mode, 'high_scores')
        self.game.score_board.delete_high_scores(high_score_key)

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
