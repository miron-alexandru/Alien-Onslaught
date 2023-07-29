"""
The ship_selection module contains the ShipSelection class that implements the
ability to change the ship in the game.
"""

import pygame

from src.utils.constants import THUNDER_SHIP_DESCRIPTIONS, PHOENIX_SHIP_DESCRIPTIONS
from src.utils.game_utils import play_sound, display_description


class ShipSelection:
    """The ShipSelection class handles the ship selection in the game."""

    def __init__(self, game, screen, ship_images, settings):
        self.screen = screen
        self.settings = settings
        self.game = game
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship
        self.font = pygame.font.SysFont("verdana", 26)
        self.ship_images = ship_images
        self.clickable_regions = []

        self.ship_selection_functions = {
            (1, 0): (
                "regular_thunder",
                lambda: (
                    self.settings.regular_thunder_ship(),
                    setattr(self.thunderbird_ship, "starting_missiles", 3),
                ),
            ),
            (1, 1): (
                "slow_thunder",
                lambda: (
                    self.settings.slow_thunder(),
                    setattr(self.thunderbird_ship, "starting_missiles", 3),
                ),
            ),
            (1, 2): (
                "artillery_thunder",
                lambda: (
                    self.settings.heavy_artillery_thunder(),
                    setattr(self.thunderbird_ship, "starting_missiles", 6),
                ),
            ),
            (2, 0): (
                "regular_phoenix",
                lambda: (
                    self.settings.regular_phoenix_ship(),
                    setattr(self.phoenix_ship, "starting_missiles", 3),
                ),
            ),
            (2, 1): (
                "fast_phoenix",
                lambda: (
                    self.settings.fast_phoenix(),
                    setattr(self.phoenix_ship, "starting_missiles", 3),
                ),
            ),
            (2, 2): (
                "artillery_phoenix",
                lambda: (
                    self.settings.heavy_artillery_phoenix(),
                    setattr(self.phoenix_ship, "starting_missiles", 5),
                ),
            ),
        }

    def draw(self):
        """Draw the ship images and text on screen."""
        screen_width = self.screen.get_width()
        self.clickable_regions = []

        self.draw_ship_type_text(1, 25, screen_width * 0.05)
        self.draw_ships(1, 25, screen_width * 0.05)

        if not self.game.singleplayer:
            self.draw_ship_type_text(2, 25, screen_width * 0.3)
            self.draw_ships(2, 25, screen_width * 0.3)

    def draw_ship_type_text(self, ship_type, y_position, x_position):
        """Draw the ship type text on the screen."""
        ship_type_text = "Thunderbird" if ship_type == 1 else "Phoenix"
        ship_type_text_color = (255, 255, 255)
        text_surface = self.font.render(ship_type_text, True, ship_type_text_color)
        self.screen.blit(text_surface, (x_position, y_position))

    def draw_ships(self, ship_type, y_position, x_position):
        """Draws the ship images on the screen."""
        ship_images = self.ship_images[(ship_type - 1) * 3 : ship_type * 3]
        image_width = ship_images[0].get_width()

        for i, ship_image in enumerate(ship_images):
            x_pos = x_position + (i * (image_width + 20))
            ship_rect = ship_image.get_rect()
            ship_rect.topleft = (x_pos, y_position + 50)
            self.screen.blit(ship_image, ship_rect)
            self.clickable_regions.append((ship_rect, ship_type, i))

            if ship_rect.collidepoint(pygame.mouse.get_pos()):
                if ship_type == 1:
                    display_description(
                        self.screen, THUNDER_SHIP_DESCRIPTIONS[i], 55, 150
                    )
                else:
                    display_description(
                        self.screen, PHOENIX_SHIP_DESCRIPTIONS[i], 55, 150
                    )

    def handle_ship_selection(self, mouse_pos):
        """Handles the ship selection."""
        for region, ship_type, index in self.clickable_regions:
            if (
                region.collidepoint(mouse_pos)
                and self.game.ui_options.ship_selection
                and (ship_type, index) in self.ship_selection_functions
            ):
                ship_name, ship_function = self.ship_selection_functions[
                    (ship_type, index)
                ]
                if ship_type == 1:
                    self.thunderbird_ship.ship_name = ship_name
                    self.thunderbird_ship.ship_selected = True
                elif ship_type == 2:
                    self.phoenix_ship.ship_name = ship_name
                    self.phoenix_ship.ship_selected = True
                ship_function()
                play_sound(self.game.sound_manager.game_sounds, "select_ship")

        if self.game.singleplayer and self.thunderbird_ship.ship_selected:
            self.game.ui_options.ship_selection = False
        elif self.phoenix_ship.ship_selected and self.thunderbird_ship.ship_selected:
            self.game.ui_options.ship_selection = False
