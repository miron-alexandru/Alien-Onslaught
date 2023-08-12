"""
The "missile" module contains the Missile class used to create
missile instances.
"""

import pygame
from pygame.sprite import Sprite

from src.animations.entities_animations import MissileEx
from src.utils.animation_constants import missile_frames


class Missile(Sprite):
    """The Missile class represents a missile object in the game.
    It also creates an instance of MissileEx class to manage the
    explosion animation for the missile.
    """

    def __init__(self, game, ship):
        super().__init__()
        self.game = game
        self.ship = ship
        self.settings = game.settings
        self.screen = self.game.screen

        self.destroy_delay = 50
        self.frames = missile_frames
        self.current_frame = 0
        self.set_missile_frames()
        self.rect = self.frames[0].get_rect()
        self.rect.midtop = (self.ship.rect.centerx, self.ship.rect.top)

        self.y_pos = float(self.rect.y)
        self.x_pos = float(self.rect.x)

        self.frame_update_rate = 5
        self.frame_counter = 0

        self.destroy_anim = MissileEx(self)
        self.is_destroyed = False

    def update(self):
        """Update the missile's position and animation."""
        if self.is_destroyed:
            self._update_destroyed_state()
        else:
            self._update_normal_state()

    def _update_destroyed_state(self):
        """Update the missile when it's in the destroyed state."""
        if self.destroy_delay > 0:
            self.destroy_anim.update_animation()
            self.destroy_delay -= 1
        else:
            self.kill()

    def _update_normal_state(self):
        """Update the missile when it's in the normal state."""
        self._update_animation_frame()

        if self.settings.game_modes.cosmic_conflict:
            self._update_position_cosmic_conflict()
        else:
            self._update_position_standard()

    def _update_animation_frame(self):
        """Update the missile's animation frame."""
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.set_missile_frames()
            self.frame_counter = 0

    def _update_position_cosmic_conflict(self):
        """Update the missile's position in the Cosmic Conflict game mode."""
        speed = self.settings.missiles_speed

        if self.ship == self.game.thunderbird_ship:
            self.x_pos += speed
        else:
            self.x_pos -= speed

        self.rect.x = self.x_pos

    def _update_position_standard(self):
        """Update the missile's position in standard game mode."""
        self.y_pos -= self.settings.missiles_speed
        self.rect.y = self.y_pos

    def set_missile_frames(self):
        """Set the missile's image frame based
        on its current state and game mode.
        """
        if self.settings.game_modes.cosmic_conflict:
            self._set_missile_frames_cosmic_conflict()
        else:
            self.image = self.frames[self.current_frame]

    def _set_missile_frames_cosmic_conflict(self):
        """Set the missile frames in the cosmic conflict game mode."""
        if self.ship == self.game.thunderbird_ship:
            self.image = pygame.transform.rotate(self.frames[self.current_frame], -90)
        else:
            self.image = pygame.transform.rotate(self.frames[self.current_frame], 90)

    def draw(self):
        """Draw the missile or explosion effect,
        depending on whether it's destroyed or not."""
        if self.is_destroyed:
            self.destroy_anim.draw_explosion()
        else:
            self.screen.blit(self.image, self.rect)

    def explode(self):
        """Trigger the explosion effect."""
        self.is_destroyed = True
