"""The ships module contains the class definitons for the ships in the game"""

from dataclasses import dataclass
import pygame
from pygame.sprite import Sprite
from animations.ship_animations import Animations
from utils.constants import SHIPS


class Thunderbird(Sprite):
    """A class to manage the Thunderbird ship."""
    def __init__(self, game, singleplayer=False):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(SHIPS['thunderbird'])

        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.centerx if singleplayer else self.screen_rect.centerx - 300
        self.rect.y = self.screen_rect.bottom - self.rect.height
        self.anims = Animations(self)
        self.state = ShipStates()

        self.immune_start_time = 0
        self.remaining_bullets = 17 if singleplayer else 9
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
        if self.state.immune and pygame.time.get_ticks() - self.immune_start_time > 4000:
            self.state.immune = False

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
        """Updates the position of the ship based on the current state of movement flags."""
        if self.moving_flags['right'] and self.rect.right < self.screen_rect.right:
            self.x_pos += self.settings.thunderbird_ship_speed
        if self.moving_flags['left'] and self.rect.left > 0:
            self.x_pos -= self.settings.thunderbird_ship_speed
        if self.moving_flags['up'] and self.rect.top > 0:
            self.y_pos -= self.settings.thunderbird_ship_speed
        if self.moving_flags['down'] and self.rect.bottom <= self.screen_rect.bottom:
            self.y_pos += self.settings.thunderbird_ship_speed

    def blitme(self):
        """Draws the ship on the screen at its current location."""
        if not self.state.alive:
            return

        # If the ship is warping, display the warp animation
        if self.state.warping:
            self.screen.blit(self.anims.warp_frames[self.anims.warp_index], self.rect)

        # If the ship is not exploding, display regular ship image
        elif not self.state.exploding:
            self.screen.blit(self.image, self.rect)

            # If shield is on, display the shield
            if self.state.shielded:
                self.screen.blit(self.anims.shield_image, self.anims.shield_rect)

            if self.state.immune:
                self.screen.blit(self.anims.immune_image, self.anims.immune_rect)

            if self.state.empowered:
                self.screen.blit(self.anims.empower_image, self.anims.empower_rect)
        else:
            # display the explosion
            self.screen.blit(self.anims.explosion_image, self.anims.explosion_rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.bottom = self.screen_rect.bottom
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y - 10)

    def draw_shield(self):
        """Turns the shield on"""
        self.state.shielded = True
        self.anims.shield_rect.center = self.rect.center

    def explode(self):
        """Starts the explosion animation"""
        self.state.exploding = True
        self.anims.explosion_rect.center = self.rect.center

    def start_warp(self):
        """Starts the warp animation"""
        self.state.warping = True

    def set_immune(self):
        """Starts the immune animation."""
        self.state.immune = True
        self.anims.immune_rect.center = self.rect.center
        self.immune_start_time = pygame.time.get_ticks()

    def empower(self):
        """Start the empower effect."""
        self.state.empowered = True

    def update_missiles_number(self):
        """Update the number of missiles"""
        self.missiles_num = self.settings.thunderbird_missiles_num



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
        """Updates the position of the ship based on the current state of movement flags."""
        if self.moving_flags['right'] and self.rect.right < self.screen_rect.right:
            self.x_pos += self.settings.phoenix_ship_speed
        if self.moving_flags['left'] and self.rect.left > 0:
            self.x_pos -= self.settings.phoenix_ship_speed
        if self.moving_flags['up'] and self.rect.top > 0:
            self.y_pos -= self.settings.phoenix_ship_speed
        if self.moving_flags['down'] and self.rect.bottom <= self.screen_rect.bottom:
            self.y_pos += self.settings.phoenix_ship_speed

    def update_missiles_number(self):
        """Update the number of missiles."""
        self.missiles_num = self.settings.thunderbird_missiles_num


@dataclass
class ShipStates:
    """This dataclass manages ship states"""
    alive: bool = True
    exploding: bool = False
    shielded: bool = False
    warping: bool = False
    single_player: bool = False
    immune: bool = False
    empowered: bool = False
