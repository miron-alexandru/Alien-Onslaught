"""
The 'game_over_manager' module contains the EndGameManager class that manages 
game ending related tasks.
"""

from src.utils.game_utils import play_music
from src.utils.constants import GAME_MODE_SCORE_KEYS


class EndGameManager:
    """The EndGameManager class manages the end game functionality of a game."""

    def __init__(self, game, settings, stats, screen):
        self.game = game
        self.settings = settings
        self.stats = stats
        self.screen = screen
        self.ending_music = ""

    def check_game_over(self):
        """Check if the game is over and act accordingly."""
        if self.settings.game_modes.cosmic_conflict:
            self.ending_music = "victory"
            self._check_cosmic_conflict_endgame()
        if (
            self.settings.game_modes.boss_rush
            and self.stats.level == 15
            and not self.game.aliens
        ):
            self.ending_music = "victory"
            self._display_endgame("victory")
            self.game.score_board.render_high_score()
        elif not any(
            [self.game.thunderbird_ship.state.alive, self.game.phoenix_ship.state.alive]
        ):
            self.ending_music = "game_over"
            self._display_endgame("gameover")

    def _display_game_over(self):
        """Display the end game image on screen play the game over sound
        and save the high score for the active game mode."""
        self.game.bg_img = self.game.reset_bg
        self.set_game_end_position()
        self.screen.blit(self.settings.game_end_img, self.settings.game_end_rect)
        self.game.gameplay_manager.reset_game_objects()
        self.game.score_board.update_high_score()

        self._play_game_over_sound()

        if self.settings.game_modes.cosmic_conflict:
            self.game.gameplay_manager.set_cosmic_conflict_high_score()

        self._check_high_score_saved()

    def _play_game_over_sound(self):
        if not self.game.ui_options.game_over_sound_played:
            play_music(self.game.sound_manager.menu_music, self.ending_music)
            self.game.ui_options.game_over_sound_played = True
            self.game.sound_manager.current_sound = self.game.sound_manager.menu_music[
                self.ending_music
            ]

    def return_to_game_menu(self):
        """End the current game, save the current high score and return to game menu."""
        self.stats.game_active = False
        self.game.gameplay_manager.reset_game_objects()

    def set_game_end_position(self):
        """Set the location of the end game image on the screen"""
        self.settings.game_end_rect.centerx = self.settings.screen_width // 2
        self.settings.game_end_rect.centery = self.settings.screen_height // 2 - 250

    def _display_endgame(self, image_name):
        self.stats.game_active = False
        self.settings.game_end_img = self.settings.misc_images[image_name]
        self._display_game_over()

    def _check_cosmic_conflict_endgame(self):
        """Check which player won in Cosmic Conflict
        and display the appropriate end game.
        """
        if not self.game.thunderbird_ship.state.alive:
            self._display_endgame("phoenix_win")
        elif not self.game.phoenix_ship.state.alive:
            self._display_endgame("thunder_win")

    def _check_high_score_saved(self):
        """Save the high score for the current game_mode."""
        if not self.game.ui_options.high_score_saved:
            game_mode = self.settings.game_modes.game_mode or "normal"
            high_score_key = GAME_MODE_SCORE_KEYS.get(game_mode, "high_scores")
            self.game.high_score_manager.save_high_score(high_score_key)
            self.game.ui_options.high_score_saved = True
