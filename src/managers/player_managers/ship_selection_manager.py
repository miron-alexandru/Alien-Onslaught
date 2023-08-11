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
        self.game = game
        self.screen = screen
        self.ship_images = ship_images
        self.settings = settings

        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

        self.font = pygame.font.SysFont("verdana", 26)
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

        self.draw_ships_and_text(1, 25, screen_width * 0.05)

        if not self.game.singleplayer:
            self.draw_ships_and_text(2, 25, screen_width * 0.3)

    def draw_ships_and_text(self, ship_type, y_offset, x_position):
        """Draw ship type text and ships for a given player."""
        self.draw_ship_type_text(ship_type, y_offset, x_position)
        self.draw_ships(ship_type, y_offset, x_position)

    def draw_ship_type_text(self, ship_type, y_position, x_position):
        """Draw the ship type text on the screen."""
        ship_type_text = "Thunderbird" if ship_type == 1 else "Phoenix"
        text_surface = self.font.render(ship_type_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x_position, y_position))

    def draw_ships(self, ship_type, y_position, x_position):
        """Draws the ship images on the screen."""
        ship_images = self.get_ship_images(ship_type)
        image_width = ship_images[0].get_width()
        spacing = 15

        for i, ship_image in enumerate(ship_images):
            x_pos = x_position + (i * (image_width + spacing))
            ship_rect = self.position_ship(ship_image, x_pos, y_position + 50)
            self.register_clickable_region(ship_rect, ship_type, i)
            self.display_ship_description(ship_rect, ship_type, i)

    def get_ship_images(self, ship_type):
        """Get ship images based on the ship type."""
        start_index = (ship_type - 1) * 3
        end_index = ship_type * 3
        return self.ship_images[start_index:end_index]

    def position_ship(self, ship_image, x_pos, y_pos):
        """Position a ship image and return its rect."""
        ship_rect = ship_image.get_rect(topleft=(x_pos, y_pos))
        self.screen.blit(ship_image, ship_rect)
        return ship_rect

    def register_clickable_region(self, ship_rect, ship_type, index):
        """Register a clickable region for a ship."""
        self.clickable_regions.append((ship_rect, ship_type, index))

    def display_ship_description(self, ship_rect, ship_type, index):
        """Display ship description when hovered over."""
        descriptions = (
            THUNDER_SHIP_DESCRIPTIONS if ship_type == 1 else PHOENIX_SHIP_DESCRIPTIONS
        )
        if ship_rect.collidepoint(pygame.mouse.get_pos()):
            display_description(self.screen, descriptions[index], 60, 140)

    def handle_ship_selection(self, mouse_pos):
        """Handles the ship selection."""
        for region, ship_type, index in self.clickable_regions:
            if self.is_valid_ship_selection(region, ship_type, index, mouse_pos):
                self.select_ship(ship_type, index)
                play_sound(self.game.sound_manager.game_sounds, "select_ship")

        self.update_ship_selection_state()

    def is_valid_ship_selection(self, region, ship_type, index, mouse_pos):
        """Checks if the ship selection is valid."""
        return (
            region.collidepoint(mouse_pos)
            and self.game.ui_options.ship_selection
            and (ship_type, index) in self.ship_selection_functions
        )

    def select_ship(self, ship_type, index):
        """Selects the chosen ship and performs the associated function."""
        ship_name, ship_function = self.ship_selection_functions[(ship_type, index)]
        if selected_ship := self.get_selected_ship(ship_type):
            selected_ship.ship_name = ship_name
            selected_ship.ship_selected = True
        ship_function()

    def get_selected_ship(self, ship_type):
        """Returns the selected ship instance based on the ship type."""
        ship_mapping = {1: self.thunderbird_ship, 2: self.phoenix_ship}
        return ship_mapping.get(ship_type)

    def update_ship_selection_state(self):
        """Update ship selection state based on conditions."""
        if self.game.singleplayer and self.thunderbird_ship.ship_selected:
            self.game.ui_options.ship_selection = False
        elif self.phoenix_ship.ship_selected and self.thunderbird_ship.ship_selected:
            self.game.ui_options.ship_selection = False
