"""
This module tests the SoundManager class which manages the sounds
in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.managers.sounds_manager import SoundManager


class TestSoundManager(unittest.TestCase):
    """Test cases for the SoundManager class."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.sound_manager = SoundManager(self.game)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.sound_manager.settings, self.game.settings)
        self.assertEqual(self.sound_manager.game, self.game)
        self.assertEqual(self.sound_manager.loading_screen, self.game.loading_screen)
        self.assertEqual(self.sound_manager.stats, self.game.stats)
        self.assertIsNone(self.sound_manager.current_sound)
        self.assertEqual(self.sound_manager.menu_music, {})
        self.assertEqual(self.sound_manager.level_music, {})
        self.assertEqual(self.sound_manager.menu_sounds, {})
        self.assertEqual(self.sound_manager.game_sounds, {})
        self.assertEqual(self.sound_manager.boss_rush_levels, {})
        self.assertEqual(self.sound_manager.endless_music, {})
        self.assertEqual(self.sound_manager.meteor_music, {})

    def test_load_sounds_gameplay_sounds(self):
        """Test the loading of the gameplay sounds."""
        self.sound_manager._load_gameplay_sounds = MagicMock()
        self.sound_manager._set_multiple_music_volume = MagicMock()
        self.sound_manager._prepare_gameplay_sounds_volume = MagicMock()

        self.sound_manager.load_sounds("gameplay_sounds")

        self.sound_manager._load_gameplay_sounds.assert_called_once()
        self.sound_manager._set_multiple_music_volume.assert_called_with(0.3)
        self.sound_manager._prepare_gameplay_sounds_volume.assert_called_once()

    @patch("src.managers.sounds_manager.set_music_volume")
    @patch("src.managers.sounds_manager.set_sounds_volume")
    def test_load_sounds_menu_sounds(
        self, mock_set_sounds_volume, mock_set_music_volume
    ):
        """Test the loading of the menu sounds."""
        self.sound_manager.load_menu_sounds = MagicMock()

        self.sound_manager.load_sounds("menu_sounds")

        self.sound_manager.load_menu_sounds.assert_called_once()
        mock_set_music_volume.assert_called_with(self.sound_manager.menu_music, 0.8)
        mock_set_sounds_volume.assert_called_with(self.sound_manager.menu_sounds, 0.7)

    @patch("src.managers.sounds_manager.load_music_files")
    @patch("src.managers.sounds_manager.load_sound_files")
    def test__load_gameplay_sounds(self, mock_load_sound_files, mock_load_music_files):
        """Test the load_gameplay_sounds method."""
        self.sound_manager._load_gameplay_sounds()

        self.assertEqual(mock_load_music_files.call_count, 4)
        self.assertEqual(mock_load_sound_files.call_count, 1)

        self.assertEqual(self.sound_manager.level_music, mock_load_music_files())
        self.assertEqual(self.sound_manager.boss_rush_levels, mock_load_music_files())
        self.assertEqual(self.sound_manager.endless_music, mock_load_music_files())
        self.assertEqual(self.sound_manager.meteor_music, mock_load_music_files())
        self.assertEqual(self.sound_manager.game_sounds, mock_load_sound_files())
        self.sound_manager.loading_screen.update.assert_called_with(100)

    @patch("src.managers.sounds_manager.load_music_files")
    @patch("src.managers.sounds_manager.load_sound_files")
    def test_load_menu_sounds(self, mock_load_sound_files, mock_load_music_files):
        """Test for the loading of the menu sounds."""
        self.sound_manager.load_menu_sounds()

        self.assertEqual(mock_load_music_files.call_count, 1)
        self.assertEqual(mock_load_sound_files.call_count, 1)

        self.assertEqual(self.sound_manager.menu_sounds, mock_load_sound_files())
        self.assertEqual(self.sound_manager.menu_music, mock_load_music_files())
        self.sound_manager.loading_screen.update.assert_called_with(100)

    def test__set_level_music_boss_rush_mode(self):
        """Test the music dictionary assignment for the boss rush game mode."""
        self.sound_manager.settings.game_modes.boss_rush = True

        self.assertEqual(
            self.sound_manager._set_level_music(), self.sound_manager.boss_rush_levels
        )

    def test__set_level_music_endless_onslaught_mode(self):
        """Test the music dictionary assignment for the endless onslaught game mode."""
        self.sound_manager.settings.game_modes.endless_onslaught = True

        self.assertEqual(
            self.sound_manager._set_level_music(), self.sound_manager.endless_music
        )

    def test__set_level_music_meteor_madness_mode(self):
        """Test the music dictionary assignment for the meteor madness game mode."""
        self.sound_manager.settings.game_modes.meteor_madness = True

        self.assertEqual(
            self.sound_manager._set_level_music(), self.sound_manager.meteor_music
        )

    def test__set_level_music_default(self):
        """Test the default level music dictionary assignment."""
        self.assertEqual(
            self.sound_manager._set_level_music(), self.sound_manager.level_music
        )

    def test_prepare_level_music_current_sound_is_none(self):
        """Test case for the prepare level music when the
        music to be played is None."""
        self.sound_manager._set_level_music = MagicMock(
            return_value=self.sound_manager.level_music
        )

        self.sound_manager.current_sound = None
        self.sound_manager.level_music[range(1, 8)] = "path_to_sound_file"
        self.sound_manager.stats.level = 1

        with patch("src.managers.sounds_manager.play_music") as mock_play_music:
            self.sound_manager.prepare_level_music()

        mock_play_music.assert_called_with(self.sound_manager.level_music, range(1, 8))
        self.assertEqual(self.sound_manager.current_sound, "path_to_sound_file")

    def test_prepare_level_music_no_change(self):
        """Test case for the  prepare level music when the
        music to be played is already the current sound.
        """
        self.sound_manager._set_level_music = MagicMock(
            return_value=self.sound_manager.level_music
        )
        self.sound_manager.current_sound = "path_to_sound_file"
        self.sound_manager.level_music[range(1, 8)] = "path_to_sound_file"
        self.sound_manager.stats.level = 1

        with patch("src.managers.sounds_manager.play_music") as mock_play_music:
            self.sound_manager.prepare_level_music()

        mock_play_music.assert_not_called()

    def test_prepare_level_music_change(self):
        """Test case for the prepare level music when the
        music to be played is not the current sound.
        """
        self.sound_manager._set_level_music = MagicMock(
            return_value=self.sound_manager.level_music
        )
        self.sound_manager.current_sound = "path_to_sound_file2"
        self.sound_manager.level_music[range(1, 8)] = "path_to_sound_file"
        self.sound_manager.stats.level = 5

        with patch("src.managers.sounds_manager.play_music") as mock_play_music:
            self.sound_manager.prepare_level_music()

        mock_play_music.assert_called_with(self.sound_manager.level_music, range(1, 8))
        self.assertEqual(self.sound_manager.current_sound, "path_to_sound_file")

    def test__prepare_gameplay_sounds_volume(self):
        """Test the preparation of the gameplay sound volume."""
        self.sound_manager.game_sounds = {
            "bullet": MagicMock(return_value=pygame.mixer.Sound),
            "alien_exploding": MagicMock(return_value=pygame.mixer.Sound),
        }
        self.sound_manager._prepare_gameplay_sounds_volume()

        self.sound_manager.game_sounds["bullet"].set_volume.assert_called_with(0.1)
        self.sound_manager.game_sounds["alien_exploding"].set_volume.assert_called_with(
            0.5
        )

    def test__get_music_dicts(self):
        """Test the get music dicts method."""
        music_dicts = self.sound_manager._get_music_dicts()

        self.assertEqual(
            music_dicts,
            {
                "level_music": self.sound_manager.level_music,
                "boss_rush_levels": self.sound_manager.boss_rush_levels,
                "endless_music": self.sound_manager.endless_music,
                "meteor_music": self.sound_manager.meteor_music,
            },
        )

    def test__set_multiple_music_volume(self):
        """Test the set_multiple_music_volume method."""
        pygame.mixer.music.set_volume = MagicMock()
        volume = 0.5

        self.sound_manager.level_music = {range(1, 8): "path_to_music_file"}
        self.sound_manager.endless_music = {range(1, 50): "path_to_music_file"}
        self.sound_manager.meteor_music = {range(1, 50): "path_to_music_file"}
        self.sound_manager.boss_rush_levels = {range(1, 5): "path_to_music_file"}

        self.sound_manager._set_multiple_music_volume(volume)

        pygame.mixer.music.set_volume.assert_called_with(volume)
        self.assertEqual(pygame.mixer.music.set_volume.call_count, 4)


if __name__ == "__main__":
    unittest.main()
