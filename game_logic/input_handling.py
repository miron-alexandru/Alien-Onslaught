"""This is a module that defines the PlayerInput class, which is responsible for
handling player input events in a game."""

import sys
import pygame
from entities.player_bullets import Firebird, Thunderbolt



class PlayerInput:
    """Class for handling player input events in a game."""
    def __init__(self, game, ui_options):
        self.game = game
        self.ui_options = ui_options
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

    def check_keydown_events(self, event, fire_bullet_method, reset_game,
                                        run_menu, singleplayer=False):
        """Respond to keys being pressed."""
        match event.key:
            # If the game is paused, check for Q, P, R, and M keys
            case pygame.K_q if self.ui_options.paused:
                pygame.quit()
                sys.exit()
            case pygame.K_p:
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_r if self.ui_options.paused:
                reset_game()
                self.ui_options.paused = not self.ui_options.paused
            case pygame.K_m if self.ui_options.paused:
                run_menu()

            # If the game is not paused, check for player keypresses
            case _ if not self.game.ui_options.paused:
                # Thunderbird controls
                if (self.thunderbird_ship.state.alive and
                    not self.thunderbird_ship.state.warping and
                    not self.thunderbird_ship.state.exploding):
                    match event.key:
                        case pygame.K_SPACE:
                            fire_bullet_method(
                                self.game.thunderbird_bullets,
                                self.game.settings.thunderbird_bullets_allowed,
                                bullet_class=Thunderbolt,
                                num_bullets=self.game.settings.thunderbird_bullet_count,
                                ship=self.thunderbird_ship)
                            self.game.settings.fire_sound.play()

                        case pygame.K_d:
                            self.thunderbird_ship.moving_flags['right'] = True
                        case pygame.K_a:
                            self.thunderbird_ship.moving_flags['left'] = True
                        case pygame.K_w:
                            self.thunderbird_ship.moving_flags['up'] = True
                        case pygame.K_s:
                            self.thunderbird_ship.moving_flags['down'] = True

                        case pygame.K_1:
                            self.thunderbird_ship.image = self.thunderbird_ship.anims.ship_images[0]
                        case pygame.K_2:
                            self.thunderbird_ship.image = self.thunderbird_ship.anims.ship_images[1]
                        case pygame.K_3:
                            self.thunderbird_ship.image = self.thunderbird_ship.anims.ship_images[2]


                # Phoenix controls
                if not singleplayer:
                    if (self.phoenix_ship.state.alive and
                    not self.phoenix_ship.state.warping and
                    not self.phoenix_ship.state.exploding):
                        match event.key:
                            case pygame.K_RETURN:
                                fire_bullet_method(
                                    self.game.phoenix_bullets,
                                    self.game.settings.phoenix_bullets_allowed,
                                    bullet_class=Firebird,
                                    num_bullets=self.game.settings.phoenix_bullet_count,
                                    ship=self.phoenix_ship)
                                self.game.settings.fire_sound.play()

                            case pygame.K_LEFT:
                                self.phoenix_ship.moving_flags['left'] = True
                            case pygame.K_RIGHT:
                                self.phoenix_ship.moving_flags['right'] = True
                            case pygame.K_UP:
                                self.phoenix_ship.moving_flags['up'] = True
                            case pygame.K_DOWN:
                                self.phoenix_ship.moving_flags['down'] = True
                            case pygame.K_KP1:
                                self.phoenix_ship.image = self.phoenix_ship.anims.ship_images[3]
                            case pygame.K_KP2:
                                self.phoenix_ship.image = self.phoenix_ship.anims.ship_images[4]
                            case pygame.K_KP3:
                                self.phoenix_ship.image = self.phoenix_ship.anims.ship_images[5]


    def check_keyup_events(self, event):
        """Respond to keys being released."""
        # Thunderbird controls
        if self.thunderbird_ship.state.alive:
            match event.key:
                # Thunderbird controls
                case pygame.K_d:
                    self.thunderbird_ship.moving_flags['right'] = False
                case pygame.K_a:
                    self.thunderbird_ship.moving_flags['left'] = False
                case pygame.K_w:
                    self.thunderbird_ship.moving_flags['up'] = False
                case pygame.K_s:
                    self.thunderbird_ship.moving_flags['down'] = False

            # Phoenix controls
        if self.phoenix_ship.state.alive:
            match event.key:
                case pygame.K_RIGHT:
                    self.phoenix_ship.moving_flags['right'] = False
                case pygame.K_LEFT:
                    self.phoenix_ship.moving_flags['left'] = False
                case pygame.K_UP:
                    self.phoenix_ship.moving_flags['up'] = False
                case pygame.K_DOWN:
                    self.phoenix_ship.moving_flags['down'] = False


    def reset_ship_movement_flags(self):
        """Stop movement of both Thunderbird and Phoenix ships."""
        self.thunderbird_ship.moving_flags['right'] = False
        self.thunderbird_ship.moving_flags['left'] = False
        self.thunderbird_ship.moving_flags['up'] = False
        self.thunderbird_ship.moving_flags['down'] = False
        self.phoenix_ship.moving_flags['right'] = False
        self.phoenix_ship.moving_flags['left'] = False
        self.phoenix_ship.moving_flags['up'] = False
        self.phoenix_ship.moving_flags['down'] = False
