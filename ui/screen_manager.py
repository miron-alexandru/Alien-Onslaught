"""This module contains a class that updates the position of different objects
in the game"""


class ScreenManager:
    """This class updates the position of objects after resizing the screen."""
    def __init__(self, settings, score_board, buttons, screen):
        self.settings = settings
        self.score_board = score_board
        self.buttons = buttons
        self.screen = screen

    def update_buttons(self):
        """Update the position of objects after resize"""
        self.buttons.play.update_pos(self.screen.get_rect().center)
        self.buttons.difficulty.update_pos(self.buttons.play.rect.centerx - 74,
                                    self.buttons.play.rect.bottom)
        self.buttons.game_modes.update_pos(self.buttons.difficulty.rect.centerx - 74,
                                    self.buttons.difficulty.rect.bottom)
        self.buttons.high_scores.update_pos(self.buttons.game_modes.rect.centerx -74,
                                    self.buttons.game_modes.rect.bottom)
        self.buttons.menu.update_pos(self.buttons.high_scores.rect.centerx - 74,
                                     self.buttons.high_scores.rect.bottom)
        self.buttons.quit.update_pos(self.buttons.menu.rect.centerx - 74,
                                     self.buttons.menu.rect.bottom)
        self.buttons.easy.update_pos(self.buttons.difficulty.rect.right - 10,
                                    self.buttons.difficulty.rect.y)
        self.buttons.medium.update_pos(self.buttons.easy.rect.right - 5,
                                    self.buttons.difficulty.rect.y)
        self.buttons.hard.update_pos(self.buttons.medium.rect.right - 5,
                                    self.buttons.difficulty.rect.y)
        self.buttons.normal.update_pos(self.buttons.game_modes.rect.right - 10,
                                    self.buttons.game_modes.rect.y)
        self.buttons.endless.update_pos(self.buttons.normal.rect.right - 5,
                                    self.buttons.normal.rect.y)
        self.buttons.slow_burn.update_pos(self.buttons.endless.rect.right -5,
                                    self.buttons.endless.rect.y)
        self.buttons.meteor_madness.update_pos(self.buttons.slow_burn.rect.right -5,
                                    self.buttons.slow_burn.rect.y)
        self.buttons.boss_rush.update_pos(self.buttons.meteor_madness.rect.right - 5,
                                    self.buttons.meteor_madness.rect.y)
        self.score_board.prep_level()
        self.score_board.render_scores()
        self.score_board.render_high_score()
        self.score_board.create_health()
