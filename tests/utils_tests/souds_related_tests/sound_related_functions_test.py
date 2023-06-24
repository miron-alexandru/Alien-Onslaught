"""
This module tests various functions from the game_utils modules
that are related to sounds.
"""

import unittest
from unittest.mock import patch
import os
import pygame

from src.utils.game_utils import (
    set_music_volume,
    play_music,
    load_sound_files,
    load_music_files,
    get_available_channels,
    set_sounds_volume,
    play_sound,
)

SOUND_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "sounds_for_testing")
)


class SoundUtilsTest(unittest.TestCase):
    """Test cases for sound related functions from game_utils."""

    def setUp(self):
        """Set up test environment."""
        pygame.mixer.init()
        self.sounds_dict = {"sound1": "sound1.wav", "sound2": "sound2.wav"}

        self.music_dict = {"music1": "music1.mp3", "music2": "music2.mp3"}

    @patch("src.utils.game_utils.SOUND_PATH", SOUND_PATH)
    def test_load_sound_files(self):
        """Test loading sound files."""
        sounds_files = load_sound_files(self.sounds_dict)

        self.assertIsNotNone(sounds_files)
        self.assertEqual(len(sounds_files), len(self.sounds_dict))

        # Assert that each sound file is an instance of pygame.mixer.Sound
        for sound_file in sounds_files.values():
            self.assertIsInstance(sound_file, pygame.mixer.Sound)

    @patch("src.utils.game_utils.SOUND_PATH", SOUND_PATH)
    def test_load_music_files(self):
        """Test loading music files."""
        music_files = load_music_files(self.music_dict)

        self.assertIsNotNone(music_files)
        self.assertEqual(len(music_files), len(self.music_dict))

        for music_file in music_files.values():
            self.assertTrue(music_file is None or isinstance(music_file, str))

    def test_play_music(self):
        """Test playing music."""
        music_files = {"music1": "sounds_for_testing/music1.mp3", "music2": None}
        music_name = "music1"

        with patch("pygame.mixer.music") as mock_music:
            # Call the function being tested
            play_music(music_files, music_name)

            # Assert that pygame.mixer.music.load and pygame.mixer.music.play were called
            mock_music.load.assert_called_once_with(music_files[music_name])
            mock_music.play.assert_called_once_with(-1)

    def test_set_sounds_volume(self):
        """Test setting sounds volume."""
        sounds = {
            "sound1": pygame.mixer.Sound(os.path.join(SOUND_PATH, "sound1.wav")),
            "sound2": pygame.mixer.Sound(os.path.join(SOUND_PATH, "sound2.wav")),
        }
        volume = 0.5

        with patch("pygame.mixer.Sound") as mock_sound:
            # Call the function being tested
            set_sounds_volume(sounds, volume)

            # Assert that the set_volume method was called for each sound
            for sound in mock_sound.return_value:
                sound.set_volume.assert_called_once_with(volume)

    def test_set_music_volume(self):
        """Test setting music volume."""
        music = {
            "music1": "sounds_for_testing/music1.mp3",
            "music2": "sounds_for_testing/music2.mp3",
        }
        volume = 0.7

        with patch("pygame.mixer.music.set_volume") as mock_music:
            set_music_volume(music, volume)

        # Assert that pygame.mixer.music.set_volume was called
        self.assertEqual(mock_music.call_count, len(music))

    def test_get_available_channels(self):
        """Test getting available sound channels."""
        available_channels = get_available_channels()

        # Assert that the returned value is a list
        self.assertIsInstance(available_channels, list)

        # Assert that each element in the list is an instance of pygame.mixer.Channel
        for channel in available_channels:
            self.assertIsInstance(channel, pygame.mixer.Channel)

    def test_play_sound(self):
        """Test playing a sound."""
        sounds_list = {
            "bullet": pygame.mixer.Sound(os.path.join(SOUND_PATH, "bullet.wav")),
            "alien_exploding": pygame.mixer.Sound(
                os.path.join(SOUND_PATH, "alien_exploding.wav")
            ),
            "sound1": pygame.mixer.Sound(os.path.join(SOUND_PATH, "sound1.wav")),
            "sound2": pygame.mixer.Sound(os.path.join(SOUND_PATH, "sound2.wav")),
        }
        sound_name = "sound1"

        with patch("pygame.mixer.Channel") as mock_channel, patch(
            "src.utils.game_utils.get_available_channels"
        ) as mock_get_available_channels:
            mock_get_available_channels.return_value = [
                pygame.mixer.Channel(2),
                pygame.mixer.Channel(3),
            ]

            # Call the function being tested
            play_sound(sounds_list, sound_name)

            # Assert the expected behavior based on the sound_name
            if sound_name == "bullet":
                mock_channel.assert_called_once_with(7)
            elif sound_name == "alien_exploding":
                mock_channel.assert_called_once_with(6)
            else:
                mock_get_available_channels.assert_called_once()
                self.assertEqual(mock_channel.call_count, 2)

            # Assert that the play method was called with the correct sound
            mock_channel.return_value.play.assert_called_once_with(
                sounds_list[sound_name]
            )


if __name__ == "__main__":
    unittest.main()
