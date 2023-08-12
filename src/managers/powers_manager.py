"""
The 'powers_managers' module contains the PowerEffectsManager class for managing the creation
and update of the power-ups and penalties in the game.
"""

import time
import random

from src.entities.powers import Power
from src.utils.constants import POWER_DOWN_ATTRIBUTES, PLAYER_HEALTH_ATTRS
from src.utils.game_utils import play_sound, display_custom_message


class PowerEffectsManager:
    """The PowerEffectsManager class manages the creation and,
    update of the power ups and penalties that appear in the game.
    """

    def __init__(self, game, score_board, stats):
        self.game = game
        self.screen = game.screen
        self.score_board = score_board
        self.stats = stats

        self.settings = game.settings
        self.thunderbird_ship = game.thunderbird_ship
        self.phoenix_ship = game.phoenix_ship
        self.thunderbird_bullets = game.thunderbird_bullets
        self.phoenix_bullets = game.phoenix_bullets

        self.last_power_up_time = 0
        self.power_down_time = 35

        self.power_names = {
            self.freeze_enemies: "Freeze",
            self.decrease_ship_speed: "Speed down",
            self.disarm_ship: "Disarmed",
            self.reverse_keys: "Reverse keys",
            self.decrease_bullet_size: "Smaller bullets",
            self.alien_upgrade: "Alien upgrade",
            self.increase_alien_numbers: "More aliens",
            self.increase_alien_hp: "Stronger aliens",
            self.increase_asteroid_freq: "More asteroids",
            self.bonus_points: "Bonus points",
            self.change_ship_size: "Size change",
            self.invincibility: "Invincibility",
            self.increase_ship_speed: "Speed up",
            self.increase_bullet_speed: "Faster bullets",
            self.increase_bullets_allowed: "More bullets",
            self.increase_bullet_count: "More bullets",
            self.increase_missiles_num: "More missiles",
            self.draw_ship_shield: "Ship shield",
            self.decrease_alien_speed: "Alien slowdown",
            self.decrease_alien_bullet_speed: "Slower alien bullets",
            self.increase_bullets_remaining: "More bullets remaining",
        }

        self.powerup_choices = self.get_powerup_choices()
        self.penalty_choices = self.get_penalty_choices()

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

    def update_power_choices(self):
        """Update the power choices."""
        self.powerup_choices = self.get_powerup_choices()
        self.penalty_choices = self.get_penalty_choices()

    def apply_powerup_or_penalty(self, player):
        """Powers up or applies a penalty on the specified player"""
        # Randomly select one of the powers and activate it.
        effect_choice = random.choice(self.powerup_choices + self.penalty_choices)
        self._check_power_name(effect_choice, player)
        effect_choice(player)
        self._play_power_sound(
            effect_choice, self.powerup_choices, self.penalty_choices
        )

    def _play_power_sound(self, effect_choice, powerup_choices, penalty_choices):
        """Play a sound effect based on the given effect choice,
        considering available power-ups and penalties.
        """
        if effect_choice in powerup_choices:
            if effect_choice.__name__ == self.freeze_enemies.__name__:
                play_sound(self.game.sound_manager.game_sounds, "freeze")
            else:
                play_sound(self.game.sound_manager.game_sounds, "power_up")
        elif effect_choice in penalty_choices:
            play_sound(self.game.sound_manager.game_sounds, "penalty")

    def update_powers(self):
        """Update powers and remove the ones that went off screen."""
        self.game.powers.update()
        for power in self.game.powers.copy():
            if power.rect.y > self.settings.screen_height:
                self.game.powers.remove(power)

    def _check_power_name(self, effect_choice, player):
        """Check what power was picked up and set the power name
        accordingly and set the display_power flag to True."""
        ship = self.thunderbird_ship if player == "thunderbird" else self.phoenix_ship
        ship.power_name = self.power_names.get(effect_choice, "Unknown Power!")
        ship.display_power = True

    def display_powers_effect(self):
        """Display what power was picked up by the player."""
        current_time = time.time()
        for ship in self.game.ships:
            if ship.display_power and not ship.state.exploding:
                self.display_power_message(ship, current_time)
            else:
                ship.power_time = current_time

    def display_power_message(self, ship, current_time):
        """Display the name of the power that the ship picked up."""
        if self.settings.game_modes.cosmic_conflict:
            display_custom_message(
                self.screen, ship.power_name, ship, cosmic=True, powers=True
            )
        else:
            display_custom_message(self.screen, ship.power_name, ship, powers=True)

        if current_time > ship.power_time + 2:
            ship.display_power = False
            ship.power_time = 0

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
    def freeze_enemies(self, _=None):
        """Freeze all aliens that are on the screen for a period of time."""
        for alien in self.game.aliens:
            alien.freeze()

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
        self.score_board.render_missiles_num()

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
        getattr(self, f"{player}_ship").remaining_bullets += 1
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

        return self._filter_power_ups(power_ups)

    def _filter_power_ups(self, power_ups):
        game_modes = self.settings.game_modes
        filtered_power_ups = power_ups.copy()

        if game_modes.last_bullet:
            filtered_power_ups.append(self.increase_bullets_remaining)
            filtered_power_ups.remove(self.increase_bullet_count)
        elif game_modes.meteor_madness:
            filtered_power_ups = [
                self.increase_ship_speed,
                self.draw_ship_shield,
                self.bonus_points,
                self.invincibility,
                self.change_ship_size,
                self.increase_missiles_num,
            ]
        elif game_modes.cosmic_conflict:
            filtered_power_ups.remove(self.decrease_alien_speed)
            filtered_power_ups.remove(self.decrease_alien_bullet_speed)
            filtered_power_ups.remove(self.freeze_enemies)
            filtered_power_ups.remove(self.draw_ship_shield)

        return filtered_power_ups

    def get_penalty_choices(self):
        """Returns a list of penalty functions available in the game.
        Depending on the game mode, the list of penalties may differ.
        """
        penalties = [
            self.disarm_ship,
            self.reverse_keys,
            self.alien_upgrade,
            self.decrease_ship_speed,
            self.decrease_bullet_size,
        ]

        return self._filter_penalties(penalties)

    def _filter_penalties(self, penalties):
        """Filter the list of penalty functions based on the current game mode settings."""
        game_modes = self.settings.game_modes
        filtered_penalties = penalties.copy()

        if not (game_modes.last_bullet or game_modes.cosmic_conflict):
            filtered_penalties.extend(
                [self.increase_alien_numbers, self.increase_alien_hp]
            )

        if game_modes.meteor_madness:
            filtered_penalties = [
                self.reverse_keys,
                self.decrease_ship_speed,
                self.increase_asteroid_freq,
            ]

        if game_modes.cosmic_conflict:
            filtered_penalties.remove(self.alien_upgrade)

        return filtered_penalties
