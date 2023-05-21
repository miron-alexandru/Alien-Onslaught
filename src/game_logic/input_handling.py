"""
This is a module that defines the PlayerInput class, which is responsible for
handling player input events in a game.
"""

import sys
import pygame
from entities.projectiles import Missile, Firebird, Thunderbolt
from utils.game_utils import play_sound


class PlayerInput:
    """Class for handling player input events in a game."""

    def __init__(self, game, ui_options):
        self.game = game
        self.settings = game.settings
        self.ui_options = ui_options
        self.thunderbird = self.game.thunderbird_ship
        self.phoenix = self.game.phoenix_ship

    def check_keydown_events(
        self, event, reset_game, run_menu, game_menu, fire_missile_method
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
                reset_game()
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_ESCAPE if self.ui_options.paused:
                pygame.mixer.stop()
                self.game.sound_manager.load_sounds("menu_sounds")
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                play_sound(self.game.sound_manager.menu_sounds, "menu", loop=True)
                self.game.sound_manager.current_sound = "menu"
                game_menu()
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_m if self.ui_options.paused:
                play_sound(self.game.sound_manager.game_sounds, "keypress")
                pygame.time.delay(300)
                self.game.stats.game_active = False
                run_menu()

            # If the game is not paused, check for player keypresses
            case _ if not self.ui_options.paused:
                self.handle_thunderbird_controls(event, fire_missile_method)

                # Phoenix controls
                if not self.game.singleplayer:
                    self._handle_phoenix_controls(event, fire_missile_method)

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

    def handle_thunderbird_controls(self, event, fire_missile_method):
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
            case pygame.K_1:
                self.thunderbird.image = self.thunderbird.anims.ship_images[0]
                if self.settings.game_modes.cosmic_conflict:
                    self.thunderbird.image = pygame.transform.rotate(
                        self.thunderbird.image, -90
                    )
            case pygame.K_2:
                self.thunderbird.image = self.thunderbird.anims.ship_images[1]
                if self.settings.game_modes.cosmic_conflict:
                    self.thunderbird.image = pygame.transform.rotate(
                        self.thunderbird.image, -90
                    )
            case pygame.K_3:
                self.thunderbird.image = self.thunderbird.anims.ship_images[2]
                if self.settings.game_modes.cosmic_conflict:
                    self.thunderbird.image = pygame.transform.rotate(
                        self.thunderbird.image, -90
                    )
            case pygame.K_z:
                fire_missile_method(
                    self.game.thunderbird_missiles,
                    self.thunderbird,
                    missile_class=Missile,
                )

    def _handle_phoenix_controls(self, event, fire_missile_method):
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
            case pygame.K_KP1:
                self.phoenix.image = self.phoenix.anims.ship_images[3]
                if self.settings.game_modes.cosmic_conflict:
                    self.phoenix.image = pygame.transform.rotate(self.phoenix.image, 90)
            case pygame.K_KP2:
                self.phoenix.image = self.phoenix.anims.ship_images[4]
                if self.settings.game_modes.cosmic_conflict:
                    self.phoenix.image = pygame.transform.rotate(self.phoenix.image, 90)
            case pygame.K_KP3:
                self.phoenix.image = self.phoenix.anims.ship_images[5]
                if self.settings.game_modes.cosmic_conflict:
                    self.phoenix.image = pygame.transform.rotate(self.phoenix.image, 90)
            case pygame.K_RCTRL:
                fire_missile_method(
                    self.game.phoenix_missiles, self.phoenix, missile_class=Missile
                )

    def reset_ship_movement_flags(self):
        """Reset movement flags for the ships."""
        self.thunderbird.moving_flags["right"] = False
        self.thunderbird.moving_flags["left"] = False
        self.thunderbird.moving_flags["up"] = False
        self.thunderbird.moving_flags["down"] = False
        self.phoenix.moving_flags["right"] = False
        self.phoenix.moving_flags["left"] = False
        self.phoenix.moving_flags["up"] = False
        self.phoenix.moving_flags["down"] = False
