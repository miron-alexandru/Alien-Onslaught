"""
The 'button module provides a class `Button` that creates a button in the game.
"""

import pygame

from src.utils.game_utils import display_description


class Button:
    """A class that represents a button on the screen."""

    def __init__(self, game, image_loc, pos, description="", center=False):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        # variable used for buttons that toggle visibility
        self.visible = False
        self.description = description

        # Load button image and scale it to the desired size.
        self.image = pygame.image.load(image_loc)

        # Build the button's rect object and set its position.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        if center:
            self.rect.center = self.screen_rect.center
            self.rect.y -= 50
        else:
            self.rect.x, self.rect.y = pos

    def update_pos(self, *args, x=0, y=0):
        """Update the button's position."""
        if len(args) == 1:
            self.rect.center = args[0]
        elif len(args) == 2:
            self.rect.topleft = args
        self.rect.move_ip(x, y)

    def draw_button(self):
        """Draws the button if it's visible."""
        self.screen.blit(self.image, self.rect)

    def show_button_info(self):
        """Display the information about the button on the screen.
        This method is mainly used for displaying
        the description for the game modes.
        """
        screen_width, screen_height = self.screen.get_size()
        display_description(
            self.screen,
            self.description,
            screen_width // 2 + 74,
            screen_height // 2 + 180,
        )
