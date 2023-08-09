"""
The save_load_manager module contains the SaveLoadSystem class that
implements the functionality of saving and loading the game from a save file.
"""

import datetime
import pickle
import os
import sys

import tkinter as tk
from tkinter import messagebox

import pygame

from src.entities.alien_entities.aliens import Alien, BossAlien
from src.utils.constants import (
    DATA_KEYS,
    ATTRIBUTE_MAPPING,
    SLOT_HEIGHT,
    TEXT_PADDING_X,
    TEXT_PADDING_Y,
    SELECTED_SLOT_COLOR,
    BORDER_WIDTH,
)
from src.utils.game_utils import (
    set_attribute,
    display_simple_message,
    play_sound,
    create_save_dir,
)


class SaveLoadSystem:
    """This class implements the Save/Load funcionality in the game."""

    def __init__(self, game, file_extension, save_folder):
        self.game = game
        self.screen = game.screen
        self.file_extension = file_extension
        self.save_folder = save_folder
        self.menu_running = False

        self.data = {}
        create_save_dir(self.save_folder)

        self.font = pygame.font.SysFont("verdana", 22)
        self.text_color = (225, 225, 225)

        self.center_x = self.screen.get_width() // 2

        self.cancel_text = self.font.render("Exit", True, self.text_color)
        self.delete_text = self.font.render("Clear Saves", True, self.text_color)

        self.cancel_rect = self.cancel_text.get_rect(
            center=(self.screen.get_width() // 2 + 100, 465)
        )
        self.delete_rect = self.delete_text.get_rect(
            center=(self.screen.get_width() // 2 - 100, 465)
        )

        self.set_screen_title_position()

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
            "thunderbird_weapon_current": game.weapons_manager.weapons["thunderbird"][
                "current"
            ],
            "thunderbird_alive": thunderbird_ship.state.alive,
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
            "phoenix_weapon_current": game.weapons_manager.weapons["phoenix"][
                "current"
            ],
            "phoenix_alive": phoenix_ship.state.alive,
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
        self.game.weapons_manager.set_weapon(
            "thunderbird",
            self.game.weapons_manager.weapons["thunderbird"]["current"],
            loaded=True,
        )
        self.game.weapons_manager.set_weapon(
            "phoenix",
            self.game.weapons_manager.weapons["phoenix"]["current"],
            loaded=True,
        )

    def prepare_sprite_data_for_serialization(self):
        """Prepare the sprite data for serialization."""
        alien_sprites = self.data["aliens"]

        return {
            "alien_sprites": [
                {
                    "rect": sprite.rect,
                    "size": sprite.image.get_size(),
                    "image": pygame.image.tostring(sprite.image, "RGBA"),
                    "is_baby": False
                    if isinstance(sprite, BossAlien)
                    else sprite.is_baby,
                    "type": "boss" if isinstance(sprite, BossAlien) else "alien",
                    "location": sprite.rect.x,
                    "hit_count": sprite.hit_count,
                    "last_bullet_time": sprite.last_bullet_time,
                    "immune_state": sprite.immune_state
                    if isinstance(sprite, Alien)
                    else None,
                    "frozen_state": sprite.frozen_state,
                }
                for sprite in alien_sprites
            ],
        }

    def save_data(self, name, save_date):
        """Saves the current game data to a file."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        sprite_data = self.prepare_sprite_data_for_serialization()

        game_data = {
            "sprite_data": sprite_data,
            **{key: self.data[key] for key in DATA_KEYS},
            "save_date": save_date,
        }
        with open(file_path, "wb") as file:
            pickle.dump(game_data, file)

    def load_data(self, name):
        """Loads game data from a file and updates the game state."""
        file_path = os.path.join(self.save_folder, f"{name}.{self.file_extension}")
        try:
            with open(file_path, "rb") as file:
                loaded_data = pickle.load(file)
                self.update_game_state_from_data(loaded_data)
                self.restore_sprites_from_data(loaded_data)
        except FileNotFoundError:
            play_sound(self.game.sound_manager.game_sounds, "empty_save")

    def restore_sprites_from_data(self, loaded_data):
        """Restores the game sprites based on the provided data."""
        sprite_data = loaded_data["sprite_data"]
        alien_sprites = self.game.aliens
        alien_sprites.empty()

        for sprite_state in sprite_data.get("alien_sprites", []):
            size = sprite_state["size"]

            sprite = self.create_alien_sprite(
                sprite_state["type"], sprite_state, self.game
            )

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
                    self.game.stats
                    if hasattr(self.game.stats, key)
                    else self.game.settings,
                    key,
                    loaded_data[key],
                )

    def handle_save_load_menu(self, save=False):
        """Displays the save or the load menu, allowing the user
        to select and interact with available save slots.
        """
        # Create the save directory and get the list of save files
        self.menu_running = True

        save_files = self._get_save_files()
        slot_selected = 0
        slot_rects = []

        while self.menu_running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        play_sound(self.game.sound_manager.game_sounds, "keypress")
                        slot_selected = (slot_selected - 1) % 3
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        play_sound(self.game.sound_manager.game_sounds, "keypress")
                        slot_selected = (slot_selected + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        self._handle_save_slot_action(self.font, slot_selected, save)
                        return
                    elif event.key == pygame.K_ESCAPE:
                        play_sound(self.game.sound_manager.game_sounds, "keypress")
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, rect in enumerate(slot_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            slot_selected = i
                            self._handle_save_slot_action(
                                self.font, slot_selected, save
                            )
                            return

                    if self.cancel_rect.collidepoint(mouse_x, mouse_y):
                        play_sound(self.game.sound_manager.game_sounds, "click")
                        return

                    if self.delete_rect.collidepoint(mouse_x, mouse_y):
                        play_sound(self.game.sound_manager.game_sounds, "click")
                        if confirm := self._show_confirmation_popup():
                            play_sound(self.game.sound_manager.game_sounds, "click")
                            self._delete_all_save_files()
                        else:
                            play_sound(self.game.sound_manager.game_sounds, "click")
                elif event.type == pygame.VIDEORESIZE:
                    self.game.screen_manager.resize_screen(event.size)
                    self.game.screen_manager.update_buttons()

            # Render the display
            self.screen.blit(self.game.bg_img, [0, 0])
            self.display_screen_title(save)
            self._draw_save_slots(
                self.font,
                self.text_color,
                self.center_x,
                save_files,
                slot_selected,
                slot_rects,
            )
            self.screen.blit(self.cancel_text, self.cancel_rect)
            self.screen.blit(self.delete_text, self.delete_rect)
            self.game.screen_manager.draw_cursor()
            pygame.display.flip()

    def _get_save_files(self):
        """Get the list of save files from the specified save folder."""
        file_list = os.listdir(self.save_folder)
        return [
            f
            for f in file_list
            if os.path.isfile(os.path.join(self.save_folder, f))
            and f.endswith(self.file_extension)
        ]

    def _get_save_status_text(self, slot_number, save_files):
        """Get the status text for the specified save slot number."""
        save_file_name = f"save{slot_number}.save"
        if save_file_name not in save_files:
            return "Empty"

        try:
            save_file_path = os.path.join(self.save_folder, save_file_name)
            save_date = os.path.getmtime(save_file_path)
            save_date_str = datetime.datetime.fromtimestamp(save_date).strftime(
                "%d %b %Y  %I:%M %p"
            )
            return f"Saved On: {save_date_str}"
        except FileNotFoundError:
            return "Empty"

    def _draw_save_slots(
        self, font, text_color, center_x, save_files, slot_selected, slot_rects
    ):
        """Display the save slots on the screen."""
        for i, slot_number in enumerate(range(1, 4)):
            status_text = self._get_save_status_text(slot_number, save_files)
            text = font.render(
                f"Save File {slot_number}: {status_text}", True, text_color
            )
            text_rect = text.get_rect(center=(center_x, 300 + i * SLOT_HEIGHT))
            slot_rects.append(text_rect)

            self.screen.blit(text, text_rect)

            rect = pygame.Rect(
                text_rect.left - TEXT_PADDING_X,
                text_rect.top - TEXT_PADDING_Y,
                text_rect.width + 2 * TEXT_PADDING_X,
                text_rect.height + 2 * TEXT_PADDING_Y,
            )

            if i == slot_selected:
                pygame.draw.rect(self.screen, SELECTED_SLOT_COLOR, rect, BORDER_WIDTH)

    def _handle_save_slot_action(self, font, slot_selected, save):
        """Handle the action for the selected save slot."""
        if save:
            self._handle_save_action(font, slot_selected)
        else:
            self._handle_load_action(font, slot_selected)

    def _handle_save_action(self, font, slot_selected):
        """Handle the action when saving the game."""
        save_files = self._get_save_files()
        if f"save{slot_selected + 1}.save" in save_files:
            if confirm_overwrite := self._show_confirmation_popup(
                delete_save_files=False
            ):
                self._save_game(font, slot_selected)
            else:
                play_sound(self.game.sound_manager.game_sounds, "click")
        else:
            self._save_game(font, slot_selected)

    def _handle_load_action(self, font, slot_selected):
        """Handle the action when loading the game from a save file."""
        save_files = self._get_save_files()
        if f"save{slot_selected + 1}.save" in save_files:
            play_sound(self.game.sound_manager.game_sounds, "load_game")
            self.load_data(f"save{slot_selected + 1}")
            self.game.game_loaded = True
            display_simple_message(self.screen, "Game Loaded!", font, "lightblue", 1000)
        else:
            play_sound(self.game.sound_manager.game_sounds, "empty_save")
            display_simple_message(self.screen, "Empty save slot", font, "red", 500)

    def _save_game(self, font, slot_selected):
        """Save the game state and display a message."""
        play_sound(self.game.sound_manager.game_sounds, "click")
        save_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data(f"save{slot_selected + 1}", save_date=save_date)
        display_simple_message(self.screen, "Game Saved!", font, "lightblue", 1000)

    def _delete_all_save_files(self):
        """Deletes all save files from the save folder."""
        save_files = self._get_save_files()

        for save_file in save_files:
            save_file_path = os.path.join(self.save_folder, save_file)
            os.remove(save_file_path)

    def _show_confirmation_popup(self, delete_save_files=True):
        """Display a confirmation popup."""
        root = tk.Tk()
        root.withdraw()

        if delete_save_files:
            user_response = messagebox.askyesno(
                "Confirmation", "Delete all save files?"
            )
        else:
            user_response = messagebox.askyesno(
                "Confirmation", "Overwrite this save file?"
            )

        root.destroy()
        return user_response

    def update_rect_positions(self):
        """Update the positions of UI elements based on the current screen width."""
        self.center_x = self.screen.get_width() // 2

        self.cancel_rect.center = (self.screen.get_width() // 2 + 100, 465)
        self.delete_rect.center = (self.screen.get_width() // 2 - 100, 465)

    def set_screen_title_position(self):
        """Set the location of the screen title images on the screen."""
        center_y = self.screen.get_height() // 2 - 180

        self.game.settings.save_game_rect.center = (
            self.game.settings.load_game_rect.center
        ) = (self.center_x, center_y)

    def display_screen_title(self, save):
        """Display the correct screen title for the save or load screen."""
        if save:
            self.screen.blit(
                self.game.settings.save_game_img, self.game.settings.save_game_rect
            )
        else:
            self.screen.blit(
                self.game.settings.load_game_img, self.game.settings.load_game_rect
            )
