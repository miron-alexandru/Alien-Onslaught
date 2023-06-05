"""
The 'projectiles' module contains classes for managing different projectiles
available in the game.

Classes:
    - 'Thunderbolt': A class that manages bullets for the Thunderbird ship.
    - 'Firebird': A class that manages bullets for the Phoenix ship.
    - 'Missile': A class that manages missles that the players have in the game.
    - 'Laser': A class that manager the laser weapon for the players.
    - 'WeaponsManager': A class that manages player weapons.
"""

import time
import pygame
from pygame.sprite import Sprite
from utils.animation_constants import missile_frames, laser_frames
from utils.constants import WEAPONS
from utils.game_utils import load_single_image, play_sound, display_laser_message
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
            self.rect.x = int(self.x_pos)
        else:
            self.y_pos -= self.speed
            self.rect.y = int(self.y_pos)

    def draw(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

    def scale_bullet(self, scale):
        """Scale the bullet image and rect."""
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
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



class WeaponsManager:
    """The WeaponManager class manages player weapons."""

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.game_modes = self.settings.game_modes
        self.screen = game.screen
        self.sound_manager = game.sound_manager
        self.draw_laser_message = False
        self.display_time = 0
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

        self.weapons = {
            "thunderbird": {
                "weapon": load_single_image(WEAPONS["thunderbolt"]),
                "current": "thunderbolt",
            },
            "phoenix": {
                "weapon": load_single_image(WEAPONS["firebird"]),
                "current": "firebird",
            },
        }
        self.singleplayer_projectiles = [
            self.game.thunderbird_bullets,
            self.game.thunderbird_missiles,
            self.game.thunderbird_laser,
        ]

        self.multiplayer_projectiles = [
            self.game.thunderbird_bullets,
            self.game.thunderbird_missiles,
            self.game.thunderbird_laser,
            self.game.phoenix_bullets,
            self.game.phoenix_missiles,
            self.game.phoenix_laser,
        ]

    def set_weapon(self, player, weapon_name):
        """Change the player weapon."""
        if weapon := self.weapons.get(player):
            if weapon_name == weapon["current"] and not self.game_modes.last_bullet:
                self.game.powers_manager.increase_bullet_count(player)
            else:
                weapon["weapon"] = load_single_image(WEAPONS[weapon_name])
                weapon["current"] = weapon_name

    def reset_weapons(self):
        """Reset the weapon to its original value for each player."""
        for player, weapon_info in self.weapons.items():
            default_weapon = "thunderbolt" if player == "thunderbird" else "firebird"
            weapon_info["current"] = default_weapon
            weapon_info["weapon"] = load_single_image(WEAPONS[default_weapon])

    def update_projectiles(self):
        """Update position of projectiles and get rid of projectiles that went of screen."""
        if self.game.singleplayer:
            all_projectiles = self.singleplayer_projectiles
        else:
            all_projectiles = self.multiplayer_projectiles

        for projectiles in all_projectiles:
            projectiles.update()

            for projectile in projectiles.copy():
                if not self.screen.get_rect().colliderect(projectile.rect):
                    projectiles.remove(projectile)

    def fire_bullet(self, bullets, bullets_allowed, bullet_class, num_bullets, ship):
        """Create new player bullets."""
        # Create the bullets at and position them correctly as the number of bullets increases
        if ship.remaining_bullets <= 0 or ship.state.disarmed:
            return

        bullet_fired = False
        if len(bullets) < bullets_allowed:
            new_bullets = [
                bullet_class(self, ship, scaled=True)
                if ship.state.scaled_weapon
                else bullet_class(self, ship)
                for _ in range(num_bullets)
            ]
            bullets.add(new_bullets)
            for i, new_bullet in enumerate(new_bullets):
                offset = 30 * (i - (num_bullets - 1) / 2)
                new_bullet.rect.centerx = ship.rect.centerx + offset
                new_bullet.rect.centery = ship.rect.centery + offset
                if self.settings.game_modes.last_bullet:
                    ship.remaining_bullets -= 1
                    self.game.score_board.render_bullets_num()
                bullet_fired = True

        if bullet_fired:
            play_sound(self.sound_manager.game_sounds, "bullet")

    def fire_missile(self, missiles, ship, missile_class):
        """Fire a missile from the given ship and update the missiles number."""
        if ship.missiles_num > 0:
            new_missile = missile_class(self, ship)
            play_sound(self.sound_manager.game_sounds, "missile_launch")
            missiles.add(new_missile)
            ship.missiles_num -= 1
            self.game.score_board.render_scores()

    def fire_laser(self, lasers, ship, laser_class):
        """Fire a laser from the ship."""
        if any(
            mode in self.settings.game_modes.game_mode
            for mode in self.settings.timed_laser_modes
        ):
            self._timed_laser(lasers, ship, laser_class)
        else:
            self._normal_laser(lasers, ship, laser_class)

    def _normal_laser(self, lasers, ship, laser_class):
        """Fire a laser from the ship based
        on the required kill count.
        """
        if ship.aliens_killed >= self.settings.required_kill_count:
            new_laser = laser_class(self, ship)
            lasers.add(new_laser)
            ship.aliens_killed = 0
            play_sound(self.sound_manager.game_sounds, "fire_laser")
        else:
            self.draw_laser_message = True
            play_sound(self.sound_manager.game_sounds, "laser_not_ready")

    def update_normal_laser_status(self):
        """Check the status of the normal laser."""
        current_time = time.time()

        for ship in self.game.ships:
            if ship.aliens_killed >= self.settings.required_kill_count:
                if not ship.laser_ready and not ship.laser_ready_msg:
                    ship.laser_ready = True
                    ship.laser_ready_msg = True
                    ship.laser_ready_start_time = current_time
                    play_sound(self.sound_manager.game_sounds, "laser_ready")

                if ship.laser_ready and current_time - ship.laser_ready_start_time >= 2:
                    ship.laser_ready = False
            else:
                ship.laser_ready_msg = False

    def _timed_laser(self, lasers, ship, laser_class):
        """Fire a laser from the ship based on a timed interval."""
        if (
            time.time() - (self.game.pause_time / 1000) - ship.last_laser_time
            >= self.settings.laser_cooldown
        ):
            new_laser = laser_class(self, ship)
            lasers.add(new_laser)
            ship.last_laser_time = time.time()
            self.game.pause_time = 0
            play_sound(self.sound_manager.game_sounds, "fire_laser")
        else:
            self.draw_laser_message = True
            play_sound(self.sound_manager.game_sounds, "laser_not_ready")

    def update_timed_laser_status(self):
        """Check the status of the timed laser."""
        if all(
            mode not in self.settings.game_modes.game_mode
            for mode in self.settings.timed_laser_modes
        ):
            return

        current_time = time.time()
        for ship in self.game.ships:
            time_since_last_ready = current_time - ship.last_laser_usage
            if time_since_last_ready >= self.settings.laser_cooldown:
                if not ship.laser_ready:
                    ship.laser_ready = True
                    ship.laser_ready_start_time = current_time
                    play_sound(self.sound_manager.game_sounds, "laser_ready")

                if ship.laser_ready and current_time - ship.laser_ready_start_time >= 2:
                    ship.laser_ready = False
                    ship.last_laser_usage = current_time

    def check_laser_availability(self):
        """Check the laser availability for each ship and
        display a message if the laser is ready or not.
        """
        for ship in self.game.ships:
            if ship.laser_ready:
                display_laser_message(self.screen, "Ready!", ship)

            if self.draw_laser_message and ship.laser_fired:
                display_laser_message(self.screen, "Not Ready!", ship)

        current_time = pygame.time.get_ticks()
        if self.draw_laser_message and current_time > self.display_time + 1500:
            self.draw_laser_message = False
            self.display_time = current_time
