"""
The 'powers' module contains classes for managing the creation
and update of the power-ups and penalties in the game.

Classes:
    - 'Power': A class that manages the powers created in the game.
    - 'PowerEffectsManager': A class that manages creation and update
    for both powers and penalties in the game.
"""

import time
import random

from pygame.sprite import Sprite
from utils.constants import (
    POWERS,
    GAME_CONSTANTS,
    WEAPON_BOXES,
    POWER_DOWN_ATTRIBUTES,
    PLAYER_HEALTH_ATTRS,
)
from utils.game_utils import load_single_image, play_sound


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
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
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
        self.thunderbird_bullets = game.thunderbird_bullets
        self.phoenix_bullets = game.phoenix_bullets
        self.score_board = score_board
        self.stats = stats

        self.last_power_up_time = 0
        self.power_down_time = 35

    def create_powers(self):
        """Creates power-ups or penalties at random intervals and locations."""
        if self.last_power_up_time == 0:
            self.last_power_up_time = time.time()

        current_time = time.time()
        time_elapsed = current_time - self.last_power_up_time

        if time_elapsed >= random.randint(15, 20):
            self.last_power_up_time = current_time
            self.create_power_up_or_penalty()

    def create_power_up_or_penalty(self):
        """Creates a power-up or penalty at a random location."""
        if random.randint(0, 4) == 0:
            power = Power(self)
            if random.randint(0, 1) == 0:
                power.make_health_power_up()
            else:
                power.make_weapon_power_up()
        else:
            power = Power(self)

        power.rect.x = random.randint(0, self.settings.screen_width - power.rect.width)
        power.rect.y = random.randint(-100, -40)
        self.game.powers.add(power)

    def apply_powerup_or_penalty(self, player):
        """Powers up or applies a penalty on the specified player"""
        powerup_choices = self.get_powerup_choices()
        penalty_choices = self.get_penalty_choices()
        # randomly select one of the powers and activate it.
        effect_choice = random.choice(powerup_choices + penalty_choices)
        effect_choice(player)

        # Play sound effect
        if effect_choice in powerup_choices:
            if effect_choice.__name__ == self.freeze_enemies.__name__:
                play_sound(self.game.sound_manager.game_sounds, "freeze")
            else:
                play_sound(self.game.sound_manager.game_sounds, "power_up")
        elif effect_choice in penalty_choices:
            play_sound(self.game.sound_manager.game_sounds, "penalty")

    def health_power_up(self, player):
        """Increase the player's health by one."""
        health_attr = PLAYER_HEALTH_ATTRS.get(player)
        if health_attr is not None:
            current_hp = getattr(self.stats, health_attr)
            if current_hp < self.stats.max_hp:
                setattr(self.stats, health_attr, current_hp + 1)
            self.score_board.create_health()
            play_sound(self.game.sound_manager.game_sounds, "health")

    def weapon_power_up(self, player, weapon_name):
        """Changes the given player's weapon."""
        self.game.weapons_manager.set_weapon(player, weapon_name)
        play_sound(self.game.sound_manager.game_sounds, "weapon")

    def freeze_enemies(self, _=None):
        """Freeze all aliens that are on the screen for a period of time."""
        for alien in self.game.aliens:
            alien.freeze()

    def update_powers(self):
        """Update powers and remove the ones that went off screen."""
        self.game.powers.update()
        for power in self.game.powers.copy():
            if power.rect.y > self.settings.screen_height:
                self.game.powers.remove(power)

    # Penalties
    def decrease_ship_speed(self, player):
        """Decreases the ship speed of the specified player."""
        setattr(
            self.settings,
            f"{player}_ship_speed",
            getattr(self.settings, f"{player}_ship_speed") - 0.4,
        )

    def reverse_keys(self, player):
        """Trigger the reverse key state on the specified player."""
        ship = getattr(self, f"{player}_ship")
        ship.state.reverse = True
        ship.last_reverse_power_down_time = time.time()

    def decrease_bullet_size(self, player):
        """Trigger the scaled_weapon state on the specified player."""
        ship = getattr(self, f"{player}_ship")
        ship.state.scaled_weapon = True
        ship.last_scaled_weapon_power_down_time = time.time()

    def disarm_ship(self, player):
        """Trigger the disarm state on the specified player."""
        ship = getattr(self, f"{player}_ship")
        ship.state.disarmed = True
        ship.last_disarmed_power_down_time = time.time()

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
        ship = getattr(self, f"{player}_ship")
        if ship.scale_counter < 2:
            ship.scale_counter += 1
            ship.scale_ship(0.5)

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
        current_time = time.time() - (self.game.pause_time / 1000)

        for ship in self.game.ships:
            for attribute, last_power_down_time_attr in POWER_DOWN_ATTRIBUTES.items():
                last_power_down_time = getattr(ship, last_power_down_time_attr)
                if getattr(ship.state, attribute) and current_time > (
                    last_power_down_time + self.power_down_time
                ):
                    setattr(ship.state, attribute, False)
                    setattr(ship, last_power_down_time_attr, None)
                    self.game.pause_time = 0

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
            self.freeze_enemies,
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
            self.decrease_bullet_size,
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
