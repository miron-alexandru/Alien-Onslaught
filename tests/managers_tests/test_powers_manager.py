"""
This module tests the PowerEffectsManager class that is used for
creating powers in the game.
"""
import time
import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.managers.powers_manager import PowerEffectsManager
from src.game_logic.game_settings import Settings


class TestPowerEffectsManager(unittest.TestCase):
    """Test cases for the PowerEffectsManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.score_board = MagicMock()
        self.stats = MagicMock()
        self.sound_manager = MagicMock()
        self.settings = Settings()
        self.game.settings = self.settings
        self.power_effects_manager = PowerEffectsManager(
            self.game, self.score_board, self.stats
        )
        self.power_effects_manager.settings = self.settings
        self.game.sound_manager = self.sound_manager

    def test_init(self):
        """Test the initialization of the manager."""
        self.assertEqual(self.power_effects_manager.screen, self.game.screen)
        self.assertEqual(self.power_effects_manager.settings, self.game.settings)
        self.assertEqual(
            self.power_effects_manager.thunderbird_ship, self.game.thunderbird_ship
        )
        self.assertEqual(
            self.power_effects_manager.phoenix_ship, self.game.phoenix_ship
        )
        self.assertEqual(
            self.power_effects_manager.phoenix_bullets, self.game.phoenix_bullets
        )
        self.assertEqual(
            self.power_effects_manager.thunderbird_bullets,
            self.game.thunderbird_bullets,
        )
        self.assertIsNotNone(self.power_effects_manager.stats)
        self.assertIsNotNone(self.power_effects_manager.score_board)
        self.assertEqual(self.power_effects_manager.last_power_up_time, 0)
        self.assertEqual(self.power_effects_manager.power_down_time, 35)
        self.assertIsInstance(self.power_effects_manager.power_names, dict)

    @patch("src.managers.powers_manager.time")
    @patch("src.managers.powers_manager.random")
    def test_create_powers(self, mock_random, mock_time):
        """Test the creation of the powers."""
        mock_time.time.side_effect = [1, 16]
        mock_random.randint.return_value = 15

        self.power_effects_manager.create_power_up_or_penalty = MagicMock()

        self.power_effects_manager.create_powers()

        self.assertEqual(self.power_effects_manager.last_power_up_time, 16)
        self.power_effects_manager.create_power_up_or_penalty.assert_called_once()

    def test_update_powers(self):
        """Test the update of the powers."""
        power1 = MagicMock()
        power2 = MagicMock()
        power1.rect.y = 50
        power2.rect.y = 2000

        self.game.powers.copy.return_value = [power1, power2]

        self.power_effects_manager.update_powers()

        self.game.powers.remove.assert_called_once_with(power2)

    @patch("src.managers.powers_manager.random")
    def test_create_power_up_or_penalty(self, mock_random):
        """Test the creation of powers."""
        self.power_effects_manager.create_power_up_or_penalty()

        self.game.powers.add.assert_called_once()

        # Mock random to create a health or weapon power up
        mock_random.randint.side_effect = [0, 0, -10, -50]

        self.power_effects_manager.create_power_up_or_penalty()
        self.assertEqual(self.game.powers.add.call_count, 2)

    @patch("src.managers.powers_manager.play_sound")
    def test_weapon_power_up(self, mock_play_sound):
        """Test the weapon power up."""
        self.power_effects_manager.weapon_power_up("phoenix", "fire_bullet")

        self.game.weapons_manager.set_weapon.assert_called_once_with(
            "phoenix", "fire_bullet"
        )

        # Check if the appropriate sound effect was played
        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "weapon"
        )

    def test_freeze_enemies(self):
        """Test the freeze enemies power up."""
        # Create a list of mock aliens
        mock_aliens = [MagicMock(), MagicMock(), MagicMock()]
        self.game.aliens = mock_aliens

        self.power_effects_manager.freeze_enemies()

        # Assert that the freeze method was called on each alien
        for alien in mock_aliens:
            alien.freeze.assert_called_once()

    @patch("src.managers.powers_manager.play_sound")
    def test_health_power_up(self, mock_play_sound):
        """Test the health power-up."""
        player = "thunderbird"

        self.stats.thunderbird_hp = 4
        self.stats.max_hp = 5

        self.power_effects_manager.health_power_up(player)

        self.assertEqual(self.stats.thunderbird_hp, 5)
        self.power_effects_manager.score_board.create_health.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "health"
        )

        self.power_effects_manager.score_board.create_health.reset_mock()
        mock_play_sound.reset_mock()

        # Test if the hp remains the same when it reached the max value.
        self.power_effects_manager.health_power_up(player)
        self.assertEqual(self.stats.thunderbird_hp, 5)

        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "health"
        )
        self.power_effects_manager.score_board.create_health.assert_called_once()

    @patch("src.managers.powers_manager.play_sound")
    def test_apply_powerup_or_penalty_freeze(self, mock_play_sound):
        """Test the apply power up or penalty for the freeze enemies power up."""
        self.power_effects_manager.check_power = MagicMock()
        player = "thunderbird"

        mock_freeze_enemies = MagicMock(name="freeze_enemies")
        mock_freeze_enemies.__name__ = "freeze_enemies"
        self.power_effects_manager.freeze_enemies = mock_freeze_enemies

        with patch("random.choice") as mock_choice:
            mock_choice.return_value = self.power_effects_manager.freeze_enemies
            self.power_effects_manager.apply_powerup_or_penalty(player)

        mock_freeze_enemies.assert_called_once_with(player)
        self.power_effects_manager.check_power.assert_called_once_with(
            mock_choice.return_value, player
        )
        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "freeze"
        )

    @patch("src.managers.powers_manager.play_sound")
    def test_apply_powerup_or_penalty_normal(self, mock_play_sound):
        """Test the apply power up or penalty for the other power ups."""
        self.power_effects_manager.check_power = MagicMock()
        player = "thunderbird"

        mock_increase_ship_speed = MagicMock(name="increase_ship_speed")
        mock_increase_ship_speed.__name__ = "increase_ship_speed"
        self.power_effects_manager.increase_ship_speed = mock_increase_ship_speed

        with patch("random.choice") as mock_choice:
            mock_choice.return_value = self.power_effects_manager.increase_ship_speed
            self.power_effects_manager.apply_powerup_or_penalty(player)

        mock_increase_ship_speed.assert_called_once_with(player)
        self.power_effects_manager.check_power.assert_called_once_with(
            mock_choice.return_value, player
        )
        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "power_up"
        )

    @patch("src.managers.powers_manager.play_sound")
    def test_apply_powerup_or_penalty_penalties(self, mock_play_sound):
        """Test the apply power up or penalty for the penalties."""
        self.power_effects_manager.check_power = MagicMock()
        player = "thunderbird"

        mock_disarm_ship = MagicMock(name="disarm_ship")
        self.power_effects_manager.disarm_ship = mock_disarm_ship

        with patch("random.choice") as mock_choice:
            mock_choice.return_value = self.power_effects_manager.disarm_ship
            self.power_effects_manager.apply_powerup_or_penalty(player)

        mock_disarm_ship.assert_called_once_with(player)
        self.power_effects_manager.check_power.assert_called_once_with(
            mock_choice.return_value, player
        )
        mock_play_sound.assert_called_once_with(
            self.sound_manager.game_sounds, "penalty"
        )

    def test_check_power(self):
        """Test the check_power_method."""
        player = "thunderbird"
        effect_choice = self.power_effects_manager.freeze_enemies

        self.power_effects_manager.check_power(effect_choice, player)

        self.assertEqual(self.game.thunderbird_ship.power_name, "Freeze")
        self.assertTrue(self.game.thunderbird_ship.display_power)

        effect_choice = MagicMock()

        self.power_effects_manager.check_power(effect_choice, player)

        self.assertEqual(self.game.thunderbird_ship.power_name, "Unknown Power!")
        self.assertTrue(self.game.thunderbird_ship.display_power)

    @patch("src.managers.powers_manager.display_custom_message")
    @patch("src.managers.powers_manager.time.time")
    def test_display_powers_effect_cosmic_conflict(
        self, mock_time, mock_display_message
    ):
        """Test the display_powers_effect in the Cosmic Conflict
        game mode.
        """
        self.settings.game_modes.cosmic_conflict = True
        mock_time.return_value = 5

        ship1 = MagicMock()
        ship1.display_power = True
        ship1.power_name = "Power 1"
        ship1.power_time = 0

        ship2 = MagicMock()
        ship2.display_power = False
        ship2.power_time = 0

        self.game.ships = [ship1, ship2]

        self.power_effects_manager.display_powers_effect()

        mock_display_message.assert_called_once_with(
            self.game.screen, "Power 1", ship1, cosmic=True, powers=True
        )
        self.assertFalse(ship1.display_power)
        self.assertEqual(ship1.power_time, 0)

    @patch("src.managers.powers_manager.display_custom_message")
    @patch("src.managers.powers_manager.time.time")
    def test_display_powers_effect_regular_mode(self, mock_time, mock_display_message):
        """Test the display_powers_effect in the other game modes."""
        self.settings.game_modes.cosmic_conflict = False
        mock_time.return_value = 5

        ship1 = MagicMock()
        ship1.display_power = True
        ship1.power_name = "Power 1"
        ship1.power_time = 0

        ship2 = MagicMock()
        ship2.display_power = True
        ship2.power_name = "Power 2"
        ship2.power_time = 0
        self.game.ships = [ship1, ship2]

        self.power_effects_manager.display_powers_effect()

        expected_calls = [
            call(self.game.screen, "Power 1", ship1, powers=True),
            call(self.game.screen, "Power 2", ship2, powers=True),
        ]

        self.assertEqual(mock_display_message.call_args_list, expected_calls)
        self.assertFalse(ship1.display_power)
        self.assertEqual(ship1.power_time, 0)

        self.assertFalse(ship2.display_power)
        self.assertEqual(ship2.power_time, 0)

    @patch("src.managers.powers_manager.display_custom_message")
    def test_display_powers_effect_not_displayed(self, mock_display_message):
        """Test the display_powers_effect when the power effect
        is not displayed.
        """
        ship = MagicMock()
        ship.display_power = False
        ship.power_time = 0
        self.game.ships = [ship]

        self.power_effects_manager.display_powers_effect()

        mock_display_message.assert_not_called()
        self.assertFalse(ship.display_power)

    def test_manage_power_downs(self):
        """Test the manage power downs method when the power
        are turned off."""
        self.game.pause_time = 5

        # Create ships with power down states and last power down times
        ship = MagicMock()
        ship.state.reverse = True
        ship.state.disarmed = True
        ship.state.scaled_weapon = True

        ship.last_reverse_power_down_time = 0
        ship.last_disarmed_power_down_time = 0
        ship.last_scaled_weapon_power_down_time = 0

        self.game.ships = [ship]

        self.power_effects_manager.manage_power_downs()

        # Assert that ship1's power down state is still True since it hasn't been 10 seconds yet
        self.assertFalse(ship.state.reverse)
        self.assertFalse(ship.state.disarmed)
        self.assertFalse(ship.state.scaled_weapon)
        self.assertEqual(ship.last_reverse_power_down_time, None)
        self.assertEqual(ship.last_disarmed_power_down_time, None)
        self.assertEqual(ship.last_scaled_weapon_power_down_time, None)

        self.assertEqual(self.game.pause_time, 0)

    def test_manage_power_downs_still_active(self):
        """Test the manage power downs method when the power down
        is still active."""

        self.game.pause_time = 0

        # Create ships with power down states and last power down times
        ship = MagicMock()
        ship.state.reverse = True
        ship.state.disarmed = True
        ship.state.scaled_weapon = True

        ship.last_reverse_power_down_time = time.time() - 5
        ship.last_disarmed_power_down_time = time.time() - 5
        ship.last_scaled_weapon_power_down_time = time.time() - 5

        self.game.ships = [ship]

        # Mock the time to the current time
        current_time = time.time() - (self.game.pause_time / 1000)
        with patch("time.time", return_value=current_time):
            self.power_effects_manager.manage_power_downs()

        # Assert that ship1's power down state is still True since it hasn't been 10 seconds yet
        self.assertTrue(ship.state.reverse)
        self.assertTrue(ship.state.disarmed)
        self.assertTrue(ship.state.scaled_weapon)
        self.assertEqual(ship.last_reverse_power_down_time, current_time - 5)
        self.assertEqual(ship.last_disarmed_power_down_time, current_time - 5)
        self.assertEqual(ship.last_scaled_weapon_power_down_time, current_time - 5)

        self.assertEqual(self.game.pause_time, 0)

    def test_decrease_ship_speed(self):
        """Test the decrease ship speed penalty."""
        player = "thunderbird"
        self.power_effects_manager.settings.thunderbird_ship_speed = 2.0

        self.power_effects_manager.decrease_ship_speed(player)

        self.assertEqual(
            self.power_effects_manager.settings.thunderbird_ship_speed, 1.6
        )

    def test_reverse_keys(self):
        """Test the reverse keys penalty."""
        player = "thunderbird"
        ship = MagicMock()
        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship
        ship.state.reverse = False

        self.power_effects_manager.reverse_keys(player)

        self.assertTrue(ship.state.reverse)
        self.assertIsNotNone(ship.last_reverse_power_down_time)

    def test_decrease_bullet_size(self):
        """Test the decrease bullet size penalty."""
        player = "thunderbird"
        ship = MagicMock()
        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship
        ship.state.scaled_weapon = False

        self.power_effects_manager.decrease_bullet_size(player)

        self.assertTrue(ship.state.scaled_weapon)
        self.assertIsNotNone(ship.last_scaled_weapon_power_down_time)

    def test_disarm_ship(self):
        """Test the disarm ship penalty."""
        player = "thunderbird"
        ship = MagicMock()
        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship
        ship.state.disarmed = False

        self.power_effects_manager.disarm_ship(player)

        self.assertTrue(ship.state.disarmed)
        self.assertIsNotNone(ship.last_disarmed_power_down_time)

    def test_alien_upgrade(self):
        """Test the alien upgrade penalty."""
        aliens = [MagicMock() for _ in range(12)]
        self.game.aliens.sprites = MagicMock(return_value=aliens)

        self.power_effects_manager.alien_upgrade()

        self.assertTrue(self.game.aliens.sprites.called)
        self.assertEqual(len(aliens), 12)
        for alien in aliens:
            self.assertTrue(alien.upgrade.called)

    def test_increase_alien_numbers(self):
        """Test the increase alien numbers penalty."""
        self.power_effects_manager.increase_alien_numbers()

        self.assertTrue(self.game.aliens_manager.create_fleet.called_with(1))

    def test_increase_alien_hp(self):
        """Test the increase alien hp penalty."""
        alien1 = MagicMock()
        alien2 = MagicMock()
        alien1.hit_count = alien2.hit_count = 2
        self.game.aliens = [alien1, alien2]

        self.power_effects_manager.increase_alien_hp()

        self.assertEqual(alien1.hit_count, 1)
        self.assertEqual(alien2.hit_count, 1)

    def test_increase_asteroid_freq(self):
        """Test the increase asteroid freq penalty."""
        self.power_effects_manager.settings.asteroid_freq = 200

        self.power_effects_manager.increase_asteroid_freq()

        self.assertEqual(self.power_effects_manager.settings.asteroid_freq, 300)

    def test_bonus_points(self):
        """Test the bonus points power up."""
        player = "thunderbird"
        self.stats.thunderbird_score = 1000

        self.power_effects_manager.bonus_points(player)

        self.assertEqual(self.stats.thunderbird_score, 1550)
        self.score_board.render_scores.assert_called_once()
        self.score_board.update_high_score.assert_called_once()

    def test_change_ship_size(self):
        """Test the change ship size power up."""
        player = "thunderbird"
        ship = MagicMock()
        ship.scale_counter = 0
        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship

        self.power_effects_manager.change_ship_size(player)

        self.assertTrue(ship.scale_ship.called)
        self.assertIsNotNone(ship.last_scaled_power_down_time)

    def test_increase_ship_speed(self):
        """Test the increase ship speed power up."""
        player1 = "thunderbird"
        player2 = "phoenix"

        initial_thunder_speed = self.settings.thunderbird_ship_speed
        initial_phoenix_speed = self.settings.phoenix_ship_speed

        self.power_effects_manager.increase_ship_speed(player1)
        self.power_effects_manager.increase_ship_speed(player2)

        self.assertEqual(
            self.settings.thunderbird_ship_speed, initial_thunder_speed + 0.3
        )
        self.assertEqual(self.settings.phoenix_ship_speed, initial_phoenix_speed + 0.3)

    def test_increase_bullet_speed(self):
        """Test the increase bullet speed power up."""
        player1 = "thunderbird"
        player2 = "phoenix"

        initial_thunder_speed = self.settings.thunderbird_bullet_speed
        initial_phoenix_speed = self.settings.phoenix_bullet_speed

        self.power_effects_manager.increase_bullet_speed(player1)
        self.power_effects_manager.increase_bullet_speed(player2)

        self.assertEqual(
            self.settings.thunderbird_bullet_speed, initial_thunder_speed + 0.3
        )
        self.assertEqual(
            self.settings.phoenix_bullet_speed, initial_phoenix_speed + 0.3
        )

    def test_invincibility(self):
        """Test for the invincibility power up."""
        player = "thunderbird"
        ship = MagicMock()

        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship

        self.power_effects_manager.invincibility(player)

        self.assertTrue(ship.set_immune.called)

    def test_increase_bullets_allowed(self):
        """Test for the increase bullets allower power up."""
        player1 = "thunderbird"
        player2 = "phoenix"

        initial_thunder_bullets = self.settings.thunderbird_bullets_allowed
        initial_phoenix_bullets = self.settings.phoenix_bullets_allowed

        self.power_effects_manager.increase_bullets_allowed(player1)
        self.power_effects_manager.increase_bullets_allowed(player2)

        self.assertEqual(
            self.settings.thunderbird_bullets_allowed, initial_thunder_bullets + 2
        )
        self.assertEqual(
            self.settings.phoenix_bullets_allowed, initial_phoenix_bullets + 2
        )

    def test_increase_bullet_count(self):
        """Test for the increase bullet count power up."""
        player1 = "thunderbird"
        player2 = "phoenix"

        initial_thunder_bullets = self.settings.thunderbird_bullet_count
        initial_phoenix_bullets = self.settings.phoenix_bullet_count

        self.power_effects_manager.increase_bullet_count(player1)
        self.power_effects_manager.increase_bullet_count(player2)

        self.assertEqual(
            self.settings.thunderbird_bullet_count, initial_thunder_bullets + 1
        )
        self.assertEqual(
            self.settings.phoenix_bullet_count, initial_phoenix_bullets + 1
        )

    def test_increase_missiles_num(self):
        """Test the increase missiles num power up."""
        player = "thunderbird"
        self.power_effects_manager.thunderbird_ship.missiles_num = 3
        initial_missiles = self.power_effects_manager.thunderbird_ship.missiles_num

        self.power_effects_manager.increase_missiles_num(player)

        self.assertEqual(
            self.power_effects_manager.thunderbird_ship.missiles_num,
            initial_missiles + 1,
        )
        self.score_board.render_missiles_num.assert_called_once()

    def test_draw_ship_shield(self):
        """Test for the draw shiled power up."""
        player = "thunderbird"
        ship = MagicMock()

        self.power_effects_manager.thunderbird_ship = ship
        self.power_effects_manager.phoenix_ship = ship

        self.power_effects_manager.draw_ship_shield(player)

        self.assertTrue(ship.draw_shield.called)

    def test_decrease_alien_speed(self):
        """Test the decrease alien speed power up."""
        player = "thunderbird"
        initial_speed = self.settings.alien_speed

        self.power_effects_manager.decrease_alien_speed(player)

        self.assertEqual(self.settings.alien_speed, initial_speed - 0.1)

        self.settings.alien_speed = 0

        self.power_effects_manager.decrease_alien_speed(player)

        self.assertEqual(self.settings.alien_speed, 0)

    def test_decrease_alien_bullet_speed(self):
        """Test the decrease alien bullet speed power up."""
        player = "thunderbird"
        initial_speed = self.settings.alien_bullet_speed

        self.power_effects_manager.decrease_alien_bullet_speed(player)

        self.assertEqual(self.settings.alien_bullet_speed, initial_speed - 0.1)

        self.settings.alien_bullet_speed = 0

        self.power_effects_manager.decrease_alien_bullet_speed(player)

        self.assertEqual(self.settings.alien_bullet_speed, 0)

    def test_increase_remaining_bullets(self):
        """Test the increase remaining bullets power up."""
        player = "thunderbird"
        self.power_effects_manager.thunderbird_ship.remaining_bullets = 9
        initial_bullets = self.power_effects_manager.thunderbird_ship.remaining_bullets

        self.power_effects_manager.increase_bullets_remaining(player)

        self.assertEqual(
            self.power_effects_manager.thunderbird_ship.remaining_bullets,
            initial_bullets + 1,
        )

        self.score_board.render_bullets_num.assert_called_once()

    def test_get_powerup_choices_normal(self):
        """Test the get power up choices method."""
        choices = self.power_effects_manager.get_powerup_choices()

        self.assertEqual(len(choices), 12)
        self.assertIn(self.power_effects_manager.increase_ship_speed, choices)
        self.assertIn(self.power_effects_manager.draw_ship_shield, choices)
        self.assertIn(self.power_effects_manager.freeze_enemies, choices)

    def test_get_powerup_choices_game_modes(self):
        """Test the get powerup choices method in game modes."""
        self.settings.game_modes.last_bullet = True
        choices = self.power_effects_manager.get_powerup_choices()

        self.assertEqual(len(choices), 12)
        self.assertIn(self.power_effects_manager.increase_bullets_remaining, choices)
        self.assertNotIn(self.power_effects_manager.increase_bullet_count, choices)

        self.settings.game_modes.last_bullet = False
        self.settings.game_modes.meteor_madness = True

        choices = self.power_effects_manager.get_powerup_choices()
        self.assertEqual(len(choices), 6)
        self.assertIn(self.power_effects_manager.bonus_points, choices)
        self.assertIn(self.power_effects_manager.increase_missiles_num, choices)
        self.assertIn(self.power_effects_manager.increase_ship_speed, choices)

    def test_get_penalty_choices(self):
        """Test the get penalty choices method."""
        choices = self.power_effects_manager.get_penalty_choices()

        self.assertEqual(len(choices), 7)
        self.assertIn(self.power_effects_manager.decrease_ship_speed, choices)
        self.assertIn(self.power_effects_manager.reverse_keys, choices)
        self.assertIn(self.power_effects_manager.disarm_ship, choices)

        self.settings.game_modes.meteor_madness = True
        choices = self.power_effects_manager.get_penalty_choices()
        self.assertEqual(len(choices), 3)
        self.assertIn(self.power_effects_manager.reverse_keys, choices)
        self.assertIn(self.power_effects_manager.decrease_ship_speed, choices)
        self.assertIn(self.power_effects_manager.increase_asteroid_freq, choices)

        self.settings.game_modes.meteor_madness = False
        self.settings.game_modes.last_bullet = True
        choices = self.power_effects_manager.get_penalty_choices()
        self.assertEqual(len(choices), 5)
        self.assertNotIn(self.power_effects_manager.increase_alien_numbers, choices)
        self.assertNotIn(self.power_effects_manager.increase_alien_hp, choices)


if __name__ == "__main__":
    unittest.main()
