"""
The 'powers' module contains classes for managing the creation
and update of the power-ups and penalties in the game.

Classes:
    - 'Power': A class that manages the powers created in the game.
    - 'PowerEffectsManager': A class that manages creation and update
    for both powers and penalties in the game.
"""

import random
import pygame

from pygame.sprite import Sprite
from utils.constants import POWERS, GAME_CONSTANTS, WEAPON_BOXES


class Power(Sprite):
    """The 'Power' class manages the power ups and penalties in the game.
    It loads an image for each type of power up, sets its speed, and
    initializes its position randomly. It also provides methods for creating
    health or weapon power ups, and for updating and drawing the power on screen.
    """

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load(POWERS["power"])
        self.speed = GAME_CONSTANTS["POWER_SPEED"]
        self.last_power_time = 0
        self._initialize_position()

        self.health = False
        self.weapon = False
        self.weapon_name = None

    def _initialize_position(self):
        """Set the initial position of the power."""
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0
        self.y_pos = float(self.rect.y)

    def make_health_power_up(self):
        """Change the power up to a health power up."""
        self.health = True
        self.image = pygame.image.load(POWERS["health"])

    def make_weapon_power_up(self):
        """Change the power up to a random weapon power up."""
        self.weapon = True
        random_box = random.choice(list(WEAPON_BOXES.keys()))
        self.image = pygame.image.load(WEAPON_BOXES[random_box])
        self.weapon_name = random_box

    def update(self):
        """Update the position of the power on the screen."""
        self.y_pos += self.speed
        self.rect.y = self.y_pos

    def draw(self):
        """Draw the power on the screen."""
        self.screen.blit(self.image, self.rect)


