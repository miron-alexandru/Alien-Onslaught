"""The sounds_manager module manages all music and sound effects in the game."""

import pygame

from utils.constants import LEVEL_SOUNDS, MENU_SOUNDS, GAME_SOUNDS
from utils.game_utils import load_sound_files, set_sounds_volume, play_sound


class SoundManager:
    """The SoundManager class manages different sounds in the game."""
    def __init__(self, game):
        self.game = game
        self.loading_screen = game.loading_screen
        self.stats = game.stats

        self.level_music = {}
        self.menu_sounds = {}
        self.game_sounds = {}
        self.current_sound = None

    def load_sounds(self, sounds_to_load):
        """Display the loading screen and load necessary sound files."""
        if sounds_to_load == 'level_sounds':
            while not self.level_music:
                self.loading_screen.update(25)
                self.level_music = load_sound_files(LEVEL_SOUNDS)
                self.loading_screen.update(50)
                self.game_sounds = load_sound_files(GAME_SOUNDS)
                self.loading_screen.update(100)
            set_sounds_volume(self.level_music, 0.05)
            set_sounds_volume(self.game_sounds, 0.2)
        elif sounds_to_load == 'menu_sounds':
            while not self.menu_sounds:
                self.loading_screen.update(50)
                self.menu_sounds = load_sound_files(MENU_SOUNDS)
                self.loading_screen.update(100)
            set_sounds_volume(self.menu_sounds, 0.2)

    def prepare_level_music(self):
        """Play the background music based on the current level."""
        current_sound_name = self.current_sound

        for key, sound_name in self.level_music.items():
            if self.stats.level in key:
                if sound_name != current_sound_name:
                    pygame.mixer.stop()
                    play_sound(self.level_music, key, loop=True)
                    self.current_sound = sound_name
                return
