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


class Thunderbird(Sprite):
    """A class to manage the Thunderbird ship. This class also
    creates instances of Animations and ShipStates class and dataclass
    that are managing the ship's animation and state."""
    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(SHIPS['thunderbird'])

        self.rect = self.image.get_rect()
        self.rect.x = (
            self.screen_rect.centerx
            if self.game.singleplayer
            else self.screen_rect.centerx - 300
        )

        self.rect.y = self.screen_rect.bottom - self.rect.height
        self.anims = Animations(self)
        self.state = ShipStates()

        self.immune_start_time = 0
        self.small_ship_time = 0
        self.last_bullet_time = 0
        self.remaining_bullets = 17 if self.game.singleplayer else 9
        self.missiles_num = self.settings.thunderbird_missiles_num

        self.moving_flags = {
            'right': False,
            'left': False,
            'up': False,
            'down': False,
        }

        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y - 10)

    def update_state(self):
        """Updates the ship state and position."""
        if (self.state.immune and pygame.time.get_ticks() - self.immune_start_time >
                self.settings.immune_time):
            self.state.immune = False

        if (self.state.scaled and pygame.time.get_ticks() - self.small_ship_time >
                self.settings.scaled_time):
            self.reset_ship_state()

        if self.state.exploding:
            self.anims.update_explosion_animation()

        elif self.state.warping:
            self.anims.update_warp_animation()

        else:
            self._update_position()

        if self.state.shielded:
            self.anims.update_animation('shield')

        if self.state.immune:
            self.anims.update_animation('immune')

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
        self.x_pos += direction * (self.moving_flags['right'] - self.moving_flags['left']) \
                    * self.settings.thunderbird_ship_speed

        self.y_pos += direction * (self.moving_flags['down'] - self.moving_flags['up']) \
                    * self.settings.thunderbird_ship_speed

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
        self.rect.bottom = self.screen_rect.bottom
        self.x_pos = (
            self.screen_rect.centerx
            if self.game.singleplayer
            else self.screen_rect.centerx - 300
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
        self.missiles_num = self.settings.thunderbird_missiles_num

    def reverse_keys(self):
        """Toggles the reverse state."""
        self.state.reverse = not self.state.reverse

    def disarm(self):
        """Toggles the disarmed state."""
        self.state.disarmed = not self.state.disarmed

    def scale_ship(self, scale_factor):
        """Change the ship's size and set the scaled
        state to True."""
        self.anims.change_ship_size(scale_factor)
        self.state.scaled = True

    def reset_ship_state(self):
        """Reset the ship to the original state and size."""
        self.image = pygame.image.load(SHIPS['thunderbird'])
        self.rect = self.image.get_rect()
        self.anims.reset_size()

        self.state.scaled = False
        self.small_ship_time = pygame.time.get_ticks()
        self.state.disarmed = False
        self.state.reverse = False



class Phoenix(Thunderbird):
    """A class to manage the Phoenix ship."""
    def __init__(self, game):
        super().__init__(game)
        self.settings = game.settings
        self.image = pygame.image.load(SHIPS['phoenix'])
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.centerx + 200
        self.rect.y = self.screen_rect.bottom - self.rect.height

        self.missiles_num = self.settings.phoenix_missiles_num

    def _update_position(self):
        """Updates the position of the ship based 
        on the current state of movement flags.
        """
        direction = -1 if self.state.reverse else 1
        self.x_pos += direction * (self.moving_flags['right'] - self.moving_flags['left']) \
                    * self.settings.phoenix_ship_speed
        self.y_pos += direction * (self.moving_flags['down'] - self.moving_flags['up']) \
                    * self.settings.phoenix_ship_speed

        # Keep the ship within the screen boundaries
        self.x_pos = max(0, min(self.x_pos, self.screen_rect.width - self.rect.width))
        self.y_pos = max(0, min(self.y_pos, self.screen_rect.height - self.rect.height))

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.bottom = self.screen_rect.bottom
        self.x_pos = self.screen_rect.centerx + 200
        self.y_pos = float(self.rect.y - 10)

    def update_missiles_number(self):
        """Update the number of missiles."""
        self.missiles_num = self.settings.thunderbird_missiles_num

    def reset_ship_state(self):
        """Reset the ship to the original state and size."""
        self.image = pygame.image.load(SHIPS['phoenix'])
        self.rect = self.image.get_rect()
        self.anims.reset_size()

        self.state.scaled = False
        self.small_ship_time = pygame.time.get_ticks()
        self.state.disarmed = False
        self.state.reverse = False


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
    firing: bool = False
