"""
The 'projectiles' module contains classes for creating different projectiles
available in the game.

Classes:
    - 'Thunderbolt': A class that manages bullets for the Thunderbird ship.
    - 'Firebird': A class that manages bullets for the Phoenix ship.
    - 'Missile': A class that manages missles that the players have in the game.
    - 'Laser': A class that manager the laser weapon for the players.
"""

import time
import pygame
from pygame.sprite import Sprite
from src.utils.animation_constants import missile_frames, laser_frames
from src.animations.other_animations import MissileEx


class Bullet(Sprite):
    """A base bullet class used to create bullets."""

    def __init__(self, game, image_path, ship, speed):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.ship = ship
        self.image = image_path
        self.rect = self.image.get_rect()
        self.rect.midtop = (ship.rect.centerx, ship.rect.top)
        self.y_pos = float(self.rect.y)
        self.x_pos = float(self.rect.x)
        self.speed = speed

    def update(self):
        """Update the bullet location on screen."""
        if self.settings.game_modes.cosmic_conflict:
            self.x_pos += (
                self.speed if self.ship == self.game.thunderbird_ship else -self.speed
            )
            self.rect.x = int(self.x_pos)
        else:
            self.y_pos -= self.speed
            self.rect.y = int(self.y_pos)

    def draw(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

    def scale_bullet(self, scale):
        """Scale the bullet image and rect."""
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )
        self.rect = self.image.get_rect(center=self.rect.center)


class Thunderbolt(Bullet):
    """A class to manage bullets for Thunderbird ship."""

    def __init__(self, manager, ship, scaled=False):
        super().__init__(
            manager,
            manager.weapons["thunderbird"]["weapon"],
            ship,
            manager.settings.thunderbird_bullet_speed,
        )
        if manager.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, -90)
        if scaled:
            self.scale_bullet(0.5)


class Firebird(Bullet):
    """A class to manage bullets for Phoenix ship."""

    def __init__(self, manager, ship, scaled=False):
        super().__init__(
            manager,
            manager.weapons["phoenix"]["weapon"],
            ship,
            manager.settings.phoenix_bullet_speed,
        )
        if manager.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, 90)
        if scaled:
            self.scale_bullet(0.5)


class Missile(Sprite):
    """The Missile class represents a missile object in the game.
    It also creates an instance of MissileEx class to manage the
    explosion animation for the missile.
    """

    def __init__(self, game, ship):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.ship = ship
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
            if self.destroy_delay > 0:
                self.destroy_anim.update_animation()
                self.destroy_delay -= 1
            else:
                self.kill()
        else:
            self.frame_counter += 1
            if self.frame_counter % self.frame_update_rate == 0:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.set_missile_frames()
                self.frame_counter = 0

            if self.settings.game_modes.cosmic_conflict:
                self.x_pos += (
                    self.settings.missiles_speed
                    if self.ship == self.game.thunderbird_ship
                    else -self.settings.missiles_speed
                )
                self.rect.x = self.x_pos
            else:
                self.y_pos -= self.settings.missiles_speed
                self.rect.y = self.y_pos

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

    def set_missile_frames(self):
        """Set the missile's image frame based
        on its current state and game mode.
        """
        if self.settings.game_modes.cosmic_conflict:
            if self.ship == self.game.thunderbird_ship:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], -90
                )
            else:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], 90
                )
        else:
            self.image = self.frames[self.current_frame]


class Laser(Sprite):
    """The Laser class represents a laser object in the game."""

    def __init__(self, game, ship):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.ship = ship

        self.frames = laser_frames
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.set_laser_frames()
        self.rect.midbottom = ship.rect.midtop

        self.frame_update_rate = 5
        self.frame_counter = 0

        self.duration = 1
        self.start_time = time.time()

    def update(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.set_laser_frames()
            self.frame_counter = 0

        if time.time() - self.start_time >= self.duration or self.ship.state.exploding:
            self.kill()

        if self.settings.game_modes.cosmic_conflict:
            if self.ship == self.game.thunderbird_ship:
                self.rect.midleft = self.ship.rect.midright
            else:
                self.rect.midright = self.ship.rect.midleft
        else:
            self.rect.midbottom = self.ship.rect.midtop

    def draw(self):
        """Draw laser on screen."""
        self.screen.blit(self.image, self.rect)

    def set_laser_frames(self):
        """Set the image of the laser based
        on its current state and game mode.
        """
        if self.settings.game_modes.cosmic_conflict:
            if self.ship == self.game.thunderbird_ship:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], -90
                )
            else:
                self.image = pygame.transform.rotate(
                    self.frames[self.current_frame], 90
                )
            self.rect = self.image.get_rect()
        else:
            self.image = self.frames[self.current_frame]
