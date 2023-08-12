"""
The 'player_health' module contains the Heart class, which is used
to display a heart image on the screen that represents the player HP.
"""

from pygame.sprite import Sprite
from src.utils.constants import OTHER
from src.utils.game_utils import load_single_image


class Heart(Sprite):
    """Draws a heart image on the screen that represents the player health."""

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.screen_rect = game.screen.get_rect()
        self.image = load_single_image(OTHER["heart"])
        self.rect = self.image.get_rect(topleft=(0, 0))

    def blitme(self):
        """Draw the heart image on screen."""
        self.screen.blit(self.image, self.rect)
