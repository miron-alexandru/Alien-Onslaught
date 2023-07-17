"""
The save_load_manager module contains the SaveLoadSystem class that
implements the functionality of saving and loading the game.
"""

import pickle
import os

from src.entities.alien_entities.aliens import Alien


class SaveLoadSystem:
    """This class implements the Save/Load funcionality in the game."""

    def __init__(self, game, file_extension, save_folder):
        self.game = game
        self.file_extension = file_extension
        self.save_folder = save_folder
        self.data = {}

    def get_data(self, data_name, data):
        """Helper method that assigns data to the data dict."""
        self.data[data_name] = data

    def get_current_game_stats(self):
        """Retrieves and stores the current game statistics."""
        data_names = {
            "aliens": self.game.aliens,
            "level": self.game.stats.level,
            "high_score": self.game.stats.high_score,
            "thunderbird_score": self.game.stats.thunderbird_score,
            "phoenix_score": self.game.stats.phoenix_score,
            "thunderbird_hp": self.game.stats.thunderbird_hp,
            "phoenix_hp": self.game.stats.phoenix_hp,
            "thunderbird_ship_speed": self.game.settings.thunderbird_ship_speed,
            "thunderbird_bullet_speed": self.game.settings.thunderbird_bullet_speed,
            "thunderbird_bullets_allowed": self.game.settings.thunderbird_bullets_allowed,
            "thunderbird_bullet_count": self.game.settings.thunderbird_bullet_count,
            "thunderbird_missiles_num": self.game.thunderbird_ship.missiles_num,
            "phoenix_ship_speed": self.game.settings.phoenix_ship_speed,
            "phoenix_bullet_speed": self.game.settings.phoenix_bullet_speed,
            "phoenix_bullets_allowed": self.game.settings.phoenix_bullets_allowed,
            "phoenix_bullet_count": self.game.settings.phoenix_bullet_count,
            "phoenix_missiles_num": self.game.phoenix_ship.missiles_num,
            "alien_speed": self.game.settings.alien_speed,
            "alien_bullet_speed": self.game.settings.alien_bullet_speed,
            "alien_points": self.game.settings.alien_points,
            "fleet_rows": self.game.settings.fleet_rows,
            "last_bullet_rows": self.game.settings.last_bullet_rows,
            "aliens_num": self.game.settings.aliens_num,
            "alien_direction": self.game.settings.alien_direction,
            "alien_bullets_num": self.game.settings.alien_bullets_num,
            "max_alien_bullets": self.game.settings.max_alien_bullets,
            "boss_hp": self.game.settings.boss_hp,
            "boss_points": self.game.settings.boss_points,
            "asteroid_speed": self.game.settings.asteroid_speed,
            "asteroid_freq": self.game.settings.asteroid_freq,
            "thunder_ship_name": self.game.thunderbird_ship.ship_name,
            "phoenix_ship_name": self.game.phoenix_ship.ship_name,
        }

        for data_name, data_value in data_names.items():
            self.get_data(data_name, data_value)

    def save_data(self, name):
        """Saves the current game data to a file."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        sprite_group = self.data["aliens"]

        game_data = {
            "sprite_data": [
                {"rect": sprite.rect, "size": sprite.image.get_size()}
                for sprite in sprite_group
            ],
            **{
                key: self.data[key]
                for key in [
                    "level",
                    "high_score",
                    "thunderbird_score",
                    "phoenix_score",
                    "thunderbird_hp",
                    "phoenix_hp",
                    "thunderbird_ship_speed",
                    "thunderbird_bullet_speed",
                    "thunderbird_bullets_allowed",
                    "thunderbird_bullet_count",
                    "thunderbird_missiles_num",
                    "phoenix_ship_speed",
                    "phoenix_bullet_speed",
                    "phoenix_bullets_allowed",
                    "phoenix_bullet_count",
                    "phoenix_missiles_num",
                    "alien_speed",
                    "alien_bullet_speed",
                    "alien_points",
                    "fleet_rows",
                    "last_bullet_rows",
                    "aliens_num",
                    "alien_direction",
                    "alien_bullets_num",
                    "max_alien_bullets",
                    "boss_hp",
                    "boss_points",
                    "asteroid_speed",
                    "asteroid_freq",
                    "thunder_ship_name",
                    "phoenix_ship_name",
                ]
            },
        }

        with open(file_path, "wb") as file:
            pickle.dump(game_data, file)

    def load_data(self, name):
        """Loads game data from a file and updates the game state."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        with open(file_path, "rb") as file:
            loaded_data = pickle.load(file)

        sprite_data = loaded_data["sprite_data"]
        sprite_group = self.game.aliens

        for sprite_state in sprite_data:
            rect = sprite_state["rect"]

            sprite = Alien(self.game)
            sprite.rect = rect

            sprite_group.add(sprite)

        for key in [
            "level",
            "high_score",
            "thunderbird_score",
            "phoenix_score",
            "thunderbird_hp",
            "phoenix_hp",
            "thunderbird_ship_speed",
            "thunderbird_bullet_speed",
            "thunderbird_bullets_allowed",
            "thunderbird_bullet_count",
            "thunderbird_missiles_num",
            "phoenix_ship_speed",
            "phoenix_bullet_speed",
            "phoenix_bullets_allowed",
            "phoenix_bullet_count",
            "phoenix_missiles_num",
            "alien_speed",
            "alien_bullet_speed",
            "alien_points",
            "fleet_rows",
            "last_bullet_rows",
            "aliens_num",
            "alien_direction",
            "alien_bullets_num",
            "max_alien_bullets",
            "boss_hp",
            "boss_points",
            "asteroid_speed",
            "asteroid_freq",
            "thunder_ship_name",
            "phoenix_ship_name",
        ]:
            if key == "thunderbird_missiles_num":
                setattr(self.game.thunderbird_ship, "missiles_num", loaded_data[key])
            elif key == "phoenix_missiles_num":
                setattr(self.game.phoenix_ship, "missiles_num", loaded_data[key])
            elif key == "thunder_ship_name":
                setattr(self.game.thunderbird_ship, "ship_name", loaded_data[key])
            elif key == "phoenix_ship_name":
                setattr(self.game.phoenix_ship, "ship_name", loaded_data[key])
            elif hasattr(self.game.stats, key) or hasattr(self.game.settings, key):
                setattr(
                    self.game.stats
                    if hasattr(self.game.stats, key)
                    else self.game.settings,
                    key,
                    loaded_data[key],
                )
