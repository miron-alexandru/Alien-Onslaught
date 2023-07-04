import unittest
from unittest.mock import MagicMock, patch, call
import os

# Import the functions from your module
# You might need to adjust the import statement based on your module's name
from src.utils.game_utils import (
    load_sound_files,
    load_music_files,
    play_music,
    set_sounds_volume,
    set_music_volume,
    get_available_channels,
    play_sound,
)

class TestSoundFunctions(unittest.TestCase):
    def setUp(self):
        # Mock the pygame.mixer and other relevant functions
        self.mock_pygame_mixer = MagicMock()
        self.mock_pygame_mixer.Sound = MagicMock()
        self.mock_pygame_mixer.music = MagicMock()
        self.mock_pygame_mixer.Channel = MagicMock()

        # Patch the necessary functions in the module
        self.patcher = patch("src.utils.game_utils.pygame", self.mock_pygame_mixer)
        self.patcher.start()

        # Create mock sound and music dictionaries
        self.mock_sounds_dict = {
            "sound1": "path/to/sound1.wav",
            "sound2": "path/to/sound2.wav",
        }
        self.mock_music_dict = {
            "music1": "path/to/music1.mp3",
            "music2": "path/to/music2.mp3",
        }

    def tearDown(self):
        # Stop the patcher after the test
        self.patcher.stop()

    def test_load_sound_files(self):
        SOUND_PATH = "path/to/sounds/folder/"  # Adjust the SOUND_PATH to match your actual path

        # Mock the sounds_dict with sample sound names and paths
        sounds_dict = {
            "sound1": "sound1.wav",
            "sound2": "sound2.wav",
        }

        # Call the function with the mock sounds_dict
        load_sound_files(sounds_dict)

        # Check that pygame.mixer.Sound was called with the correct paths
        expected_calls = [
            call(os.path.join(SOUND_PATH, "sound1.wav")),
            call(os.path.join(SOUND_PATH, "sound2.wav")),
        ]
        print(self.mock_pygame_mixer.Sound.call_args_list)
        self.mock_pygame_mixer.Sound.assert_has_calls(expected_calls)

    def tesi_load_music_files(self):
        load_music_files(self.mock_music_dict)

        # Check that pygame.mixer.music.load was called with the correct paths
        self.mock_pygame_mixer.music.load.assert_any_call(
            "path/to/music1.mp3"
        )
        self.mock_pygame_mixer.music.load.assert_any_call(
            "path/to/music2.mp3"
        )

    def tesi_play_music(self):
        # Assuming the music_name is "music1" and exists in the music_files dictionary
        music_files = {"music1": "path/to/music1.mp3"}
        music_name = "music1"
        play_music(music_files, music_name)

        # Check that pygame.mixer.music.load and pygame.mixer.music.play were called with the correct music path
        self.mock_pygame_mixer.music.load.assert_called_once_with(
            "path/to/music1.mp3"
        )
        self.mock_pygame_mixer.music.play.assert_called_once_with(-1)

    def tesi_set_sounds_volume(self):
        sounds = load_sound_files(self.mock_sounds_dict)
        set_sounds_volume(sounds, 0.5)

        # Check that set_volume was called on all sound objects
        for sound in sounds.values():
            sound.set_volume.assert_called_once_with(0.5)

    def tesi_set_music_volume(self):
        music_files = load_music_files(self.mock_music_dict)
        set_music_volume(music_files, 0.7)

        # Check that pygame.mixer.music.set_volume was called with the correct volume
        self.mock_pygame_mixer.music.set_volume.assert_called_once_with(0.7)

    def tesi_get_available_channels(self):
        # Assuming 3 channels are available
        self.mock_pygame_mixer.get_num_channels.return_value = 3

        available_channels = get_available_channels()

        # Check that pygame.mixer.Channel was called with the correct channel numbers
        self.mock_pygame_mixer.Channel.assert_any_call(0)
        self.mock_pygame_mixer.Channel.assert_any_call(1)
        self.mock_pygame_mixer.Channel.assert_any_call(2)

        # Check that the returned available_channels list is correct
        self.assertEqual(available_channels, [
            self.mock_pygame_mixer.Channel.return_value,
            self.mock_pygame_mixer.Channel.return_value,
            self.mock_pygame_mixer.Channel.return_value,
        ])

    def tesi_play_sound(self):
        # Assuming sound_name is "bullet"
        sounds_list = {"bullet": MagicMock()}
        sound_name = "bullet"

        play_sound(sounds_list, sound_name)

        # Check that pygame.mixer.Channel.play was called with the correct sound object
        self.mock_pygame_mixer.Channel.return_value.play.assert_called_once_with(
            sounds_list["bullet"]
        )

if __name__ == "__main__":
    unittest.main()
