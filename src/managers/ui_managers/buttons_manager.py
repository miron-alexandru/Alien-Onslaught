"""
The buttons_manager module provides the GameButtonsManager class that handles the
behavior and creation of the buttons in the game.
"""

import sys
import pygame

from src.ui.button import Button

from src.utils.constants import (
    BUTTON_NAMES,
    GAME_MODE_SCORE_KEYS,
    DIFFICULTIES,
    GAME_MODES_DESCRIPTIONS,
)
from src.utils.game_utils import load_button_imgs, play_sound


class GameButtonsManager:
    """This class creates the buttons for the game.
    Contains the methods for handling every button action.
    """

    def __init__(self, game, screen, ui_options, gm_options):
        self.screen = screen
        self.game = game
        self.settings = game.settings
        self.ui_options = ui_options
        self.gm_options = gm_options
        self.screen_rect = self.screen.get_rect()

        self.button_imgs = load_button_imgs(BUTTON_NAMES)

        self._create_game_buttons()
        self._create_menu_buttons()

    def _create_game_buttons(self):
        """Create buttons for the game menu."""
        self.play = Button(self, self.button_imgs["play_button"], (0, 0), center=True)
        self.load_game = Button(
            self,
            self.button_imgs["load_game"],
            (self.play.rect.centerx - 74, self.play.rect.bottom),
        )
        self.select_ship = Button(
            self,
            self.button_imgs["select_ship"],
            (self.load_game.rect.centerx - 74, self.load_game.rect.bottom),
        )
        # Difficulty buttons
        self.difficulty = Button(
            self,
            self.button_imgs["difficulty"],
            (self.select_ship.rect.centerx - 74, self.select_ship.rect.bottom),
        )
        self.easy = Button(
            self,
            self.button_imgs["easy"],
            (self.difficulty.rect.right - 10, self.difficulty.rect.y),
        )
        self.medium = Button(
            self,
            self.button_imgs["medium"],
            (self.easy.rect.right - 5, self.easy.rect.y),
        )
        self.hard = Button(
            self,
            self.button_imgs["hard"],
            (self.medium.rect.right - 5, self.medium.rect.y),
        )

        # Game mode buttons
        self.game_modes = Button(
            self,
            self.button_imgs["game_modes"],
            (self.difficulty.rect.centerx - 74, self.difficulty.rect.bottom),
        )
        self.normal = Button(
            self,
            self.button_imgs["normal"],
            (self.game_modes.rect.right - 8, self.game_modes.rect.y),
            GAME_MODES_DESCRIPTIONS[0],
        )
        self.endless = Button(
            self,
            self.button_imgs["endless"],
            (self.normal.rect.right - 5, self.normal.rect.y),
            GAME_MODES_DESCRIPTIONS[1],
        )
        self.slow_burn = Button(
            self,
            self.button_imgs["slow_burn"],
            (self.endless.rect.right - 5, self.endless.rect.y),
            GAME_MODES_DESCRIPTIONS[2],
        )
        self.meteor_madness = Button(
            self,
            self.button_imgs["meteor_madness"],
            (self.normal.rect.left, self.slow_burn.rect.bottom),
            GAME_MODES_DESCRIPTIONS[3],
        )
        self.boss_rush = Button(
            self,
            self.button_imgs["boss_rush"],
            (self.meteor_madness.rect.right - 5, self.meteor_madness.rect.y),
            GAME_MODES_DESCRIPTIONS[4],
        )
        self.last_bullet = Button(
            self,
            self.button_imgs["last_bullet"],
            (self.boss_rush.rect.right - 5, self.boss_rush.rect.y),
            GAME_MODES_DESCRIPTIONS[5],
        )
        self.cosmic_conflict = Button(
            self,
            self.button_imgs["cosmic_conflict"],
            (self.slow_burn.rect.right - 5, self.slow_burn.rect.y),
            GAME_MODES_DESCRIPTIONS[6],
        )
        self.one_life_reign = Button(
            self,
            self.button_imgs["one_life_reign"],
            (self.last_bullet.rect.right - 5, self.last_bullet.rect.y),
            GAME_MODES_DESCRIPTIONS[7],
        )

        # High scores and other game menu buttons
        self.high_scores = Button(
            self,
            self.button_imgs["high_scores"],
            (self.game_modes.rect.centerx - 74, self.game_modes.rect.bottom),
        )
        self.delete_scores = Button(
            self,
            self.button_imgs["delete_scores"],
            (self.high_scores.rect.left - 85, self.high_scores.rect.y),
        )
        self.menu = Button(
            self,
            self.button_imgs["menu_button"],
            (self.high_scores.rect.centerx - 74, self.high_scores.rect.bottom),
        )
        self.quit = Button(
            self,
            self.button_imgs["quit_button"],
            (self.menu.rect.centerx - 74, self.menu.rect.bottom),
        )

        # Lists containing the game buttons, difficulty buttons and game mode buttons
        self.game_buttons = [
            self.play,
            self.quit,
            self.menu,
            self.load_game,
            self.select_ship,
            self.difficulty,
            self.high_scores,
            self.game_modes,
        ]
        self.difficulty_buttons = [self.easy, self.medium, self.hard]
        self.game_mode_buttons = [
            self.endless,
            self.normal,
            self.slow_burn,
            self.meteor_madness,
            self.boss_rush,
            self.last_bullet,
            self.cosmic_conflict,
            self.one_life_reign,
        ]

    def _create_menu_buttons(self):
        """Create the buttons for the main menu."""
        self.single = Button(
            self,
            self.button_imgs["single_player"],
            (0, 0),
            center=False,
            menu_button=True,
        )
        self.multi = Button(
            self,
            self.button_imgs["multiplayer"],
            (self.single.rect.centerx - 100, self.single.rect.bottom),
        )
        self.menu_quit = Button(
            self,
            self.button_imgs["menu_quit_button"],
            (self.multi.rect.centerx - 100, self.multi.rect.bottom),
        )

    def display_description(self):
        """Display the description of the game mode button currently
        hovered over by the mouse cursor.
        """
        for button in self.game_mode_buttons:
            # Create a smaller rectangle for collision detection
            # to avoid triggering for adjacent buttons
            collision_rect = button.rect.inflate(-5, 0)
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
        self.ui_options.ship_selection = False

    def handle_quit_button(self):
        """Play the quit sound effect and quit the game."""
        self.game.sound_manager.game_sounds["quit_effect"].play()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()

    def handle_high_scores_button(self):
        """Toggle the visibility of the high score."""
        self.ui_options.show_high_scores = not self.ui_options.show_high_scores

    def handle_game_modes_button(self):
        """Toggle the visibility of the game modes."""
        self.ui_options.show_game_modes = not self.ui_options.show_game_modes

    def handle_load_game_button(self):
        self.game.save_load_manager.handle_save_load_menu()

    def _set_game_mode_settings(self, game_mode_setting):
        """Helper function to set the game mode settings based on the current mode."""
        self.gm_options.endless_onslaught = False
        self.gm_options.slow_burn = False
        self.gm_options.meteor_madness = False
        self.gm_options.boss_rush = False
        self.gm_options.last_bullet = False
        self.gm_options.cosmic_conflict = False
        self.gm_options.one_life_reign = False

        if game_mode_setting is not None:
            setattr(self.gm_options, game_mode_setting, True)

    def handle_endless_button(self):
        """Toggle the Endless game mode setting and hide game mode buttons."""
        self._set_game_mode("endless_onslaught", "endless_onslaught")

    def handle_normal_button(self):
        """Turn all game modes off, play the normal game."""
        self._set_game_mode(None, "normal")

    def handle_slow_burn_button(self):
        """Toggle the Slow Burn game mode and hide game mode buttons."""
        self._set_game_mode("slow_burn", "slow_burn")

    def handle_meteor_madness_button(self):
        """Toggle the Meteor Madness game mode and hide all game mode buttons."""
        self._set_game_mode("meteor_madness", "meteor_madness")

    def handle_boss_rush_button(self):
        """Toggle the Boss Rush game mode and hide all game mode buttons."""
        self._set_game_mode("boss_rush", "boss_rush")

    def handle_last_bullet_button(self):
        """Toggle the Last Bullet game mode and hide all game mode buttons."""
        self._set_game_mode("last_bullet", "last_bullet")

    def handle_one_life_reign_button(self):
        """Toggle the One Life Reign game mode and hide all game mode buttons."""
        self._set_game_mode("one_life_reign", "one_life_reign")

    def handle_cosmic_conflict_button(self):
        """Toggle the Cosmic Conflict game mode and hide all game mode buttons."""
        if self.game.singleplayer:
            return
        for ship in self.game.ships:
            ship.state.alive = True
        self._set_game_mode("cosmic_conflict", "cosmic_conflict")

    def _set_game_mode(self, game_mode_setting, selected_game_mode):
        """Set the current game mode and hide UI."""
        self._set_game_mode_settings(game_mode_setting)
        self.gm_options.game_mode = selected_game_mode
        self.ui_options.show_game_modes = False

    def handle_difficulty_button(self, speedup_scale, max_alien_speed):
        """Set the game difficulty (speed-up scale)."""

        def handle():
            """Set the speedup scale and hide the difficulty options UI."""
            self.game.settings.speedup_scale = speedup_scale
            self.game.settings.max_alien_speed = max_alien_speed
            self.ui_options.show_difficulty = False

        return handle

    def handle_difficulty_toggle(self):
        """Toggle visibility of the difficulty buttons."""
        self.ui_options.show_difficulty = not self.ui_options.show_difficulty

    def handle_delete_button(self):
        """Delete all high scores for the current game mode."""
        game_mode = self.game.settings.game_modes.game_mode or "normal"
        high_score_key = GAME_MODE_SCORE_KEYS.get(game_mode, "high_scores")
        self.game.high_score_manager.delete_high_scores(high_score_key)
        self.ui_options.show_high_scores = not self.ui_options.show_high_scores

    def create_button_actions_dict(self, menu_method, reset_game):
        """Create a dictionary mapping buttons to their corresponding actions."""
        return {
            self.play: lambda: self.handle_play_button(reset_game),
            self.menu: menu_method,
            self.quit: self.handle_quit_button,
            self.high_scores: self.handle_high_scores_button,
            self.game_modes: self.handle_game_modes_button,
            self.endless: self.handle_endless_button,
            self.meteor_madness: self.handle_meteor_madness_button,
            self.boss_rush: self.handle_boss_rush_button,
            self.last_bullet: self.handle_last_bullet_button,
            self.slow_burn: self.handle_slow_burn_button,
            self.cosmic_conflict: self.handle_cosmic_conflict_button,
            self.one_life_reign: self.handle_one_life_reign_button,
            self.normal: self.handle_normal_button,
            self.easy: self.handle_difficulty_button(
                DIFFICULTIES["EASY"], DIFFICULTIES["MAX_EASY"]
            ),
            self.medium: self.handle_difficulty_button(
                DIFFICULTIES["MEDIUM"], DIFFICULTIES["MAX_MEDIUM"]
            ),
            self.hard: self.handle_difficulty_button(
                DIFFICULTIES["HARD"], DIFFICULTIES["MAX_HARD"]
            ),
            self.difficulty: self.handle_difficulty_toggle,
            self.delete_scores: self.handle_delete_button,
            self.select_ship: self.handle_ship_selection_button,
            self.load_game: self.handle_load_game_button,
        }

    def handle_quit_event(self):
        """Handle the quit event by quitting the pygame and exiting the program."""
        pygame.quit()
        sys.exit()

    def handle_single_player_button_click(self, start_single):
        """Handle the event when the single player button is clicked.
        Play a menu click sound and start a single player game.
        """
        play_sound(self.game.sound_manager.menu_sounds, "click_menu")
        start_single()

    def handle_multiplayer_button_click(self, start_multi):
        """Handle the event when the multiplayer button is clicked.
        Play a menu click sound and start a multiplayer game.
        """
        play_sound(self.game.sound_manager.menu_sounds, "click_menu")
        start_multi()

    def handle_quit_button_click(self):
        """Handle the event when the quit button is clicked."""
        play_sound(self.game.sound_manager.menu_sounds, "quit_effect")
        pygame.time.delay(800)
        self.handle_quit_event()

    def handle_ship_selection_button(self):
        """Handle the even when the ship selection button
        is clicked.
        """
        self.ui_options.ship_selection = not self.ui_options.ship_selection
        self.game.thunderbird_ship.ship_selected = False
        self.game.phoenix_ship.ship_selected = False
