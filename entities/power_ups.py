"""The power_ups module contains the class for creating instances of power-ups."""

import random
import pygame

from pygame.sprite import Sprite
from utils.constants import POWER_UPS, GAME_CONSTANTS



class PowerUp(Sprite):
    """A class that manages the power ups for the game"""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load(POWER_UPS['power_up'])
        self.speed = GAME_CONSTANTS['POWER_UP_SPEED']
        self.last_power_up_time = 0
        self._initialize_position()
        self.health = False

    def _initialize_position(self):
        """Set the initial position of the power up."""
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0
        self.y_pos = float(self.rect.y)

    def make_health_power_up(self):
        """Makes health power up"""
        self.health = True
        self.image = pygame.image.load(POWER_UPS['health'])

    def update(self):
        """Update the power-up position."""
        self.y_pos += self.speed
        self.rect.y = self.y_pos

    def draw_powerup(self):
        """Draw the power-up."""
        self.screen.blit(self.image, self.rect)


class PowerUpsManager:
    """The PowerUpsManager class manages the creation and,
    update of the power ups that appear in the game."""
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.last_power_up_time = 0

    def create_power_ups(self):
        """Create multiple power ups after a certain time has passed"""
        if self.last_power_up_time == 0:
            self.last_power_up_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        # change the range to determine how often power ups are created
        if current_time - self.last_power_up_time >= random.randint(25000, 45000): # miliseconds
            self.last_power_up_time = current_time
            # change the range to determine the chance for a power up to be health power up
            if random.randint(0, 4) == 0:
                power_up = PowerUp(self)
                power_up.make_health_power_up()
            else:
                power_up = PowerUp(self)
            # create power up at a random location, at the top of the screen.
            power_up.rect.x = random.randint(0, self.settings.screen_width - power_up.rect.width)
            power_up.rect.y = random.randint(-100, -40)
            self.game.power_ups.add(power_up)

    def update_power_ups(self):
        """Update power-ups and remove power ups that went off screen."""
        self.game.power_ups.update()
        for power in self.game.power_ups.copy():
            if power.rect.y  > self.settings.screen_height:
                self.game.power_ups.remove(power)
