"""
The 'screen_manager' module provides classes for managing the game screen.

Classes:
    - 'ScreenManager': Manages the screen after resizing, the game controls
    and the custom cursor.
    - 'LoadingScreen': Manages the loading screen for the game.
"""

import pygame
from utils.game_utils import display_controls


class ScreenManager:
    """Updates the position of game objects after resizing the screen,
    manages the custom cursor and creates the images and positions
    for the controls displayed on the game menu.
    """

    def __init__(self, settings, score_board, buttons, screen):
        self.settings = settings
        self.score_board = score_board
        self.buttons = buttons
        self.screen = screen
        self.player_controls = pygame.image.load(
            "../game_assets/images/buttons/player_controls.png"
        )
        self._initialize_cursor()
        self._create_controls()

    def update_buttons(self):
        """Updates the position of game objects after resizing the screen."""
        self.buttons.play.update_pos(self.screen.get_rect().center, y=-50)
        self.buttons.difficulty.update_pos(
            self.buttons.play.rect.centerx - 74, self.buttons.play.rect.bottom
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
            self.buttons.high_scores.rect.right - 10, self.buttons.high_scores.rect.y
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
            self.buttons.game_modes.rect.right - 10, self.buttons.game_modes.rect.y
        )
        self.buttons.endless.update_pos(
            self.buttons.normal.rect.right - 5, self.buttons.normal.rect.y
        )
        self.buttons.slow_burn.update_pos(
            self.buttons.endless.rect.right - 5, self.buttons.endless.rect.y
        )
        self.buttons.meteor_madness.update_pos(
            self.buttons.slow_burn.rect.right - 5, self.buttons.slow_burn.rect.y
        )
        self.buttons.boss_rush.update_pos(
            self.buttons.meteor_madness.rect.right - 5,
            self.buttons.meteor_madness.rect.y,
        )
        self.buttons.last_bullet.update_pos(
            self.buttons.boss_rush.rect.right - 5, self.buttons.boss_rush.rect.y
        )

        self.score_board.prep_level()
        self.score_board.render_scores()
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
        self.cursor_surface.blit(self.settings.cursor_img, (0, 0))
        self.screen.blit(self.cursor_surface, self.settings.cursor_rect)

    def _create_controls(self):
        """This method creates the images and positions
        for the controls that will be displayed on the game menu.
        """
        (
            self.p1_controls,
            self.p1_controls_rect,
            self.p2_controls,
            self.p2_controls_rect,
            self.t1_surfaces,
            self.t1_rects,
            self.t2_surfaces,
            self.t2_rects,
        ) = display_controls(self.player_controls, self.screen)


class LoadingScreen:
    """Manages the loading screen for the game,
    including updating the progress of the loading
    bar and drawing it on the screen.
    """

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.load_bar_width = 400
        self.load_bar_height = 25
        self.load_bar_x = (self.width - self.load_bar_width) // 2
        self.load_bar_y = (self.height - self.load_bar_height) // 2
        self.load_percent = 0
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render("Loading...", True, (255, 255, 255))

    def update(self, progress):
        """Update progress of the loading bar."""
        self.load_percent = progress
        self.draw()

    def draw(self):
        """Draw the loading screen on the screen."""
        self.screen.fill((2, 24, 49, 255))
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                self.load_bar_x,
                self.load_bar_y,
                self.load_bar_width,
                self.load_bar_height,
            ),
            2,
        )
        load_bar_fill = self.load_bar_width * self.load_percent // 100
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (self.load_bar_x, self.load_bar_y, load_bar_fill, self.load_bar_height),
        )
        self.screen.blit(
            self.text,
            (
                (self.width - self.text.get_width()) // 2,
                (self.height - self.text.get_height()) // 2 - 50,
            ),
        )
        pygame.display.update()
