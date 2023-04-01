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

    def draw(self):
        """Draw the power-up."""
        self.screen.blit(self.image, self.rect)


class PowerUpsManager:
    """The PowerUpsManager class manages the creation and,
    update of the power ups that appear in the game."""
    def __init__(self, game, score_board):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.thunderbird_ship = game.thunderbird_ship
        self.phoenix_ship = game.phoenix_ship
        self.score_board = score_board
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


    def increase_ship_speed(self, player):
        """Increases the ship speed of the specified player"""
        setattr(self.settings, f"{player}_ship_speed",
                getattr(self.settings, f"{player}_ship_speed") + 0.3)

    def increase_bullet_speed(self, player):
        """Increases the bullet speed of the specified player"""
        setattr(self.settings, f"{player}_bullet_speed",
                getattr(self.settings, f"{player}_bullet_speed") + 0.3)

    def increase_bullets_allowed(self, player):
        """Increases the bullets allowed for the specified player"""
        setattr(self.settings, f"{player}_bullets_allowed",
                getattr(self.settings, f"{player}_bullets_allowed") + 2)

    def increase_bullet_count(self, player):
        """Increases the bullet number of the specified player"""
        setattr(self.settings, f"{player}_bullet_count",
                getattr(self.settings, f"{player}_bullet_count") + 1)

    def increase_missiles_num(self, player):
        """Increases the number of missiles for the specified player."""
        getattr(self, f"{player}_ship").missiles_num += 1

    def draw_ship_shield(self, player):
        """Activates the shield on the specified player"""
        getattr(self, f"{player}_ship").draw_shield()

    def decrease_alien_speed(self, _=None):
        """Decreases alien speed."""
        if self.settings.alien_speed > 0:
            setattr(self.settings, "alien_speed", getattr(self.settings, "alien_speed") - 0.1)
        else:
            return None

    def decrease_alien_bullet_speed(self, _=None):
        """Decreases alien bullet speed."""
        if self.settings.alien_bullet_speed > 1:
            setattr(self.settings, "alien_bullet_speed",
                getattr(self.settings, "alien_bullet_speed") - 0.1)
        else:
            return None

    def increase_bullets_remaining(self, player):
        """Power up special for the Last Bullet game mode, it increases
        the remaining bullets number by one."""
        players = {
            "thunderbird": self.thunderbird_ship,
            "phoenix": self.phoenix_ship
        }
        players[player].remaining_bullets += 1
        self.score_board.render_bullets_num()
