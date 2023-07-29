"""
The 'sounds_manager' module contains the `SoundManager` class which manages
different sounds in the game. Additionally, it handles the loading of sound
files for usage throughout the game.
"""

import pygame

from src.utils.constants import (
    LEVEL_SOUNDS,
    MENU_SOUNDS,
    MENU_MUSIC,
    GAME_SOUNDS,
    BOSS_RUSH_MUSIC,
    ENDLESS_SOUNDTRACK,
    METEOR_MADNESS_MUSIC,
)
from src.utils.game_utils import (
    load_sound_files,
    set_sounds_volume,
    set_music_volume,
    load_music_files,
    play_music,
)


class SoundManager:
    """This class is responsible for loading and playing various
    sound effects and music.
    """

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.loading_screen = game.loading_screen
        self.stats = game.stats

        (
            self.menu_music,
            self.level_music,
            self.menu_sounds,
            self.game_sounds,
            self.boss_rush_levels,
            self.endless_music,
            self.meteor_music,
        ) = ({}, {}, {}, {}, {}, {}, {})

        self.current_sound = None

    def load_sounds(self, sounds_to_load):
        """Load necessary sound files."""
        if sounds_to_load == "gameplay_sounds":
            self._load_gameplay_sounds()
            self._set_multiple_music_volume(0.3)
            self._prepare_gameplay_sounds_volume()
        elif sounds_to_load == "menu_sounds":
            self.load_menu_sounds()
            set_music_volume(self.menu_music, 0.8)
            set_sounds_volume(self.menu_sounds, 0.7)

    def _load_gameplay_sounds(self):
        """Load the sound files for the level-specific music and game sounds
        while displaying the loading screen.
        """
        while not (self.level_music and self.game_sounds):
            self.loading_screen.update(25)
            self.level_music = load_music_files(LEVEL_SOUNDS)
            self.boss_rush_levels = load_music_files(BOSS_RUSH_MUSIC)
            self.endless_music = load_music_files(ENDLESS_SOUNDTRACK)
            self.meteor_music = load_music_files(METEOR_MADNESS_MUSIC)
            self.loading_screen.update(75)
            self.game_sounds = load_sound_files(GAME_SOUNDS)
            self.loading_screen.update(100)

    def load_menu_sounds(self):
        """Load the sound files for the menu while displaying the loading screen."""
        while not (self.menu_sounds and self.menu_music):
            self.loading_screen.update(25)
            self.menu_sounds = load_sound_files(MENU_SOUNDS)
            self.menu_music = load_music_files(MENU_MUSIC)
            self.loading_screen.update(100)

    def _set_level_music(self):
        """Determine the appropriate music dictionary
        based on the current game mode."""
        if self.settings.game_modes.boss_rush:
            return self.boss_rush_levels

        if self.settings.game_modes.endless_onslaught:
            return self.endless_music

        if self.settings.game_modes.meteor_madness:
            return self.meteor_music

        return self.level_music

    def prepare_level_music(self):
        """This method determines the appropriate background music
        to play based on the current game mode and level.
        """
        music_to_play = self._set_level_music()

        for key, sound_name in music_to_play.items():
            if self.stats.level in key:
                if sound_name != self.current_sound:
                    play_music(music_to_play, key)
                    self.current_sound = sound_name
                return

    def _prepare_gameplay_sounds_volume(self):
        """Prepare the volume for specific sounds."""
        self.game_sounds["bullet"].set_volume(0.1)
        self.game_sounds["alien_exploding"].set_volume(0.5)

    def _get_music_dicts(self):
        """Retrieve the dictionaries containing the loaded music files."""
        return {
            "level_music": self.level_music,
            "boss_rush_levels": self.boss_rush_levels,
            "endless_music": self.endless_music,
            "meteor_music": self.meteor_music,
        }

    def _set_multiple_music_volume(self, volume):
        """Set the volume of multiple game music items."""
        music_dicts = self._get_music_dicts()
        for music_dict in music_dicts.values():
            for _ in music_dict.values():
                pygame.mixer.music.set_volume(volume)
