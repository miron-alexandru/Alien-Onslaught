"""
This module tests the SaveLoadSystem class that is used to save
and load the game state.
"""
import os
import datetime
import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.managers.save_load_manager import SaveLoadSystem
from src.entities.alien_entities.aliens import Alien, BossAlien

from src.utils.constants import ATTRIBUTE_MAPPING

from src.game_logic.game_settings import Settings
from src.game_logic.game_stats import GameStats


class TestSaveLoadSystem(unittest.TestCase):
    """Test cases for the SaveLoadSystem class."""

    def setUp(self):
        # pygame.init()
        self.game = MagicMock()
        self.game.settings = Settings()
        self.game.stats = GameStats(
            self.game, self.game.phoenix_ship, self.game.thunderbird_ship
        )
        self.game.screen = self.game.bg_img = pygame.Surface((1280, 700))
        self.font = MagicMock()
        self.font.render.return_value = pygame.Surface((200, 50))
        with patch("src.managers.save_load_manager.create_save_dir"), patch(
            "src.managers.save_load_manager.pygame.font.SysFont", return_value=self.font
        ):
            self.save_load_manager = SaveLoadSystem(self.game, "save", "save_data")

        os.makedirs(self.save_load_manager.save_folder, exist_ok=True)

    def tearDown(self):
        # Remove the temporary folder and its contents after testing
        for root, _, files in os.walk(
            self.save_load_manager.save_folder, topdown=False
        ):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.save_load_manager.game, self.game)
        self.assertEqual(self.save_load_manager.screen, self.game.screen)
        self.assertEqual(self.save_load_manager.file_extension, "save")
        self.assertEqual(self.save_load_manager.save_folder, "save_data")
        self.assertFalse(self.save_load_manager.menu_running)

        self.assertEqual(self.save_load_manager.font, self.font)
        self.assertEqual(self.save_load_manager.center_x, 640)

        self.assertIsInstance(self.save_load_manager.cancel_text, pygame.Surface)
        self.assertIsInstance(self.save_load_manager.delete_text, pygame.Surface)
        self.assertIsInstance(self.save_load_manager.cancel_rect, pygame.Rect)
        self.assertIsInstance(self.save_load_manager.delete_rect, pygame.Rect)

    def test_get_data(self):
        """Test the get_data helper method."""
        # Set up data
        data_name = "test_data"
        data = ["player1_hp", "player2_hp"]

        self.save_load_manager.get_data(data_name, data)

        self.assertEqual(self.save_load_manager.data[data_name], data)

    def test_get_current_game_stats(self):
        """Test the get_current_game_stats method."""
        self.save_load_manager.get_current_game_stats()

        # Assertions
        self.assertEqual(self.save_load_manager.data["aliens"], self.game.aliens)
        self.assertEqual(self.save_load_manager.data["level"], self.game.stats.level)
        self.assertEqual(
            self.save_load_manager.data["high_score"], self.game.stats.high_score
        )

        # Thunderbird Ship
        self.assertEqual(
            self.save_load_manager.data["thunder_ship_name"],
            self.game.thunderbird_ship.ship_name,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_score"],
            self.game.stats.thunderbird_score,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_aliens_killed"],
            self.game.thunderbird_ship.aliens_killed,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_hp"],
            self.game.stats.thunderbird_hp,
        )

        self.assertEqual(
            self.save_load_manager.data["thunderbird_ship_speed"],
            self.game.settings.thunderbird_ship_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_bullet_speed"],
            self.game.settings.thunderbird_bullet_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_bullets_allowed"],
            self.game.settings.thunderbird_bullets_allowed,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_bullet_count"],
            self.game.settings.thunderbird_bullet_count,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_remaining_bullets"],
            self.game.thunderbird_ship.remaining_bullets,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_missiles_num"],
            self.game.thunderbird_ship.missiles_num,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_weapon_current"],
            self.game.weapons_manager.weapons["thunderbird"]["current"],
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_alive"],
            self.game.thunderbird_ship.state.alive,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_shielded"],
            self.game.thunderbird_ship.state.shielded,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_disarmed"],
            self.game.thunderbird_ship.state.disarmed,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_reversed"],
            self.game.thunderbird_ship.state.reverse,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_scaled_weapon"],
            self.game.thunderbird_ship.state.scaled_weapon,
        )
        self.assertEqual(
            self.save_load_manager.data["thunderbird_immune"],
            self.game.thunderbird_ship.state.immune,
        )

        # Phoenix Ship
        self.assertEqual(
            self.save_load_manager.data["phoenix_ship_name"],
            self.game.phoenix_ship.ship_name,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_score"], self.game.stats.phoenix_score
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_aliens_killed"],
            self.game.phoenix_ship.aliens_killed,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_hp"], self.game.stats.phoenix_hp
        )

        self.assertEqual(
            self.save_load_manager.data["phoenix_ship_speed"],
            self.game.settings.phoenix_ship_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_bullet_speed"],
            self.game.settings.phoenix_bullet_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_bullets_allowed"],
            self.game.settings.phoenix_bullets_allowed,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_bullet_count"],
            self.game.settings.phoenix_bullet_count,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_remaining_bullets"],
            self.game.phoenix_ship.remaining_bullets,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_missiles_num"],
            self.game.phoenix_ship.missiles_num,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_weapon_current"],
            self.game.weapons_manager.weapons["phoenix"]["current"],
        )

        self.assertEqual(
            self.save_load_manager.data["phoenix_alive"],
            self.game.phoenix_ship.state.alive,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_shielded"],
            self.game.phoenix_ship.state.shielded,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_disarmed"],
            self.game.phoenix_ship.state.disarmed,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_reversed"],
            self.game.phoenix_ship.state.reverse,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_scaled_weapon"],
            self.game.phoenix_ship.state.scaled_weapon,
        )
        self.assertEqual(
            self.save_load_manager.data["phoenix_immune"],
            self.game.phoenix_ship.state.immune,
        )

        # Game Modes
        self.assertEqual(
            self.save_load_manager.data["game_mode"],
            self.game.settings.game_modes.game_mode,
        )
        self.assertEqual(
            self.save_load_manager.data["endless_onslaught"],
            self.game.settings.game_modes.endless_onslaught,
        )
        self.assertEqual(
            self.save_load_manager.data["slow_burn"],
            self.game.settings.game_modes.slow_burn,
        )
        self.assertEqual(
            self.save_load_manager.data["meteor_madness"],
            self.game.settings.game_modes.meteor_madness,
        )
        self.assertEqual(
            self.save_load_manager.data["boss_rush"],
            self.game.settings.game_modes.boss_rush,
        )
        self.assertEqual(
            self.save_load_manager.data["last_bullet"],
            self.game.settings.game_modes.last_bullet,
        )
        self.assertEqual(
            self.save_load_manager.data["cosmic_conflict"],
            self.game.settings.game_modes.cosmic_conflict,
        )
        self.assertEqual(
            self.save_load_manager.data["one_life_reign"],
            self.game.settings.game_modes.one_life_reign,
        )

        # Game Settings
        self.assertEqual(
            self.save_load_manager.data["alien_speed"], self.game.settings.alien_speed
        )
        self.assertEqual(
            self.save_load_manager.data["alien_bullet_speed"],
            self.game.settings.alien_bullet_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["alien_points"], self.game.settings.alien_points
        )
        self.assertEqual(
            self.save_load_manager.data["fleet_rows"], self.game.settings.fleet_rows
        )
        self.assertEqual(
            self.save_load_manager.data["last_bullet_rows"],
            self.game.settings.last_bullet_rows,
        )
        self.assertEqual(
            self.save_load_manager.data["aliens_num"], self.game.settings.aliens_num
        )
        self.assertEqual(
            self.save_load_manager.data["alien_bullets_num"],
            self.game.settings.alien_bullets_num,
        )
        self.assertEqual(
            self.save_load_manager.data["max_alien_bullets"],
            self.game.settings.max_alien_bullets,
        )
        self.assertEqual(
            self.save_load_manager.data["boss_hp"], self.game.settings.boss_hp
        )
        self.assertEqual(
            self.save_load_manager.data["boss_points"], self.game.settings.boss_points
        )
        self.assertEqual(
            self.save_load_manager.data["asteroid_speed"],
            self.game.settings.asteroid_speed,
        )
        self.assertEqual(
            self.save_load_manager.data["asteroid_freq"],
            self.game.settings.asteroid_freq,
        )
        self.assertEqual(
            self.save_load_manager.data["speedup_scale"],
            self.game.settings.speedup_scale,
        )

        self.assertEqual(len(self.save_load_manager.data), 58)

    def test_update_alien_states(self):
        """Test the update_alien_states method."""
        # Set up initial alien states
        frozen_alien = MagicMock()
        frozen_alien.frozen_state = True
        frozen_alien.immune_state = False

        normal_alien = MagicMock()
        normal_alien.immune_state = False
        normal_alien.frozen_state = False

        self.game.aliens = [frozen_alien, normal_alien]

        self.save_load_manager.update_alien_states()

        # Assertions
        self.game.powers_manager.freeze_enemies.assert_called_once()
        self.game.powers_manager.alien_upgrade.assert_not_called()

    def test_update_player_ship_states(self):
        """Test the update_player_ship_states method."""
        # Set up initial ship states
        self.game.thunderbird_ship.state.disarmed = True
        self.game.thunderbird_ship.state.shielded = True
        self.game.thunderbird_ship.state.reverse = False
        self.game.thunderbird_ship.state.scaled_weapon = False
        self.game.thunderbird_ship.state.immune = False

        self.game.phoenix_ship.state.disarmed = False
        self.game.phoenix_ship.state.shielded = False
        self.game.phoenix_ship.state.reverse = False
        self.game.phoenix_ship.state.scaled_weapon = True
        self.game.phoenix_ship.state.immune = True

        self.save_load_manager.update_player_ship_states()

        # Assertions
        self.game.powers_manager.disarm_ship.assert_called_once_with("thunderbird")
        self.game.powers_manager.draw_ship_shield.assert_called_once_with("thunderbird")
        self.game.powers_manager.decrease_bullet_size.assert_called_once_with("phoenix")
        self.game.powers_manager.invincibility.assert_called_once_with("phoenix")

        self.game.powers_manager.reverse_keys.assert_not_called()

    def test_update_player_weapon(self):
        """Test the update_player_weapon method."""
        # Set up weapons
        self.game.weapons_manager.weapons = {
            "thunderbird": {"current": "blaster"},
            "phoenix": {"current": "laser"},
        }

        self.save_load_manager.update_player_weapon()
        expected_calls = [
            call("thunderbird", "blaster", loaded=True),
            call("phoenix", "laser", loaded=True),
        ]
        self.assertEqual(
            self.game.weapons_manager.set_weapon.call_args_list, expected_calls
        )

    @patch("src.managers.save_load_manager.pygame.image.tostring")
    def test_prepare_sprite_data_for_serialization(self, mock_tostring):
        """Test the prepare_sprite_data_for_serialization method."""
        # Set up the mock data for the pygame.image.tostring call
        mock_tostring.side_effect = lambda img, format: img
        alien = MagicMock(spec=Alien)
        alien.rect = MagicMock(x=100, y=200)
        alien.image = MagicMock(
            get_size=MagicMock(return_value=(30, 40)),
            tostring=MagicMock(return_value=b"sample_image_data"),
        )
        alien.is_baby = False
        alien.hit_count = 3
        alien.last_bullet_time = 123
        alien.immune_state = False
        alien.frozen_state = True

        boss_alien = MagicMock(spec=BossAlien)
        boss_alien.rect = MagicMock(x=300, y=400)
        boss_alien.image = MagicMock(
            get_size=MagicMock(return_value=(50, 60)),
            tostring=MagicMock(return_value=b"another_image_data"),
        )
        boss_alien.is_baby = True
        boss_alien.hit_count = 1
        boss_alien.last_bullet_time = 2923
        boss_alien.immune_state = False
        boss_alien.frozen_state = False

        sprite_data = {
            "aliens": [
                alien,
                boss_alien,
            ]
        }

        self.save_load_manager.data = sprite_data

        result = self.save_load_manager.prepare_sprite_data_for_serialization()

        # Assert the output of the method with the expected serialized data

        expected_data = {
            "alien_sprites": [
                {
                    "rect": alien.rect,
                    "size": (30, 40),
                    "image": alien.image,
                    "is_baby": False,
                    "type": "alien",
                    "location": 100,
                    "hit_count": 3,
                    "last_bullet_time": 123,
                    "immune_state": False,
                    "frozen_state": True,
                },
                {
                    "rect": boss_alien.rect,
                    "size": (50, 60),
                    "image": boss_alien.image,
                    "is_baby": False,
                    "type": "boss",
                    "location": 300,
                    "hit_count": 1,
                    "last_bullet_time": 2923,
                    "immune_state": None,
                    "frozen_state": False,
                },
            ],
        }

        self.assertEqual(result, expected_data)

    @patch("src.managers.save_load_manager.pickle.dump")
    @patch("src.managers.save_load_manager.os.path.join")
    def test_save_data(self, mock_join, mock_pickle_dump):
        """Test the save_data method."""
        self.save_load_manager.prepare_sprite_data_for_serialization = MagicMock()
        self.save_load_manager.get_current_game_stats()

        mock_open_func = MagicMock()

        with patch("builtins.open", mock_open_func):
            self.save_load_manager.save_data("save1", MagicMock())

        mock_open_func.assert_called_once()
        mock_join.assert_called_once_with(
            self.save_load_manager.save_folder, "save1.save"
        )
        mock_pickle_dump.assert_called_once()

    @patch("src.managers.save_load_manager.pickle.load")
    @patch("src.managers.save_load_manager.os.path.join")
    def test_load_data(self, mock_join, mock_pickle_load):
        """Test the load_data method."""
        self.save_load_manager.update_game_state_from_data = MagicMock()
        self.save_load_manager.restore_sprites_from_data = MagicMock()

        mock_open_func = MagicMock()
        with patch("builtins.open", mock_open_func):
            self.save_load_manager.load_data("save1")

        mock_open_func.assert_called_once()
        mock_join.assert_called_once_with(
            self.save_load_manager.save_folder, "save1.save"
        )
        mock_pickle_load.assert_called_once()

        self.save_load_manager.update_game_state_from_data.assert_called_once()
        self.save_load_manager.restore_sprites_from_data.assert_called_once()

    @patch("src.managers.save_load_manager.pygame.image.fromstring")
    def test_restore_sprites_from_data(self, mock_fromstring):
        """Test the restore_sprites_from_data method."""
        # Set up loaded sprites data
        loaded_data = {
            "sprite_data": {
                "alien_sprites": [
                    {
                        "type": "alien",
                        "size": (32, 32),
                        "rect": (100, 100, 32, 32),
                        "image": b"MockImageString",
                        "location": (200, 200),
                        "frozen_state": False,
                        "is_baby": False,
                        "immune_state": False,
                        "last_bullet_time": 128,
                    },
                ]
            }
        }

        self.save_load_manager.restore_sprites_from_data(loaded_data)

        # Assertions
        self.assertEqual(self.game.aliens.empty.call_count, 1)
        self.assertEqual(
            mock_fromstring.call_count, len(loaded_data["sprite_data"]["alien_sprites"])
        )

        restored_sprites = self.game.aliens.add.call_args_list
        self.assertEqual(
            len(restored_sprites), len(loaded_data["sprite_data"]["alien_sprites"])
        )

        for i, call_args in enumerate(restored_sprites):
            sprite = call_args[0][0]
            sprite_state = loaded_data["sprite_data"]["alien_sprites"][i]

            self.assertEqual(sprite.size, sprite_state["size"])
            self.assertEqual(sprite.rect, sprite_state["rect"])
            self.assertEqual(sprite.x_pos, sprite_state["location"])
            self.assertEqual(sprite.frozen_state, sprite_state["frozen_state"])
            self.assertEqual(sprite.immune_state, sprite_state["immune_state"])
            self.assertEqual(sprite.last_bullet_time, sprite_state["last_bullet_time"])

    def test_create_regular_alien_sprite(self):
        """Test the create_alien_sprite method with a normal Alien."""
        sprite_type = "alien"
        sprite_state = {"is_baby": False}
        sprite = self.save_load_manager.create_alien_sprite(
            sprite_type, sprite_state, self.game
        )

        self.assertIsInstance(sprite, Alien)

    def test_create_boss_alien_sprite(self):
        """Test the create_alien_sprite method with a BossAlien."""
        sprite_type = "boss"
        sprite_state = {}

        sprite = self.save_load_manager.create_alien_sprite(
            sprite_type, sprite_state, self.game
        )

        self.assertIsInstance(sprite, BossAlien)

    def test_create_baby_alien_sprite(self):
        """Test the create_alien_sprite method with a baby Alien."""
        sprite_type = "alien"
        sprite_state = {"is_baby": True, "location": 100}

        sprite = self.save_load_manager.create_alien_sprite(
            sprite_type, sprite_state, self.game
        )

        # Assertions
        self.assertIsInstance(sprite, Alien)
        self.assertTrue(sprite.is_baby)
        self.assertEqual(sprite.x_pos, 100)

    @patch("src.managers.save_load_manager.set_attribute")
    def test_update_game_state_from_data(self, mock_set_attribute):
        """Test the update_game_state_from_data method."""

        loaded_data = {
            "high_score": 1000,
            "level": 5,
            "thunder_ship_name": "Thunderbird",
            "thunderbird_score": 5000,
            "thunderbird_aliens_killed": 50,
            "thunderbird_hp": 80,
            "thunderbird_ship_speed": 10,
            "thunderbird_bullet_speed": 15,
            "thunderbird_bullets_allowed": 5,
            "thunderbird_bullet_count": 20,
            "thunderbird_remaining_bullets": 15,
            "thunderbird_missiles_num": 3,
            "thunderbird_weapon_current": "Laser",
            "thunderbird_alive": False,
            "thunderbird_shielded": True,
            "thunderbird_disarmed": False,
            "thunderbird_reversed": False,
            "thunderbird_scaled_weapon": True,
            "thunderbird_immune": False,
            "phoenix_ship_name": "Phoenix",
            "phoenix_score": 3000,
            "phoenix_aliens_killed": 30,
            "phoenix_hp": 100,
            "phoenix_ship_speed": 12,
            "phoenix_bullet_speed": 18,
            "phoenix_bullets_allowed": 7,
            "phoenix_bullet_count": 25,
            "phoenix_remaining_bullets": 22,
            "phoenix_missiles_num": 2,
            "phoenix_weapon_current": "Plasma",
            "phoenix_alive": True,
            "phoenix_shielded": False,
            "phoenix_disarmed": True,
            "phoenix_reversed": True,
            "phoenix_scaled_weapon": False,
            "phoenix_immune": True,
            "game_mode": "boss_rush",
            "endless_onslaught": False,
            "slow_burn": True,
            "meteor_madness": False,
            "boss_rush": True,
            "last_bullet": False,
            "cosmic_conflict": False,
            "one_life_reign": False,
            "alien_speed": 5,
            "alien_bullet_speed": 8,
            "alien_points": 100,
            "fleet_rows": 5,
            "last_bullet_rows": 3,
            "aliens_num": 30,
            "alien_bullets_num": 10,
            "max_alien_bullets": 20,
            "boss_hp": 200,
            "boss_points": 500,
            "asteroid_speed": 6,
            "asteroid_freq": 4,
            "speedup_scale": 1.2,
        }

        self.save_load_manager.update_game_state_from_data(loaded_data)

        # Assertions
        self.assertEqual(mock_set_attribute.call_count, len(ATTRIBUTE_MAPPING))

        for key, attributes in ATTRIBUTE_MAPPING.items():
            self.assertTrue(key in loaded_data)
            self.assertTrue(loaded_data[key] is not None)
            mock_set_attribute.assert_any_call(self.game, attributes, loaded_data[key])

        self.assertEqual(self.game.stats.high_score, 1000)
        self.assertEqual(self.game.stats.thunderbird_score, 5000)
        self.assertEqual(self.game.stats.thunderbird_hp, 80)

        self.assertEqual(self.game.settings.thunderbird_ship_speed, 10)
        self.assertEqual(self.game.settings.thunderbird_bullet_speed, 15)
        self.assertEqual(self.game.settings.alien_speed, 5)
        self.assertEqual(self.game.settings.alien_bullet_speed, 8)

    @patch("src.managers.save_load_manager.pygame")
    def test_handle_save_load_menu(self, mock_pygame):
        """Test the handle_save_load_menu method."""
        self.save_load_manager.display_screen_title = MagicMock()
        self.save_load_manager.screen = MagicMock()

        with patch("src.managers.save_load_manager.pygame.display.flip"):
            self.save_load_manager._get_save_files = MagicMock(
                return_value=["save1.save", "save2.save", "save3.save"]
            )
            self.save_load_manager._draw_save_slots = MagicMock()
            mock_pygame.display.flip.side_effect = lambda: setattr(
                self.save_load_manager, "menu_running", False
            )

            # Call the method under test
            self.save_load_manager.handle_save_load_menu(save=True)

            # Make assertions based on expected calls and interactions
            self.save_load_manager._get_save_files.assert_called_once()
            # self.game.screen.fill.assert_called_once_with((0, 0, 0))
            self.save_load_manager._draw_save_slots.assert_called_once()

            expected_blit_calls = [
                call(self.game.bg_img, [0, 0]),
                call(
                    self.font.render.return_value,
                    self.font.render.return_value.get_rect(
                        center=(self.game.screen.get_width() // 2 + 100, 465)
                    ),
                ),
                call(
                    self.font.render.return_value,
                    self.font.render.return_value.get_rect(
                        center=(self.game.screen.get_width() // 2 - 100, 465)
                    ),
                ),
            ]
            self.assertEqual(
                self.save_load_manager.screen.blit.call_args_list, expected_blit_calls
            )
            self.save_load_manager.display_screen_title.assert_called_once()
            self.game.screen_manager.draw_cursor.assert_called_once()
            mock_pygame.display.flip.assert_called_once()

    def test_get_save_files(self):
        """Test the get_save_files method."""
        # Create test files with different extensions
        test_files = [
            "savegame1.save",
            "savegame2.save",
            "savegame3.save",
            "random_file.txt",
        ]
        for filename in test_files:
            open(
                os.path.join(self.save_load_manager.save_folder, filename),
                "w",
                encoding="utf-8",
            ).close()

        result = self.save_load_manager._get_save_files()

        # Define the expected result
        expected_result = ["savegame1.save", "savegame2.save", "savegame3.save"]

        # Assertion
        self.assertListEqual(result, expected_result)

    def test_get_save_status_text_no_savefiles(self):
        """Test the get_save_status_text with no savefiles."""
        save_files = []

        # Call the method
        result = self.save_load_manager._get_save_status_text(
            slot_number=1, save_files=save_files
        )

        expected_result = "Empty"

        # Assertion
        self.assertEqual(result, expected_result)

    def test_get_save_status_text_existing_savefile(self):
        """Test the get_save_status_text with a savefile."""
        # Prepare data for testing
        test_save_file = "save1.save"
        open(
            os.path.join(self.save_load_manager.save_folder, test_save_file),
            "w",
            encoding="utf-8",
        ).close()

        save_files = [test_save_file]

        # Call the method
        result = self.save_load_manager._get_save_status_text(
            slot_number=1, save_files=save_files
        )

        # Get the current date and time in the required format
        current_time_str = datetime.datetime.now().strftime("%d %b %Y  %I:%M %p")

        expected_result = f"Saved On: {current_time_str}"

        # Assertion
        self.assertEqual(result, expected_result)

    @patch("src.managers.save_load_manager.pygame.draw.rect")
    def test_draw_save_slots(self, mock_draw_rect):
        """Test the draw_save_slots method."""
        # Prepare data for testing
        test_save_files = ["save1.save", "save2.save", "save3.save"]
        for filename in test_save_files:
            open(
                os.path.join(self.save_load_manager.save_folder, filename),
                "w",
                encoding="utf-8",
            ).close()

        text_color = (255, 255, 255)
        center_x = 400
        slot_selected = 0
        slot_rects = []

        # Call the method
        self.save_load_manager._draw_save_slots(
            font=self.font,
            text_color=text_color,
            center_x=center_x,
            save_files=test_save_files,
            slot_selected=slot_selected,
            slot_rects=slot_rects,
        )
        current_time = datetime.datetime.now().strftime("%d %b %Y  %I:%M %p")
        expected_text_0 = f"Save File 1: Saved On: {current_time}"
        actual_text_0 = self.font.render.call_args_list[2][0][0]

        expected_text_1 = f"Save File 2: Saved On: {current_time}"
        actual_text_1 = self.font.render.call_args_list[3][0][0]
        # Assertions:
        mock_draw_rect.assert_called_once()
        self.assertEqual(actual_text_0, expected_text_0)
        self.assertEqual(actual_text_1, expected_text_1)
        self.assertEqual(len(slot_rects), 3)

    def test_handle_save_slot_action(self):
        """Test the handle_save_slot_action method."""
        self.save_load_manager._handle_save_action = MagicMock()
        self.save_load_manager._handle_load_action = MagicMock()
        slot_selected = 1
        # Save case
        self.save_load_manager._handle_save_slot_action(
            self.font, slot_selected, save=True
        )

        self.save_load_manager._handle_save_action.assert_called_once_with(
            self.font, slot_selected
        )
        self.save_load_manager._handle_load_action.assert_not_called()

        # Load case
        self.save_load_manager._handle_save_action.reset_mock()
        self.save_load_manager._handle_save_slot_action(
            self.font, slot_selected, save=False
        )

        self.save_load_manager._handle_load_action.assert_called_once_with(
            self.font, slot_selected
        )
        self.save_load_manager._handle_save_action.assert_not_called()

    def test_handle_save_action_overwrite(self):
        """Test the handle_save_action methond when overwriting a savefile."""
        # Prepare testing data
        slot_selected = 0

        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save"]
        )
        self.save_load_manager._show_confirmation_popup = MagicMock()
        self.save_load_manager._save_game = MagicMock()

        self.save_load_manager._handle_save_action(self.font, slot_selected)

        # Assertions
        self.save_load_manager._get_save_files.assert_called_once()
        self.save_load_manager._show_confirmation_popup.assert_called_once_with(
            delete_save_files=False
        )
        self.save_load_manager._save_game.assert_called_once()

    @patch("src.managers.save_load_manager.play_sound")
    def test_handle_save_action_overwrite_not_accepting(self, mock_play_sound):
        """Test the handle_save_action methond when not confirming the
        overwrite."""
        # Prepare testing data
        slot_selected = 0

        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save"]
        )
        self.save_load_manager._show_confirmation_popup = MagicMock(return_value=False)
        self.save_load_manager._save_game = MagicMock()

        self.save_load_manager._handle_save_action(self.font, slot_selected)

        # Assertions
        self.save_load_manager._get_save_files.assert_called_once()
        self.save_load_manager._show_confirmation_popup.assert_called_once_with(
            delete_save_files=False
        )
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "click"
        )

        self.save_load_manager._save_game.assert_not_called()

    def test_handle_save_action_new_save(self):
        """Test the handle_save_action methond with a new savefile."""
        # Prepare testing data
        slot_selected = 2

        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save"]
        )
        self.save_load_manager._show_confirmation_popup = MagicMock()
        self.save_load_manager._save_game = MagicMock()

        self.save_load_manager._handle_save_action(self.font, slot_selected)

        # Assertions
        self.save_load_manager._get_save_files.assert_called_once()
        self.save_load_manager._show_confirmation_popup.assert_not_called()
        self.save_load_manager._save_game.assert_called_once()

    @patch("src.managers.save_load_manager.play_sound")
    @patch("src.managers.save_load_manager.display_simple_message")
    def test_handle_load_action_existing_savefile(
        self, mock_display_message, mock_play_sound
    ):
        """Test the handle_load_action with an existing savefile."""
        # Prepare data for testing
        slot_selected = 0

        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save"]
        )
        self.save_load_manager.load_data = MagicMock()

        self.save_load_manager._handle_load_action(self.font, slot_selected)

        self.save_load_manager._get_save_files.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "load_game"
        )
        self.save_load_manager.load_data.assert_called_once_with(
            f"save{slot_selected + 1}"
        )
        self.assertTrue(self.game.game_loaded)
        mock_display_message.assert_called_once_with(
            self.game.screen, "Game Loaded!", self.font, "lightblue", 1000
        )

    @patch("src.managers.save_load_manager.play_sound")
    @patch("src.managers.save_load_manager.display_simple_message")
    def test_handle_load_action_non_existing_savefile(
        self, mock_display_message, mock_play_sound
    ):
        """Test the handle_load_action with a non existing savefile."""
        # Prepare data for testing
        slot_selected = 2

        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save"]
        )
        self.save_load_manager.load_data = MagicMock()

        self.save_load_manager._handle_load_action(self.font, slot_selected)

        self.save_load_manager._get_save_files.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "empty_save"
        )
        mock_display_message.assert_called_once_with(
            self.game.screen, "Empty save slot", self.font, "red", 500
        )

        self.save_load_manager.load_data.assert_not_called()

    @patch("src.managers.save_load_manager.play_sound")
    @patch("src.managers.save_load_manager.display_simple_message")
    def test_save_game(self, mock_display_message, mock_play_sound):
        """Test the _save_game method."""
        slot_selected = 1
        self.save_load_manager.save_data = MagicMock()
        save_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_load_manager._save_game(self.font, slot_selected)

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "click"
        )
        self.save_load_manager.save_data.assert_called_once_with(
            f"save{slot_selected + 1}", save_date=save_date
        )
        mock_display_message.assert_called_once_with(
            self.game.screen, "Game Saved!", self.font, "lightblue", 1000
        )

    def test_delete_all_save_files(self):
        """Test the delete_all_save_files method."""
        # Set up test data
        self.save_load_manager._get_save_files = MagicMock(
            return_value=["save1.save", "save2.save", "save3.save"]
        )

        # Create some sample save files
        sample_save_files = ["save1.save", "save2.save", "save3.save"]
        for save_file in sample_save_files:
            with open(
                os.path.join(self.save_load_manager.save_folder, save_file),
                "w",
                encoding="utf-8",
            ) as file:
                file.write("Sample data")

        # Call the method
        self.save_load_manager._delete_all_save_files()

        # Check if the save files have been deleted
        self.assertFalse(os.listdir(self.save_load_manager.save_folder))

    @patch("src.managers.save_load_manager.tk.Tk")
    @patch("src.managers.save_load_manager.messagebox.askyesno")
    def test_show_confirmation_popup_delete_save_files(self, mock_askyesno, mock_tk):
        """Test the show_confirmation_popup with delete_save_files."""
        mock_askyesno.return_value = True

        # Call the _show_confirmation_popup method with delete_save_files=True
        response = self.save_load_manager._show_confirmation_popup(
            delete_save_files=True
        )

        # Assertions
        self.assertTrue(response)
        mock_tk.assert_called_once()
        mock_askyesno.assert_called_once_with("Confirmation", "Delete all save files?")

    @patch("src.managers.save_load_manager.tk.Tk")
    @patch("src.managers.save_load_manager.messagebox.askyesno")
    def test_show_confirmation_popup_overwrite_save_file(self, mock_askyesno, mock_tk):
        """Test the show_confirmation_popup with overwrite save_file."""
        mock_askyesno.return_value = False

        # Call the _show_confirmation_popup method with delete_save_files=False
        response = self.save_load_manager._show_confirmation_popup(
            delete_save_files=False
        )

        # Assertions
        self.assertFalse(response)
        mock_tk.assert_called_once()
        mock_askyesno.assert_called_once_with(
            "Confirmation", "Overwrite this save file?"
        )

    def test_update_rect_positions(self):
        """Test the update_rect_positions method."""
        self.save_load_manager.update_rect_positions()

        # Assertions
        self.assertEqual(self.save_load_manager.center_x, 640)
        self.assertEqual(self.save_load_manager.cancel_rect.center, (740, 465))
        self.assertEqual(self.save_load_manager.delete_rect.center, (540, 465))

    def test_set_screen_title_position(self):
        """Test the set_screen_title_position method."""
        self.save_load_manager.set_screen_title_position()

        # Assertions
        self.assertEqual(self.game.settings.save_game_rect.center, (640, 170))
        self.assertEqual(self.game.settings.load_game_rect.center, (640, 170))

    def test_display_screen_title(self):
        """Test the display_screen_title method."""
        self.save_load_manager.screen = MagicMock()
        save = True
        self.save_load_manager.display_screen_title(save)

        self.save_load_manager.screen.blit.assert_called_once_with(
            self.game.settings.save_game_img, self.game.settings.save_game_rect
        )


if __name__ == "__main__":
    unittest.main()
