"""The 'powers' module contains the Power class used to create power instances."""

import random

from pygame.sprite import Sprite
from src.utils.constants import POWERS, GAME_CONSTANTS, WEAPON_BOXES
from src.utils.game_utils import load_single_image


class Power(Sprite):
    """The 'Power' class represents the power ups and penalties in the game.
    It loads an image for each type of power up, sets its speed, and
    initializes its position randomly. It also provides methods for creating
    health or weapon power ups, and for updating and drawing the power on screen.
    """

    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image = load_single_image(POWERS["power"])
        self.health_image = load_single_image(POWERS["health"])
        self.speed = GAME_CONSTANTS["POWER_SPEED"]
        self.last_power_time = 0
        self._initialize_position()

        self.health = False
        self.weapon = False
        self.weapon_name = None

    def _initialize_position(self):
        """Set the initial position of the power."""
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            0, self.game.settings.screen_width - self.rect.width
        )
        self.rect.y = 0
        self.y_pos = float(self.rect.y)

    def make_health_power_up(self):
        """Change the power up to a health power up."""
        self.health = True
        self.image = self.health_image

    def make_weapon_power_up(self):
        """Change the power up to a random weapon power up."""
        self.weapon = True
        random_box = random.choice(list(WEAPON_BOXES.keys()))
        self.image = load_single_image(WEAPON_BOXES[random_box])
        self.weapon_name = random_box

    def update(self):
        """Update the position of the power on the screen."""
        self.y_pos += self.speed
        self.rect.y = int(self.y_pos)

    def draw(self):
        """Draw the power on the screen."""
        self.game.screen.blit(self.image, self.rect)
