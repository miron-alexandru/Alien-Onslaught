"""
The 'screen_manager' module provides the ScreenManager class used to manage
the screen, the game controls displayed, the custom cursor and
other screen related events.
"""

import pygame

from src.utils.game_utils import (
    display_controls,
    load_single_image,
    display_high_scores,
    resize_image,
)
from src.utils.constants import GAME_MODE_SCORE_KEYS


class ScreenManager:
    """Updates the position of game objects after resizing the screen,
    manages the custom cursor and creates the images and positions
    for the controls displayed on the game menu.
    """

    def __init__(
        self, game, settings, score_board, buttons_manager, screen, singleplayer
    ):
        self.game = game
        self.settings = settings
        self.score_board = score_board
        self.buttons = buttons_manager
        self.screen = screen
        self.player_controls = load_single_image("buttons/player_controls.png")
        self.screen_flag = pygame.RESIZABLE
        self.full_screen = False
        self.singleplayer = singleplayer
        self._initialize_cursor()
        self.create_controls()

    def update_buttons(self):
        """Updates the position of game objects after resizing the screen."""
        self.buttons.play.update_pos(self.screen.get_rect().center, y=-115)
        self.buttons.load_game.update_pos(
            self.buttons.play.rect.centerx - 74, self.buttons.play.rect.bottom
        )
        self.buttons.select_ship.update_pos(
            self.buttons.load_game.rect.centerx - 74, self.buttons.load_game.rect.bottom
        )
        self.buttons.difficulty.update_pos(
            self.buttons.select_ship.rect.centerx - 74,
            self.buttons.select_ship.rect.bottom,
        )
        self.buttons.game_modes.update_pos(
            self.buttons.difficulty.rect.centerx - 74,
            self.buttons.difficulty.rect.bottom,
        )
        self.buttons.high_scores.update_pos(
            self.buttons.game_modes.rect.centerx - 74,
            self.buttons.game_modes.rect.bottom,
        )
        self.buttons.delete_scores.update_pos(
            self.buttons.high_scores.rect.left - 85, self.buttons.high_scores.rect.y
        )
        self.buttons.menu.update_pos(
            self.buttons.high_scores.rect.centerx - 74,
            self.buttons.high_scores.rect.bottom,
        )
        self.buttons.quit.update_pos(
            self.buttons.menu.rect.centerx - 74, self.buttons.menu.rect.bottom
        )
        self.buttons.easy.update_pos(
            self.buttons.difficulty.rect.right - 10, self.buttons.difficulty.rect.y
        )
        self.buttons.medium.update_pos(
            self.buttons.easy.rect.right - 5, self.buttons.difficulty.rect.y
        )
        self.buttons.hard.update_pos(
            self.buttons.medium.rect.right - 5, self.buttons.difficulty.rect.y
        )
        self.buttons.normal.update_pos(
            self.buttons.game_modes.rect.right - 8, self.buttons.game_modes.rect.y
        )
        self.buttons.endless.update_pos(
            self.buttons.normal.rect.right - 5, self.buttons.normal.rect.y
        )
        self.buttons.slow_burn.update_pos(
            self.buttons.endless.rect.right - 5, self.buttons.endless.rect.y
        )
        self.buttons.cosmic_conflict.update_pos(
            self.buttons.slow_burn.rect.right - 5, self.buttons.slow_burn.rect.y
        )
        self.buttons.meteor_madness.update_pos(
            self.buttons.normal.rect.left, self.buttons.slow_burn.rect.bottom
        )
        self.buttons.boss_rush.update_pos(
            self.buttons.meteor_madness.rect.right - 5,
            self.buttons.meteor_madness.rect.y,
        )
        self.buttons.last_bullet.update_pos(
            self.buttons.boss_rush.rect.right - 5, self.buttons.boss_rush.rect.y
        )
        self.buttons.one_life_reign.update_pos(
            self.buttons.last_bullet.rect.right - 5, self.buttons.last_bullet.rect.y
        )
        # Update Menu Buttons
        self.buttons.single.update_pos(self.screen.get_rect().center, y=-80)
        self.buttons.multi.update_pos(
            self.buttons.single.rect.centerx - 100, self.buttons.single.rect.bottom
        )
        self.buttons.menu_quit.update_pos(
            self.buttons.multi.rect.centerx - 100, self.buttons.multi.rect.bottom
        )
        self.settings.game_title_rect.centerx = self.screen.get_rect().centerx
        # Update scoreboard
        self.score_board.prep_level()
        self.score_board.render_scores()
        self.score_board.render_missiles_num()
        self.score_board.render_high_score()
        self.score_board.create_health()
        self.score_board.render_bullets_num()

    def _initialize_cursor(self):
        """Set the normal cursor invisible and initialize the custom cursor."""
        pygame.mouse.set_visible(False)
        cursor_width, cursor_height = self.screen.get_size()
        self.cursor_surface = pygame.Surface(
            (cursor_width, cursor_height), pygame.SRCALPHA
        )

    def draw_cursor(self):
        """Draw the custom in the location of the normal cursor."""
        self.settings.cursor_rect.center = pygame.mouse.get_pos()
        self.cursor_surface.blit(self.settings.cursor_img, (5, 10))
        self.screen.blit(self.cursor_surface, self.settings.cursor_rect)

    def create_controls(self):
        """This method creates the images and positions
        for the controls that will be displayed on the game menu.
        """
        (
            self.p1_controls_img,
            self.p1_controls_img_rect,
            self.p2_controls_img,
            self.p2_controls_img_rect,
            self.p1_controls_text,
            self.p1_controls_text_rects,
            self.p2_controls_text,
            self.p2_controls_text_rects,
            self.game_controls_img,
            self.game_controls_img_rect,
            self.game_controls_text,
            self.game_controls_text_rects,
        ) = display_controls(self.player_controls, self.screen)

    def draw_menu_objects(self, bg_img, bg_img_rect):
        """Draw the buttons, game title and controls on the menu screen"""
        self.screen.blit(bg_img, bg_img_rect)
        self.screen.blit(self.p1_controls_img, self.p1_controls_img_rect)
        self.screen.blit(self.p2_controls_img, self.p2_controls_img_rect)
        self.screen.blit(self.game_controls_img, self.game_controls_img_rect)
        self.screen.blit(self.settings.game_title, self.settings.game_title_rect)
        self.buttons.single.draw_button()
        self.buttons.multi.draw_button()
        self.buttons.menu_quit.draw_button()

        for i, surface in enumerate(self.p1_controls_text):
            self.screen.blit(surface, self.p1_controls_text_rects[i])

        for i, surface in enumerate(self.p2_controls_text):
            self.screen.blit(surface, self.p2_controls_text_rects[i])

        for i, surface in enumerate(self.game_controls_text):
            self.screen.blit(surface, self.game_controls_text_rects[i])

    def display_high_scores_on_screen(self):
        """Display the high scores for the current game mode active"""
        game_mode = self.settings.game_modes.game_mode or "normal"
        high_score_key = GAME_MODE_SCORE_KEYS[game_mode]
        display_high_scores(self, self.screen, high_score_key)

    def display_pause(self):
        """Display the pause screen."""
        pause_rect = self.settings.pause.get_rect()
        pause_rect.centerx = self.screen.get_rect().centerx
        pause_rect.centery = self.screen.get_rect().centery
        self.screen.blit(self.settings.pause, pause_rect)

    def update_window_mode(self):
        """Update window mode based on the screen flag"""
        info = pygame.display.Info()
        self.screen_flag = pygame.FULLSCREEN if self.full_screen else pygame.RESIZABLE
        if self.game.ui_options.resizable:
            pygame.display.set_mode((info.current_w, info.current_h), self.screen_flag)
            self.game.ui_options.resizable = False

    def toggle_window_mode(self):
        """Toggle window mode from FULLSCREEN to RESIZABLE"""
        self.full_screen = not self.full_screen
        self.game.ui_options.resizable = not self.game.ui_options.resizable

    def resize_screen(self, size):
        """Resize the game screen and update relevant game objects.
        Screen has max width and max height."""
        min_width, min_height = 1260, 700
        max_width, max_height = 1920, 1080
        width = max(min(size[0], max_width), min_width)
        height = max(min(size[1], max_height), min_height)
        size = (width, height)

        self.screen = pygame.display.set_mode(size, self.screen_flag)

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.game.bg_img = resize_image(self.game.bg_img)
        self.game.second_bg = resize_image(self.settings.second_bg)
        self.game.third_bg = resize_image(self.settings.third_bg)
        self.game.fourth_bg = resize_image(self.settings.fourth_bg)
        self.game.reset_bg = resize_image(self.settings.bg_img)

        self.game.game_over_manager.set_game_end_position()
        self.game.save_load_manager.update_rect_positions()
        self.game.save_load_manager.set_screen_title_position()

        for ship in self.game.ships:
            ship.screen_rect = self.screen.get_rect()
            ship.set_cosmic_conflict_pos()