class PowerEffectsManager:
    """The PowerEffectsManager class manages the creation and,
    update of the power ups and penalties that appear in the game.
    """

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
        """Creates power-ups or penalties at random intervals and locations."""
        if self.last_power_up_time == 0:
            self.last_power_up_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        # Determines how often powers and penalties are appearing.
        if current_time - self.last_power_up_time >= random.randint(
            10000, 20000
        ):  # milliseconds
            self.last_power_up_time = current_time
            # Determine the chance for a power to be health power up, weapon power up or
            # normal power
            if random.randint(0, 4) == 0:
                power = Power(self)
                if random.randint(0, 1) == 0:
                    power.make_health_power_up()
                else:
                    power.make_weapon_power_up()
            else:
                power = Power(self)
            # create a power up or a penalty at a random location, at the top of the screen.
            power.rect.x = random.randint(
                0, self.settings.screen_width - power.rect.width
            )
            power.rect.y = random.randint(-100, -40)
            self.game.powers.add(power)

    def update_powers(self):
        """Update powers and remove the ones that went off screen."""
        self.game.powers.update()
        for power in self.game.powers.copy():
            if power.rect.y > self.settings.screen_height:
                self.game.powers.remove(power)

    # Penalties
    def reverse_keys(self, player):
        """Trigger the reverse key state on the specified player."""
        getattr(self, f"{player}_ship").reverse_keys()

    def decrease_ship_speed(self, player):
        """Decreases the ship speed of the specified player."""
        setattr(
            self.settings,
            f"{player}_ship_speed",
            getattr(self.settings, f"{player}_ship_speed") - 0.4,
        )

    def disarm_ship(self, player):
        """Trigger the disarm state on the specified player."""
        getattr(self, f"{player}_ship").disarm()

    def alien_upgrade(self, _=None):
        """Select a random sample of aliens from the game's
        `aliens` sprite group and upgrade them.
        """
        aliens = self.game.aliens.sprites()
        if len(aliens) >= 12:
            selected_aliens = random.sample(aliens, 12)
        else:
            selected_aliens = random.choices(aliens, k=len(aliens))
        for alien in selected_aliens:
            alien.upgrade()

    def increase_alien_numbers(self, _=None):
        """Increases the number of aliens by creating one fleet."""
        self.game.aliens_manager.create_fleet(1)

    def increase_alien_hp(self, _=None):
        """Decreases the hit count of each alien, making them harder to destroy."""
        for alien in self.game.aliens:
            alien.hit_count -= 1

    def increase_asteroid_freq(self, _=None):
        """Increases asteroid frequency, used only in the Meteor Madness game mode."""
        self.settings.asteroid_freq += 100

    # Power Ups
    def bonus_points(self, player):
        """Increases the points for the specified player."""
        setattr(
            self.stats, f"{player}_score", getattr(self.stats, f"{player}_score") + 550
        )
        self.score_board.render_scores()
        self.score_board.update_high_score()

    def change_ship_size(self, player):
        """Make the specified player smaller (for a period of time)."""
        getattr(self, f"{player}_ship").scale_ship(0.5)

    def invincibility(self, player):
        """Trigger the invincibility state on the specified player."""
        getattr(self, f"{player}_ship").set_immune()

    def increase_ship_speed(self, player):
        """Increases the ship speed of the specified player."""
        setattr(
            self.settings,
            f"{player}_ship_speed",
            getattr(self.settings, f"{player}_ship_speed") + 0.3,
        )
        # for ship in self.game.ships:
        #   if isinstance(ship, type(self.game.thunderbird_ship)) and player == "thunderbird":
        #      ship.update_speed_from_settings("thunderbird")
        # elif isinstance(ship, type(self.game.phoenix_ship)) and player == "phoenix":
        #    ship.update_speed_from_settings("phoenix")

    def increase_bullet_speed(self, player):
        """Increases the bullet speed of the specified player."""
        setattr(
            self.settings,
            f"{player}_bullet_speed",
            getattr(self.settings, f"{player}_bullet_speed") + 0.3,
        )

    def increase_bullets_allowed(self, player):
        """Increases the bullets allowed for the specified player."""
        setattr(
            self.settings,
            f"{player}_bullets_allowed",
            getattr(self.settings, f"{player}_bullets_allowed") + 2,
        )

    def increase_bullet_count(self, player):
        """Increases the bullet number of the specified player."""
        setattr(
            self.settings,
            f"{player}_bullet_count",
            getattr(self.settings, f"{player}_bullet_count") + 1,
        )

    def increase_missiles_num(self, player):
        """Increases the number of missiles for the specified player."""
        getattr(self, f"{player}_ship").missiles_num += 1
        self.score_board.render_scores()

    def draw_ship_shield(self, player):
        """Activates the shield on the specified player."""
        getattr(self, f"{player}_ship").draw_shield()

    def decrease_alien_speed(self, _=None):
        """Decreases the speed of aliens."""
        if self.settings.alien_speed > 0:
            self.settings.alien_speed -= 0.1

    def decrease_alien_bullet_speed(self, _=None):
        """Decreases the speed of alien bullets."""
        if self.settings.alien_bullet_speed > 1:
            self.settings.alien_bullet_speed -= 0.1

    def increase_bullets_remaining(self, player):
        """Power up special for the Last Bullet game mode, it increases
        the remaining bullets number by one for the specified player."""
        players = {"thunderbird": self.thunderbird_ship, "phoenix": self.phoenix_ship}
        players[player].remaining_bullets += 1
        self.score_board.render_bullets_num()

    def manage_power_downs(self):
        """Set the power down states of the ship to False after a period of time."""
        for ship in self.game.ships:
            if ship.state.reverse or ship.state.disarmed:
                power_down_time = 15000
                current_time = pygame.time.get_ticks()
                if current_time > self.last_power_down_time + power_down_time:
                    self.last_power_down_time = current_time
                    if ship.state.reverse:
                        ship.state.reverse = False
                    if ship.state.disarmed:
                        ship.state.disarmed = False

    def get_powerup_choices(self):
        """Returns a list of power-up functions available in the game.
        Depending on the game mode, the list of power-ups may differ.
        """
        power_ups = [
            self.increase_ship_speed,
            self.increase_bullet_speed,
            self.increase_bullets_allowed,
            self.draw_ship_shield,
            self.decrease_alien_speed,
            self.decrease_alien_bullet_speed,
            self.bonus_points,
            self.invincibility,
            self.change_ship_size,
            self.increase_bullet_count,
            self.increase_missiles_num,
        ]

        if self.settings.game_modes.last_bullet:
            power_ups.append(self.increase_bullets_remaining)
            power_ups.remove(self.increase_bullet_count)
        elif self.settings.game_modes.meteor_madness:
            power_ups = [
                self.increase_ship_speed,
                self.draw_ship_shield,
                self.bonus_points,
                self.invincibility,
                self.change_ship_size,
                self.increase_missiles_num,
            ]

        return power_ups

    def get_penalty_choices(self):
        """Returns a list of penalties functions available in the game.
        Depending on the game mode, the list of penalties may differ.
        """
        penalties = [
            self.disarm_ship,
            self.reverse_keys,
            self.alien_upgrade,
            self.decrease_ship_speed,
        ]

        if not self.settings.game_modes.last_bullet:
            penalties += [self.increase_alien_numbers, self.increase_alien_hp]
        if self.settings.game_modes.meteor_madness:
            penalties = [
                self.reverse_keys,
                self.decrease_ship_speed,
                self.increase_asteroid_freq,
            ]

        return penalties