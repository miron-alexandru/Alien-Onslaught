"""The powers module contains the class for creating instances of power-ups or penalties"""

import random
import pygame

from pygame.sprite import Sprite
from utils.constants import POWERS, GAME_CONSTANTS, WEAPON_BOXES



class Power(Sprite):
    """A class that manages the power ups or penalties for the game"""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load(POWERS['power'])
        self.speed = GAME_CONSTANTS['POWER_SPEED']
        self.last_power_time = 0
        self._initialize_position()

        self.health = False
        self.weapon = False
        self.weapon_name = None

    def _initialize_position(self):
        """Set the initial position of the power up."""
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0
        self.y_pos = float(self.rect.y)

    def make_health_power_up(self):
        """Makes health power up"""
        self.health = True
        self.image = pygame.image.load(POWERS['health'])

    def make_weapon_power_up(self):
        """Makes a random weapon power up."""
        self.weapon = True
        random_box = random.choice(list(WEAPON_BOXES.keys()))
        self.image = pygame.image.load(WEAPON_BOXES[random_box])
        self.weapon_name = random_box

    def update(self):
        """Update the power position."""
        self.y_pos += self.speed
        self.rect.y = self.y_pos

    def draw(self):
        """Draw the power."""
        self.screen.blit(self.image, self.rect)


class PowerEffectsManager:
    """The PowerEffectsManager class manages the creation and,
    update of the power ups and penalties that appear in the game."""
    def __init__(self, game, score_board, stats):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.thunderbird_ship = game.thunderbird_ship
        self.phoenix_ship = game.phoenix_ship
        self.score_board = score_board
        self.stats = stats

        self.last_power_up_time = 0
        self.last_power_down_time = 0


    def create_powers(self):
        """Create multiple power ups or penalties after a certain time has passed"""
        if self.last_power_up_time == 0:
            self.last_power_up_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        # change the range to determine how often power ups or penalties are created
        if current_time - self.last_power_up_time >= random.randint(25000, 45000): # miliseconds
            self.last_power_up_time = current_time
            # change the range to determine the chance for a power up to be health power up
            if random.randint(0, 4) == 0:
                power = Power(self)
                if random.randint(0, 1) == 0:
                    power.make_health_power_up()
                else:
                    power.make_weapon_power_up()
            else:
                power = Power(self)
            # create a power up or a penalty at a random location, at the top of the screen.
            power.rect.x = random.randint(0, self.settings.screen_width - power.rect.width)
            power.rect.y = random.randint(-100, -40)
            self.game.powers.add(power)

    def update_powers(self):
        """Update power-ups or penalties and remove the ones that went off screen."""
        self.game.powers.update()
        for power in self.game.powers.copy():
            if power.rect.y  > self.settings.screen_height:
                self.game.powers.remove(power)

    def alien_upgrade(self, _=None):
        """Gives an upgrade to the aliens."""
        aliens = self.game.aliens.sprites()
        if len(aliens) >= 12:
            selected_aliens = random.sample(aliens, 12)
        else:
            selected_aliens = random.choices(aliens, k=len(aliens))
        for alien in selected_aliens:
            alien.upgrade()


    def reverse_keys(self, player):
        """Trigger the reverse key state on the specified player."""
        getattr(self, f"{player}_ship").reverse_keys()

    def disarm_ship(self, player):
        """Trigger the disarm state on the specified player."""
        getattr(self, f"{player}_ship").disarm()

    def bonus_points(self, player):
        """Increases the points for the specified player"""
        setattr(self.stats, f"{player}_score",
                getattr(self.stats, f"{player}_score") + 550)
        self.score_board.render_scores()
        self.score_board.update_high_score()

    def invincibility(self, player):
        """Trigger the invincibility state on the specified player"""
        getattr(self, f"{player}_ship").set_immune()

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

    def manage_power_downs(self):
        """Set the power down states of the ship to False after a period of time."""
        for ship in self.game.ships:
            if ship.state.reverse or ship.state.disarmed:
                power_down_time = 10000
                current_time = pygame.time.get_ticks()
                if current_time > self.last_power_down_time + power_down_time:
                    self.last_power_down_time = current_time
                    if ship.state.reverse:
                        ship.state.reverse = False
                    if ship.state.disarmed:
                        ship.state.disarmed = False
