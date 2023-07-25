"""
The weapons_manager module contains the WeaponsManager class that manages
the creation and behavior of player weapons available in the game.
"""

import time
import pygame

from src.utils.constants import WEAPONS
from src.utils.game_utils import play_sound, display_custom_message, load_single_image


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
        self.game_modes = self.settings.game_modes

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

    def set_weapon(self, player, weapon_name, loaded=False):
        """Change the player weapon."""
        if weapon := self.weapons.get(player):
            if (
                weapon_name == weapon["current"]
                and not self.game_modes.last_bullet
                and not loaded
            ):
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
                if self.game_modes.last_bullet:
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
            self.game.score_board.render_missiles_num(ship)

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
        if self.game_modes.last_bullet:
            self.draw_laser_message = True
            play_sound(self.sound_manager.game_sounds, "laser_not_ready")
            return

        if ship.aliens_killed >= self.settings.required_kill_count:
            new_laser = laser_class(self, ship)
            lasers.add(new_laser)
            ship.aliens_killed = 0
            ship.laser_ready = False
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

                if (
                    ship.laser_ready
                    and current_time - ship.laser_ready_start_time >= 1.5
                ):
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
            ship.laser_ready = False
            play_sound(self.sound_manager.game_sounds, "fire_laser")
        else:
            self.draw_laser_message = True
            play_sound(self.sound_manager.game_sounds, "laser_not_ready")

    def update_timed_laser_status(self):
        """Check the status of the timed laser."""
        current_time = time.time()
        for ship in self.game.ships:
            if ship.state.alive:
                time_since_last_ready = current_time - ship.last_laser_usage
                if time_since_last_ready >= self.settings.laser_cooldown:
                    if not ship.laser_ready:
                        ship.laser_ready = True
                        ship.laser_ready_start_time = current_time
                        play_sound(self.sound_manager.game_sounds, "laser_ready")

                    if (
                        ship.laser_ready
                        and current_time - ship.laser_ready_start_time >= 2
                    ):
                        ship.laser_ready = False
                        ship.last_laser_usage = current_time

    def check_laser_availability(self):
        """Check the laser availability for each ship and
        display a message if the laser is ready or not.
        """
        for ship in self.game.ships:
            if ship.laser_ready and ship.state.alive:
                if self.game_modes.cosmic_conflict:
                    display_custom_message(self.screen, "Ready!", ship, cosmic=True)
                else:
                    display_custom_message(self.screen, "Ready!", ship)

            if self.draw_laser_message and ship.laser_fired:
                if self.game_modes.last_bullet:
                    display_custom_message(self.screen, "Not available!", ship)
                elif self.game_modes.cosmic_conflict:
                    display_custom_message(self.screen, "Not Ready!", ship, cosmic=True)
                else:
                    display_custom_message(self.screen, "Not Ready!", ship)

        current_time = pygame.time.get_ticks()
        if self.draw_laser_message and current_time > self.display_time + 1500:
            self.draw_laser_message = False
            self.display_time = current_time

    def update_laser_status(self):
        """Update laser status for the one of the lasers, based
        on the game mode."""
        if any(
            mode in self.settings.game_modes.game_mode
            for mode in self.settings.timed_laser_modes
        ):
            self.update_timed_laser_status()
        elif not self.game_modes.last_bullet:
            self.update_normal_laser_status()
