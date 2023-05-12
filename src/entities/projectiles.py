"""
The 'projectiles' module contains classes for managing different projectiles
available in the game.

Classes:
    - 'Thunderbolt': A class that manages bullets for the Thunderbird ship.
    - 'Firebird': A class that manages bullets for the Phoenix ship.
    - 'Missile': A class that manages missles that the players have in the game.
    - 'BulletsManager': A class that manages player bullets.
"""

import pygame
from pygame.sprite import Sprite
from utils.animation_constants import missile_frames
from utils.constants import WEAPONS
from animations.other_animations import MissileEx


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
            self.rect.x = self.x_pos
        else:
            self.y_pos -= self.speed
            self.rect.y = self.y_pos

    def draw(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)


class Thunderbolt(Bullet):
    """A class to manage bullets for Thunderbird ship."""

    def __init__(self, game, ship):
        super().__init__(
            game,
            game.bullets_manager.weapons["thunderbird"]["weapon"],
            ship,
            game.settings.thunderbird_bullet_speed,
        )
        if game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, -90)


class Firebird(Bullet):
    """A class to manage bullets for Phoenix ship."""

    def __init__(self, game, ship):
        super().__init__(
            game,
            game.bullets_manager.weapons["phoenix"]["weapon"],
            ship,
            game.settings.phoenix_bullet_speed,
        )
        if game.settings.game_modes.cosmic_conflict:
            self.image = pygame.transform.rotate(self.image, 90)


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


class BulletsManager:
    """The BulletsManager class manages the changing and update
    of the player bullets.
    """

    def __init__(self, game):
        self.game = game
        self.game_modes = self.game.settings.game_modes
        self.screen = game.screen
        self.weapons = {
            "thunderbird": {
                "weapon": pygame.image.load(WEAPONS["thunderbolt"]),
                "current": "thunderbolt",
            },
            "phoenix": {
                "weapon": pygame.image.load(WEAPONS["firebird"]),
                "current": "firebird",
            },
        }

    def set_weapon(self, player, weapon_name):
        """Change the player weapon."""
        if weapon := self.weapons.get(player):
            if weapon_name == weapon["current"] and not self.game_modes.last_bullet:
                self.game.powers_manager.increase_bullet_count(player)
            else:
                weapon["weapon"] = pygame.image.load(WEAPONS[weapon_name])
                weapon["current"] = weapon_name

    def update_projectiles(self):
        """Update position of projectiles and get rid of projectiles that went of screen."""
        if self.game.singleplayer:
            all_projectiles = [
                self.game.thunderbird_bullets,
                self.game.thunderbird_missiles,
            ]
        else:
            all_projectiles = [
                self.game.thunderbird_bullets,
                self.game.thunderbird_missiles,
                self.game.phoenix_bullets,
                self.game.phoenix_missiles,
            ]

        for projectiles in all_projectiles:
            projectiles.update()

            for projectile in projectiles.copy():
                if not self.screen.get_rect().colliderect(projectile.rect):
                    projectiles.remove(projectile)

    def reset_weapons(self):
        """Reset the weapon to its original value for each player."""
        for player, weapon_info in self.weapons.items():
            default_weapon = "thunderbolt" if player == "thunderbird" else "firebird"
            weapon_info["current"] = default_weapon
            weapon_info["weapon"] = pygame.image.load(WEAPONS[default_weapon])
