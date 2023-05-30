"""
The 'ships' module contains classes for managing the player ships in the game.

Classes:
    - 'Thunderbird': Represents the Thunderbird ship in the game.
    - 'Phoenix': Represents the Phoenix ship in the game.
    - 'ShipStates': A dataclass that manages the state of the ships.
"""

from dataclasses import dataclass
import pygame
from pygame.sprite import Sprite
from animations.ship_animations import Animations
from utils.constants import SHIPS


class Ship(Sprite):
    """Base class used to create ships in the game."""

    def __init__(self, game, image_path, conflict_pos, missiles=0):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.image_path = image_path
        self.offset = 0
        self.starting_missiles = 3
        self.missiles_num = missiles
        self.ship_type = None
        self.image = pygame.image.load(self.image_path)

        self.rect = self.image.get_rect()
        self.cosmic_conflict_pos = conflict_pos

        self.anims = Animations(self)
        self.state = ShipStates()

        self.immune_start_time = 0
        self.small_ship_time = 0
        self.last_bullet_time = 0
        self.last_reverse_power_down_time = None
        self.last_disarmed_power_down_time = None
        self.last_scaled_weapon_power_down_time = None
        self.remaining_bullets = 17 if self.game.singleplayer else 9

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
        """Updates the ship state and position."""
        if (
            self.state.immune
            and pygame.time.get_ticks() - self.immune_start_time
            > self.settings.immune_time
        ):
            self.state.immune = False

        if (
            self.state.scaled
            and pygame.time.get_ticks() - self.small_ship_time
            > self.settings.scaled_time
        ):
            self.reset_ship_state()

        if self.state.exploding:
            self.anims.update_explosion_animation()

        elif self.state.warping:
            self.anims.update_warp_animation()

        else:
            self._update_position()

        if self.state.shielded:
            self.anims.update_animation("shield")

        if self.state.immune:
            self.anims.update_animation("immune")

        if self.state.empowered:
            self.anims.update_animation("empower")

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
        """Draws the ship on the screen at its current location.
        Depending on the current state of the ship,
        it draws the corresponding animation.
        """
        if self.state.warping:
            # If the ship is warping, draw the warp animation
            self.screen.blit(self.anims.warp_frames[self.anims.warp_index], self.rect)
            return

        if self.state.exploding:
            # If the ship is exploding, draw the explosion
            self.screen.blit(self.anims.explosion_image, self.anims.explosion_rect)
            return

        # Draw regular ship image
        self.screen.blit(self.image, self.rect)

        if self.state.shielded:
            # Draw shield if shielded
            self.screen.blit(self.anims.shield_image, self.anims.shield_rect)

        if self.state.immune:
            # Draw immune image if immune
            self.screen.blit(self.anims.immune_image, self.anims.immune_rect)

        if self.state.empowered:
            # Draw empower image if empowered
            self.screen.blit(self.anims.empower_image, self.anims.empower_rect)

    def center_ship(self):
        """Center the ship on the screen."""
        if self.settings.game_modes.cosmic_conflict:
            self.rect.bottom = self.screen_rect.centery
        else:
            self.rect.bottom = self.screen_rect.bottom
        self.x_pos = (
            (
                self.screen_rect.centerx
                if self.game.singleplayer
                else self.screen_rect.centerx + self.offset
            )
            if not self.settings.game_modes.cosmic_conflict
            else self.cosmic_conflict_pos
        )
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
        self.missiles_num = (6 if self.settings.game_modes.one_life_reign
            else self.starting_missiles)

    def scale_ship(self, scale_factor):
        """Change the ship's size and set the scaled
        state to True."""
        self.anims.change_ship_size(scale_factor)
        self.state.scaled = True

    def reset_ship_state(self):
        """Reset the ship to the original state and size."""
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.anims.reset_size()

        self.state.scaled = False
        self.small_ship_time = pygame.time.get_ticks()
        self.state.disarmed = False
        self.state.reverse = False
        self.state.scaled_weapon = False

    def update_speed_from_settings(self, player):
        """Updates the ship speed attribute based on the current value
        in the settings file for the specified player.
        """
        self.ship_speed = getattr(self.settings, f"{player}_ship_speed")


class Thunderbird(Ship):
    """Class that represents the Thunderbird ship in the game."""

    def __init__(self, game):
        self.screen_rect = game.screen.get_rect()
        super().__init__(game, SHIPS["thunderbird"], self.screen_rect.left + 10)
        self.missiles_num = game.settings.thunderbird_missiles_num
        self.ship_type = "thunderbird"
        self.offset = -300

    def set_cosmic_conflict_pos(self):
        """The the ship position for the Cosmic Conflict game mode."""
        if self.game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, -90)
        self.cosmic_conflict_pos = self.screen_rect.left + 10


class Phoenix(Ship):
    """Class that represents the Phoenix ship in the game."""

    def __init__(self, game):
        self.screen_rect = game.screen.get_rect()
        super().__init__(game, SHIPS["phoenix"], self.screen_rect.right - 50)
        self.missiles_num = game.settings.phoenix_missiles_num
        self.ship_type = "phoenix"
        self.offset = 200

    def set_cosmic_conflict_pos(self):
        """Set the ship position for the Cosmic Conflict game Mode"""
        if self.game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, 90)
        self.cosmic_conflict_pos = self.screen_rect.right - 50


@dataclass
class ShipStates:
    """A dataclass to manage ship states."""

    alive: bool = True
    exploding: bool = False
    shielded: bool = False
    warping: bool = False
    single_player: bool = False
    immune: bool = False
    empowered: bool = False
    reverse: bool = False
    disarmed: bool = False
    scaled: bool = False
    scaled_weapon: bool = False
    firing: bool = False
