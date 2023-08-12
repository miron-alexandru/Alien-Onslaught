"""
The 'ship' module contains the Ship base class that is used to create
player ships.
"""

import os
import time

import pygame
from pygame.sprite import Sprite

from src.animations.ship_animations import Animations
from src.utils.game_utils import BASE_PATH
from src.utils.constants import SHIPS, ship_image_paths
from src.utils.game_dataclasses import ShipStates


class Ship(Sprite):
    """Base class used to create ships."""

    def __init__(self, game, image_path, conflict_pos, missiles=0):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.image_path = image_path
        self.offset = 0
        self.starting_missiles = 3
        self.missiles_num = missiles
        self.aliens_killed = self.settings.required_kill_count
        self.remaining_bullets = 17 if self.game.singleplayer else 9
        self.image = pygame.image.load(self.image_path)

        self.rect = self.image.get_rect()
        self.cosmic_conflict_pos = conflict_pos

        self.anims = Animations(self)
        self.state = ShipStates()

        self.immune_start_time = 0
        self.small_ship_time = 0
        self.last_bullet_time = 0
        self.scale_counter = 0
        self.ship_selected = False

        self.laser_fired = False
        self.laser_ready = False
        self.laser_ready_msg = False

        self.last_laser_time = 0
        self.laser_ready_start_time = 0.0
        self.last_laser_usage = 0.0

        self.display_power = False
        self.power_name = ""
        self.power_time = 0

        self.ship_type = None
        self.ship_name = ""
        self.last_reverse_power_down_time = None
        self.last_disarmed_power_down_time = None
        self.last_scaled_weapon_power_down_time = None

        self.moving_flags = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }

        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y - 10)
        self.ship_speed = None

    @property
    def ship_speed(self):
        """Returns the speed of the ship based on the ship type."""
        return getattr(self.settings, f"{self.ship_type}_ship_speed")

    @ship_speed.setter
    def ship_speed(self, value):
        self._ship_speed = value

    def update_state(self):
        """Updates the ship state."""
        if (
            self.state.immune
            and pygame.time.get_ticks() - self.immune_start_time
            > self.settings.immune_time
        ):
            self.state.immune = False

        if (
            self.state.scaled
            and time.time() - self.small_ship_time > self.settings.scaled_time
        ):
            self.reset_ship_size()

        if self.state.exploding:
            self.anims.update_explosion_animation()

        elif self.state.warping:
            self.anims.update_warp_animation()

        else:
            self._update_position()

        if self.state.shielded:
            self.anims.update_shield_animation()

        if self.state.immune:
            self.anims.update_immune_animation()

        if self.state.empowered:
            self.anims.update_empower_animation()

        # Update rect object from self.x_pos and self.y_pos
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

    def _update_position(self):
        """Updates the position of the ship based
        on the current state of movement flags.
        """
        direction = -1 if self.state.reverse else 1
        self.x_pos += (
            direction
            * (self.moving_flags["right"] - self.moving_flags["left"])
            * self.ship_speed
        )

        self.y_pos += (
            direction
            * (self.moving_flags["down"] - self.moving_flags["up"])
            * self.ship_speed
        )

        # Keep the ship within the screen boundaries
        self.x_pos = max(0, min(self.x_pos, self.screen_rect.width - self.rect.width))
        self.y_pos = max(0, min(self.y_pos, self.screen_rect.height - self.rect.height))

    def blitme(self):
        """Draws the ship on the screen at its current location and,
        depending on the current state of the ship, it draws the corresponding animation.
        """
        if self.state.warping:
            self.screen.blit(self.anims.warp_frames[self.anims.warp_index], self.rect)
            return

        if self.state.exploding:
            self.screen.blit(self.anims.explosion_image, self.anims.explosion_rect)
            return

        # Draw regular ship image
        self.screen.blit(self.image, self.rect)

        if self.state.shielded:
            self.screen.blit(self.anims.shield_image, self.anims.shield_rect)

        if self.state.immune:
            self.screen.blit(self.anims.immune_image, self.anims.immune_rect)

        if self.state.empowered:
            self.screen.blit(self.anims.empower_image, self.anims.empower_rect)

    def center_ship(self):
        """Center the ship on the screen."""
        if self.settings.game_modes.cosmic_conflict:
            self.rect.bottom = self.screen_rect.centery
            x_pos = self.cosmic_conflict_pos
        else:
            self.rect.bottom = self.screen_rect.bottom
            x_pos = (
                self.screen_rect.centerx
                if self.game.singleplayer
                else self.screen_rect.centerx + self.offset
            )

        self.x_pos = x_pos
        self.y_pos = float(self.rect.y - 10)

    def draw_shield(self):
        """Sets the shielded state to True."""
        self.state.shielded = True
        self.anims.shield_rect.center = self.rect.center

    def explode(self):
        """Sets the exploding state to True."""
        self.state.exploding = True
        self.anims.explosion_rect.center = self.rect.center

    def start_warp(self):
        """Sets the warping state to True."""
        self.state.warping = True

    def set_immune(self):
        """Sets the immuen state to True."""
        self.state.immune = True
        self.anims.immune_rect.center = self.rect.center
        self.immune_start_time = pygame.time.get_ticks()

    def empower(self):
        """Sets the empowered state to True."""
        self.state.empowered = True

    def update_missiles_number(self):
        """Update the number of missiles."""
        if self.settings.game_modes.one_life_reign:
            self.missiles_num = 6
        elif self.settings.game_modes.last_bullet:
            self.missiles_num = 1
        else:
            self.missiles_num = self.starting_missiles

    def scale_ship(self, scale_factor):
        """Change the ship's size and set the scaled
        state to True."""
        self.anims.change_ship_size(scale_factor)
        self.state.scaled = True

    def reset_ship_size(self):
        """Reset the ship to the original state and size."""
        self.anims.reset_size()

        ship_type = "thunderbird" if self.ship_type == "thunderbird" else "phoenix"
        self.image_path = os.path.join(
            BASE_PATH, ship_image_paths.get(self.ship_name, SHIPS[f"{ship_type}1"])
        )
        self.image = pygame.image.load(self.image_path)

        self.rect = self.image.get_rect()

        self.state.scaled = False
        self.small_ship_time = time.time()
        self.scale_counter = 0

    def reset_ship_state(self):
        """Reset ship states and other variables."""
        self.state.disarmed = False
        self.state.reverse = False
        self.state.scaled_weapon = False
        self.state.shielded = False
        self.state.immune = False
        self.ship_selected = False

        self.aliens_killed = self.settings.required_kill_count
        self.last_laser_time = 0
        self.laser_fired = False
        self.laser_ready = False
        self.laser_ready_start_time = 0.0
        self.last_laser_usage = 0.0
        self.laser_ready_msg = False

    def update_speed_from_settings(self, player):
        """Updates the ship speed attribute based on the current value
        in the settings file for the specified player.
        """
        self.ship_speed = getattr(self.settings, f"{player}_ship_speed")
