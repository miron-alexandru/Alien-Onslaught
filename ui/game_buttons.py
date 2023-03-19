"""
This module provides a class `GameButtons` that creates and manages
the buttons and displays the controls used in the game.
"""
import sys
import pygame
import pygame.font

from utils.constants import BUTTON_NAMES
from utils.game_utils import load_button_imgs, display_controls



class Button:
    """A class that manages the button"""
    def __init__(self, game, image_loc, pos, center=False):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Load button image and scale it to the desired size.
        self.image = pygame.image.load(image_loc)

        # Build the button's rect object and set its position.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        if center:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.x, self.rect.y = pos


    def update_pos(self, *args):
        """Update the button's position."""
        if len(args) == 1:
            self.rect.center = args[0]
        elif len(args) == 2:
            self.rect.topleft = args

    def draw_button(self):
        """Draws the button"""
        self.screen.blit(self.image, self.rect)


class GameButtons:
    """This class creates the buttons for the game.
    Contains the methods for handling every button action, 
    and displays the controls in the game menu"""
    def __init__(self, game, screen):
        self.screen = screen
        self.game = game
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
        self.last_stand = Button(self, self.button_imgs["last_stand"],
                            (self.endless.rect.right - 5, self.endless.rect.y))
        self.high_scores = Button(self, self.button_imgs['high_scores'],
                            (self.game_modes.rect.centerx - 74, self.game_modes.rect.bottom))
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

    def _create_menu_buttons(self):
        """Create the buttons for the game menu"""
        self.single = Button(self, self.button_imgs["single_player"], (0, 0), center=True)
        self.multi = Button(self, self.button_imgs["multiplayer"],
                            (self.single.rect.centerx - 100, self.single.rect.bottom))
        self.menu_quit = Button(self, self.button_imgs["menu_quit_button"],
                            (self.multi.rect.centerx - 100, self.multi.rect.bottom))


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
        self.game.show_difficulty = False
        self.game.show_high_scores = False
        self.game.show_game_modes = False


    def handle_quit_button(self):
        """Quit game"""
        pygame.quit()
        sys.exit()


    def handle_high_scores_button(self):
        """Toggle the visibility of the high score"""
        self.game.show_high_scores = not self.game.show_high_scores


    def handle_game_modes_button(self):
        """Toggle the visibility of the game modes"""
        self.game.show_game_modes = not self.game.show_game_modes


    def handle_endless_button(self):
        """Toggle the endless game mode setting and hide game mode buttons"""
        self.game.settings.endless = not self.game.settings.endless
        self.game.settings.last_stand = False
        self.game.show_game_modes = False

    def handle_normal_button(self):
        """Turn all game modes off, play the normal game"""
        self.game.settings.endless = False
        self.game.settings.last_stand = False
        self.game.show_game_modes = False


    def handle_last_stand_button(self):
        """Toggle the last stand game mode and hide game mode buttons"""
        self.game.settings.last_stand = not self.game.settings.last_stand
        self.game.settings.endless = False
        self.game.show_game_modes = False

    def handle_difficulty_button(self, speedup_scale):
        """Set the game difficulty (speed-up scale)"""
        def handle():
            self.game.settings.speedup_scale = speedup_scale
            self.game.show_difficulty = False
        return handle


    def handle_difficulty_toggle(self):
        """Toggle visibility of the difficulty buttons"""
        self.game.show_difficulty = not self.game.show_difficulty
