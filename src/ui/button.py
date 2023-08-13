"""
The 'button' module provides the Button class used to create UI buttons.
"""

import pygame

from src.utils.game_utils import display_description


class Button:
    """A class that represents a button on the screen."""

    def __init__(
        self, game, image_loc, pos, description="", center=False, menu_button=False
    ):
        """Initialize button attributes."""
        self.screen = game.screen
        self.description = description
        self.image = pygame.image.load(image_loc)
        self.screen_rect = self.screen.get_rect()

        self.visible = False

        # Build the button's rect object and set its position.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        if center:
            self.rect.center = self.screen_rect.center
            self.rect.y -= 115
        elif menu_button:
            self.rect.center = self.screen_rect.center
            self.rect.y -= 80
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
        """Draws the button."""
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
