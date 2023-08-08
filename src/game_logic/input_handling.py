"""
The "input_handling" module defines the PlayerInput class, which is responsible for
handling player input events in the game.
"""

import sys
import pygame

from src.entities.projectiles.missile import Missile
from src.entities.projectiles.laser import Laser
from src.entities.projectiles.player_bullets import Firebird, Thunderbolt
from src.utils.game_utils import play_sound, play_music


class PlayerInput:
    """Class for handling player input events in a game."""

    def __init__(self, game, ui_options):
        self.game = game
        self.settings = game.settings
        self.ui_options = ui_options
        self.thunderbird = self.game.thunderbird_ship
        self.phoenix = self.game.phoenix_ship

    def check_keydown_events(
        self,
        event,
        reset_game,
        run_menu,
        game_menu,
        fire_missile_method,
        fire_laser_method,
    ):
        """Respond to keys being pressed."""
        match event.key:
            # If the game is paused, check for Q, P, R, ESC and M keys
            case pygame.K_q if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "quit_effect")
                pygame.time.delay(800)
                pygame.quit()
                sys.exit()
            case pygame.K_p:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_r if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                self.game.sound_manager.current_sound = None
                reset_game()
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_ESCAPE if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                play_music(self.game.sound_manager.menu_music, "menu")
                self.game.sound_manager.current_sound = "menu"
                game_menu()
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_m if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                pygame.time.delay(300)
                self.game.stats.game_active = False
                run_menu()
            case pygame.K_s if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                self.game.save_load_manager.get_current_game_stats()
                self.game.save_load_manager.handle_save_load_menu(save=True)
                self.ui_options.paused = not self.ui_options.paused

            # If the game is not paused, check for player keypresses
            case _ if not self.ui_options.paused:
                self._handle_thunderbird_controls(
                    event, fire_missile_method, fire_laser_method
                )

                # Phoenix controls
                if not self.game.singleplayer:
                    self._handle_phoenix_controls(
                        event, fire_missile_method, fire_laser_method
                    )

    def check_keyup_events(self, event):
        """Respond to keys being released."""
        # Thunderbird controls
        if self.thunderbird.state.alive:
            match event.key:
                # Thunderbird controls
                case pygame.K_d:
                    self.thunderbird.moving_flags["right"] = False
                case pygame.K_a:
                    self.thunderbird.moving_flags["left"] = False
                case pygame.K_w:
                    self.thunderbird.moving_flags["up"] = False
                case pygame.K_s:
                    self.thunderbird.moving_flags["down"] = False
                case pygame.K_SPACE:
                    self.thunderbird.state.firing = False
                case pygame.K_c:
                    self.thunderbird.laser_fired = False

        # Phoenix controls
        if not self.game.singleplayer and self.phoenix.state.alive:
            match event.key:
                case pygame.K_RIGHT:
                    self.phoenix.moving_flags["right"] = False
                case pygame.K_LEFT:
                    self.phoenix.moving_flags["left"] = False
                case pygame.K_UP:
                    self.phoenix.moving_flags["up"] = False
                case pygame.K_DOWN:
                    self.phoenix.moving_flags["down"] = False
                case pygame.K_RETURN:
                    self.phoenix.state.firing = False
                case pygame.K_RSHIFT:
                    self.phoenix.laser_fired = False

    def handle_ship_firing(self, fire_bullet_method):
        """Handles the ship firing."""
        current_time = pygame.time.get_ticks()
        ships = {
            "thunderbird": (
                self.thunderbird,
                self.game.thunderbird_bullets,
                self.game.settings.thunderbird_bullets_allowed,
                Thunderbolt,
                self.game.settings.thunderbird_bullet_count,
            ),
            "phoenix": (
                self.phoenix,
                self.game.phoenix_bullets,
                self.game.settings.phoenix_bullets_allowed,
                Firebird,
                self.game.settings.phoenix_bullet_count,
            ),
        }

        for ship_data in ships.values():
            ship, bullets, bullets_allowed, bullet_class, bullet_count = ship_data
            if ship.state.firing and current_time - ship.last_bullet_time > 200:
                fire_bullet_method(
                    bullets,
                    bullets_allowed,
                    bullet_class=bullet_class,
                    num_bullets=bullet_count,
                    ship=ship,
                )
                ship.last_bullet_time = current_time

    def _handle_thunderbird_controls(
        self, event, fire_missile_method, fire_laser_method
    ):
        """Handle Thunderbird controls."""
        if (
            not self.thunderbird.state.alive
            or self.thunderbird.state.warping
            or self.thunderbird.state.exploding
        ):
            return
        match event.key:
            case pygame.K_SPACE:
                self.thunderbird.state.firing = True
            case pygame.K_d:
                self.thunderbird.moving_flags["right"] = True
            case pygame.K_a:
                self.thunderbird.moving_flags["left"] = True
            case pygame.K_w:
                self.thunderbird.moving_flags["up"] = True
            case pygame.K_s:
                self.thunderbird.moving_flags["down"] = True
            case pygame.K_x:
                fire_missile_method(
                    self.game.thunderbird_missiles,
                    self.thunderbird,
                    missile_class=Missile,
                )
            case pygame.K_c:
                fire_laser_method(
                    self.game.thunderbird_laser, self.thunderbird, laser_class=Laser
                )
                self.thunderbird.laser_fired = True

    def _handle_phoenix_controls(self, event, fire_missile_method, fire_laser_method):
        """Handle Phoenix controls."""
        if (
            not self.phoenix.state.alive
            or self.phoenix.state.warping
            or self.phoenix.state.exploding
        ):
            return
        match event.key:
            case pygame.K_RETURN:
                self.phoenix.state.firing = True
            case pygame.K_LEFT:
                self.phoenix.moving_flags["left"] = True
            case pygame.K_RIGHT:
                self.phoenix.moving_flags["right"] = True
            case pygame.K_UP:
                self.phoenix.moving_flags["up"] = True
            case pygame.K_DOWN:
                self.phoenix.moving_flags["down"] = True
            case pygame.K_RCTRL:
                fire_missile_method(
                    self.game.phoenix_missiles, self.phoenix, missile_class=Missile
                )
            case pygame.K_RSHIFT:
                fire_laser_method(
                    self.game.phoenix_laser, self.phoenix, laser_class=Laser
                )
                self.phoenix.laser_fired = True

    def reset_ship_flags(self):
        """Reset movement flags and firing state for the ships."""
        self.thunderbird.moving_flags["right"] = False
        self.thunderbird.moving_flags["left"] = False
        self.thunderbird.moving_flags["up"] = False
        self.thunderbird.moving_flags["down"] = False
        self.phoenix.moving_flags["right"] = False
        self.phoenix.moving_flags["left"] = False
        self.phoenix.moving_flags["up"] = False
        self.phoenix.moving_flags["down"] = False
        self.phoenix.state.firing = False
        self.thunderbird.state.firing = False
