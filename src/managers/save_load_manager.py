"""
The save_load_manager module contains the SaveLoadSystem class that
implements the functionality of saving and loading the game.
"""

import pickle
import os

import pygame

from src.entities.alien_entities.aliens import Alien, BossAlien
from src.utils.constants import DATA_KEYS, ATTRIBUTE_MAPPING
from src.utils.game_utils import set_attribute


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
        game = self.game
        stats = self.game.stats
        thunderbird_ship = self.game.thunderbird_ship
        phoenix_ship = self.game.phoenix_ship
        settings = self.game.settings
        game_modes = self.game.settings.game_modes

        data_names = {
            # Other Game Stats
            "aliens": game.aliens,
            "level": stats.level,
            "high_score": stats.high_score,

            # Thunderbird Ship
            "thunder_ship_name": thunderbird_ship.ship_name,
            "thunderbird_score": stats.thunderbird_score,
            "thunderbird_aliens_killed": thunderbird_ship.aliens_killed,
            "thunderbird_hp": stats.thunderbird_hp,

            "thunderbird_ship_speed": settings.thunderbird_ship_speed,
            "thunderbird_bullet_speed": settings.thunderbird_bullet_speed,
            "thunderbird_bullets_allowed": settings.thunderbird_bullets_allowed,
            "thunderbird_bullet_count": settings.thunderbird_bullet_count,
            "thunderbird_remaining_bullets": thunderbird_ship.remaining_bullets,
            "thunderbird_missiles_num": thunderbird_ship.missiles_num,
            "thunderbird_weapon_current": game.weapons_manager.weapons["thunderbird"]["current"],

            "thunderbird_shielded": thunderbird_ship.state.shielded,
            "thunderbird_disarmed": thunderbird_ship.state.disarmed,
            "thunderbird_reversed": thunderbird_ship.state.reverse,
            "thunderbird_scaled_weapon": thunderbird_ship.state.scaled_weapon,
            "thunderbird_immune": thunderbird_ship.state.immune,

            # Phoenix Ship
            "phoenix_ship_name": phoenix_ship.ship_name,
            "phoenix_score": stats.phoenix_score,
            "phoenix_aliens_killed": phoenix_ship.aliens_killed,
            "phoenix_hp": stats.phoenix_hp,

            "phoenix_ship_speed": settings.phoenix_ship_speed,
            "phoenix_bullet_speed": settings.phoenix_bullet_speed,
            "phoenix_bullets_allowed": settings.phoenix_bullets_allowed,
            "phoenix_bullet_count": settings.phoenix_bullet_count,
            "phoenix_remaining_bullets": phoenix_ship.remaining_bullets,
            "phoenix_missiles_num": phoenix_ship.missiles_num,
            "phoenix_weapon_current": game.weapons_manager.weapons["phoenix"]["current"],

            "phoenix_shielded": phoenix_ship.state.shielded,
            "phoenix_disarmed": phoenix_ship.state.disarmed,
            "phoenix_reversed": phoenix_ship.state.reverse,
            "phoenix_scaled_weapon": phoenix_ship.state.scaled_weapon,
            "phoenix_immune": phoenix_ship.state.immune,

            # Game Modes
            "game_mode": game_modes.game_mode,
            "endless_onslaught": game_modes.endless_onslaught,
            "slow_burn": game_modes.slow_burn,
            "meteor_madness": game_modes.meteor_madness,
            "boss_rush": game_modes.boss_rush,
            "last_bullet": game_modes.last_bullet,
            "cosmic_conflict": game_modes.cosmic_conflict,
            "one_life_reign": game_modes.one_life_reign,

            # Game Settings
            "alien_speed": settings.alien_speed,
            "alien_bullet_speed": settings.alien_bullet_speed,
            "alien_points": settings.alien_points,
            "fleet_rows": settings.fleet_rows,
            "last_bullet_rows": settings.last_bullet_rows,
            "aliens_num": settings.aliens_num,
            "alien_bullets_num": settings.alien_bullets_num,
            "max_alien_bullets": settings.max_alien_bullets,
            "boss_hp": settings.boss_hp,
            "boss_points": settings.boss_points,
            "asteroid_speed": settings.asteroid_speed,
            "asteroid_freq": settings.asteroid_freq,
            "speedup_scale": settings.speedup_scale,

        }

        for data_name, data_value in data_names.items():
            self.get_data(data_name, data_value)

    def update_alien_states(self):
        """Check the states of the aliens in the game and
        perform corresponding power actions.
        """
        if any(sprite.frozen_state for sprite in self.game.aliens):
            self.game.powers_manager.freeze_enemies()

        if any(sprite.immune_state for sprite in self.game.aliens):
            self.game.powers_manager.alien_upgrade()

    def update_player_ship_states(self):
        """Update the states of the player's ships and perform corresponding actions."""
        ships_to_check = ["thunderbird", "phoenix"]

        # Check individual ship states and perform actions accordingly
        for ship_name in ships_to_check:
            ship_state = getattr(self.game, f"{ship_name}_ship").state
            if ship_state.disarmed:
                self.game.powers_manager.disarm_ship(ship_name)
            if ship_state.shielded:
                self.game.powers_manager.draw_ship_shield(ship_name)
            if ship_state.reverse:
                self.game.powers_manager.reverse_keys(ship_name)
            if ship_state.scaled_weapon:
                self.game.powers_manager.decrease_bullet_size(ship_name)
            if ship_state.immune:
                self.game.powers_manager.invincibility(ship_name)

    def update_player_weapon(self):
        """Updates the player's current weapon based on the loaded data."""
        self.game.weapons_manager.set_weapon("thunderbird", self.game.weapons_manager.weapons["thunderbird"]["current"], loaded=True)
        self.game.weapons_manager.set_weapon("phoenix", self.game.weapons_manager.weapons["phoenix"]["current"], loaded=True)

    def prepare_sprite_data_for_serialization(self):
        """Prepare the sprite data for serialization."""
        alien_sprites = self.data["aliens"]

        return {
            "alien_sprites": [
                {
                    "rect": sprite.rect,
                    "size": sprite.image.get_size(),
                    "image": pygame.image.tostring(sprite.image, "RGBA"),
                    "is_baby": sprite.is_baby if not isinstance(sprite, BossAlien) else False, 
                    "type": "boss" if isinstance(sprite, BossAlien) else "alien",
                    "location": sprite.rect.x,
                    "hit_count": sprite.hit_count,
                    "last_bullet_time": sprite.last_bullet_time,
                    "immune_state": sprite.immune_state if isinstance(sprite, Alien) else None,
                    "frozen_state": sprite.frozen_state,
                }
                for sprite in alien_sprites
            ],
        }

    def save_data(self, name):
        """Saves the current game data to a file."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        sprite_data = self.prepare_sprite_data_for_serialization()

        game_data = {
            "sprite_data": sprite_data,
            **{
                key: self.data[key]
                for key in DATA_KEYS
            },
        }

        with open(file_path, "wb") as file:
            pickle.dump(game_data, file)

    def load_data(self, name):
        """Loads game data from a file and updates the game state."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        with open(file_path, "rb") as file:
            loaded_data = pickle.load(file)

        self.update_game_state_from_data(loaded_data)
        self.restore_sprites_from_data(loaded_data)

    def restore_sprites_from_data(self, loaded_data):
        """Restores the game sprites based on the provided data."""
        sprite_data = loaded_data["sprite_data"]
        alien_sprites = self.game.aliens
        alien_sprites.empty()

        for sprite_state in sprite_data.get("alien_sprites", []):
            size = sprite_state["size"]

            sprite = self.create_alien_sprite(sprite_state["type"], sprite_state, self.game)

            sprite.size = size
            sprite.rect = sprite_state["rect"]
            sprite.image = pygame.image.fromstring(sprite_state["image"], size, "RGBA")
            sprite.x_pos = sprite_state["location"]
            sprite.frozen_state = sprite_state["frozen_state"]
            sprite.immune_state = sprite_state["immune_state"]
            sprite.last_bullet_time = sprite_state["last_bullet_time"]

            alien_sprites.add(sprite)

    def create_alien_sprite(self, sprite_type, sprite_state, game):
        """Create an alien sprite based on the given sprite type and state."""
        if sprite_type == "boss":
            sprite = BossAlien(game)
        elif sprite_type == "alien" and sprite_state["is_baby"]:
            sprite = Alien(game, baby_location=sprite_state["location"], is_baby=True)
            sprite.animation.change_scale(0.5)
        else:
            sprite = Alien(game)

        return sprite

    def update_game_state_from_data(self, loaded_data):
        """Updates the game state based on the loaded data."""
        for key in DATA_KEYS:
            if key in ATTRIBUTE_MAPPING:
                attributes = ATTRIBUTE_MAPPING[key]
                set_attribute(self.game, attributes, loaded_data[key])
            elif hasattr(self.game.stats, key) or hasattr(self.game.settings, key):
                setattr(
                    self.game.stats if hasattr(self.game.stats, key) else self.game.settings,
                    key,
                    loaded_data[key],
                )

