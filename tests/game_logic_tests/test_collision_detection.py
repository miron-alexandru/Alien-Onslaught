"""
This module tests the CollisionManager class which manages the
collisions in the game.
"""


import unittest
from unittest.mock import MagicMock, patch, call

import pygame

from src.game_logic.collision_detection import CollisionManager
from src.entities.projectiles.missile import Missile
from src.entities.alien_entities.aliens import BossAlien


class TestCollisionManager(unittest.TestCase):
    """Test cases for the CollisionManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.thunderbird_ship = MagicMock()
        self.phoenix_ship = MagicMock()
        self.game.thunderbird_ship = self.thunderbird_ship
        self.game.phoenix_ship = self.phoenix_ship
        self.game.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.collision_manager = CollisionManager(self.game)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.collision_manager.game, self.game)
        self.assertEqual(self.collision_manager.stats, self.game.stats)
        self.assertEqual(self.collision_manager.settings, self.game.settings)
        self.assertEqual(self.collision_manager.score_board, self.game.score_board)
        self.assertEqual(
            self.collision_manager.thunderbird_ship, self.game.thunderbird_ship
        )
        self.assertEqual(self.collision_manager.phoenix_ship, self.game.phoenix_ship)
        self.assertEqual(self.collision_manager.handled_collisions, {})

    @patch("src.game_logic.collision_detection.play_sound")
    def test_handle_shielded_ship_collisions(self, mock_play_sound):
        """Test the shield collisions with aliens."""
        ships = MagicMock()
        aliens = MagicMock()
        bullets = MagicMock()
        asteroids = MagicMock()

        self.collision_manager._handle_alien_collisions_with_shielded_ship = MagicMock()
        self.collision_manager._handle_bullet_collisions_with_shielded_ship = (
            MagicMock()
        )
        self.collision_manager._handle_asteroid_collisions_with_shielded_ship = (
            MagicMock()
        )

        self.collision_manager.handle_shielded_ship_collisions(
            [ships], [aliens], [bullets], [asteroids]
        )

        self.collision_manager._handle_alien_collisions_with_shielded_ship.assert_called_once_with(
            ships, [aliens]
        )
        self.collision_manager._handle_bullet_collisions_with_shielded_ship.assert_called_once_with(
            ships, [bullets]
        )
        self.collision_manager._handle_asteroid_collisions_with_shielded_ship.assert_called_once_with(
            ships, [asteroids]
        )

    def test_handle_alien_collisions_with_shielded_ship(self):
        """Test the shield collisions with aliens."""
        self.collision_manager._destroy_alien_and_play_sound = MagicMock()
        ship = MagicMock()
        aliens = MagicMock()

        self.collision_manager._handle_alien_collisions_with_shielded_ship(
            ship, [aliens]
        )

        self.collision_manager._destroy_alien_and_play_sound.assert_called_once_with(
            aliens
        )

    def test_handle_bullet_collisions_with_shielded_ship(self):
        """Test the shield collisions with bullets."""
        self.collision_manager._resolve_shield_collision = MagicMock()
        ship = MagicMock()
        bullets = MagicMock()

        self.collision_manager._handle_bullet_collisions_with_shielded_ship(
            ship, [bullets]
        )

        self.collision_manager._resolve_shield_collision.assert_called_once_with(
            bullets, "alien_exploding", ship
        )

    def test_handle_asteroids_collisions_with_shielded_ship(self):
        """Test the shield collisions with asteroids."""
        self.collision_manager._resolve_shield_collision = MagicMock()
        ship = MagicMock()
        asteroids = MagicMock()

        self.collision_manager._handle_asteroid_collisions_with_shielded_ship(
            ship, [asteroids]
        )

        self.collision_manager._resolve_shield_collision.assert_called_once_with(
            asteroids, "asteroid_exploding", ship
        )

    @patch("src.game_logic.collision_detection.play_sound")
    def test_destroy_alien_play_sound(self, mock_play_sound):
        """Test the destroy_alien_play_sound_method."""
        alien = MagicMock()

        self.collision_manager._destroy_alien_and_play_sound(alien)

        alien.kill.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "alien_exploding"
        )

    @patch("src.game_logic.collision_detection.play_sound")
    def test_resolve_shield_collision(self, mock_play_sound):
        """Test the resolve_shield_collision method."""
        entity = MagicMock()
        sound_key = "collision_sound"
        ship = MagicMock()
        ship.state.shielded = True

        self.collision_manager._resolve_shield_collision(entity, sound_key, ship)

        entity.kill.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, sound_key
        )
        self.assertFalse(ship.state.shielded)

    @patch("src.game_logic.collision_detection.play_sound")
    def test_check_asteroids_collisions_with_thunder_hit(self, mock_play_sound):
        """Test the asteroids collisions when the Thunderbird ship is hit."""
        asteroid = MagicMock()
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()
        self.game.asteroids = [asteroid]

        self.thunderbird_ship.state.alive = True
        self.thunderbird_ship.state.immune = False
        self.game.ships = [self.thunderbird_ship]

        self.collision_manager.check_asteroids_collisions(thunderbird_hit, phoenix_hit)

        thunderbird_hit.assert_called_once()
        asteroid.kill.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "asteroid_exploding"
        )

        phoenix_hit.assert_not_called()

    @patch("src.game_logic.collision_detection.play_sound")
    def test_check_asteroids_collisions_with_both_ships_hit(self, mock_play_sound):
        """Test the asteroids collisions when both ships are hit."""
        asteroid = MagicMock()
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()
        self.game.asteroids = [asteroid]

        self.thunderbird_ship.state.alive = True
        self.thunderbird_ship.state.immune = False
        self.phoenix_ship.state.alive = True
        self.phoenix_ship.state.immune = False

        self.collision_manager.check_asteroids_collisions(thunderbird_hit, phoenix_hit)

        thunderbird_hit.assert_called_once()
        phoenix_hit.assert_called_once()
        self.assertTrue(asteroid.kill.call_count, 2)
        self.assertTrue(mock_play_sound.call_count, 2)

    @patch("src.game_logic.collision_detection.play_sound")
    def test_check_asteroids_collisions_with_missiles_and_lasers(self, mock_play_sound):
        """Test the asteroids collisions with lasers and missiles."""
        # Mock objects
        thunder_missile = MagicMock(spec=Missile)
        thunder_missile.rect = MagicMock()
        thunder_laser = MagicMock(spec=pygame.sprite.Sprite)
        thunder_laser.rect = MagicMock()

        phoenix_missile = MagicMock(spec=Missile)
        phoenix_missile.rect = MagicMock()
        phoenix_laser = MagicMock(spec=pygame.sprite.Sprite)
        phoenix_laser.rect = MagicMock()

        asteroid = MagicMock()
        asteroid.rect = MagicMock()

        self.game.asteroids = [asteroid]
        self.game.thunderbird_missiles = [thunder_missile]
        self.game.phoenix_missiles = [phoenix_missile]
        self.game.thunderbird_laser = [thunder_laser]
        self.game.phoenix_laser = [phoenix_laser]

        self.collision_manager.check_asteroids_collisions(MagicMock(), MagicMock())

        # Assertions
        self.assertTrue(asteroid.kill.called)
        mock_play_sound.assert_called_with(
            self.game.sound_manager.game_sounds, "asteroid_exploding"
        )
        self.assertTrue(asteroid.kill.call_count, 4)
        self.assertTrue(mock_play_sound.call_count, 4)
        self.assertTrue(thunder_missile.explode.called)
        self.assertTrue(phoenix_missile.explode.called)

    def test_check_powers_collisions_with_power_method(self):
        """Test the power collisions when a normal power is picked up."""
        power = MagicMock()
        power.health = False
        power.weapon = False

        self.thunderbird_ship.state.alive = True
        self.phoenix_ship.state.alive = True

        self.game.powers = [power]

        power_method = MagicMock()
        health_power_method = MagicMock()
        weapon_power_method = MagicMock()

        self.collision_manager.check_powers_collisions(
            power_method, health_power_method, weapon_power_method
        )

        self.assertTrue(power.kill.call_count, 2)
        self.thunderbird_ship.empower.assert_called_once()
        self.phoenix_ship.empower.assert_called_once()

        expected_calls = [
            call("thunderbird"),
            call("phoenix"),
        ]

        self.assertEqual(power_method.call_args_list, expected_calls)

        health_power_method.assert_not_called()
        weapon_power_method.assert_not_called()

    def test_check_powers_collisions_with_health_power_method(self):
        """Test the powers collisions when a health power is picked up."""
        power = MagicMock()
        power.health = True
        power.weapon = False

        self.thunderbird_ship.state.alive = True
        self.phoenix_ship.state.alive = False
        self.phoenix_ship.power_name = ""
        self.phoenix_ship.display_power = False

        self.game.powers = [power]

        power_method = MagicMock()
        health_power_method = MagicMock()
        weapon_power_method = MagicMock()

        self.collision_manager.check_powers_collisions(
            power_method, health_power_method, weapon_power_method
        )

        self.assertTrue(power.kill.call_count, 2)
        self.thunderbird_ship.empower.assert_called_once()
        self.assertEqual(self.thunderbird_ship.power_name, "+1 HP")
        self.assertTrue(self.thunderbird_ship.display_power)
        self.assertEqual(health_power_method.call_count, 1)

        self.phoenix_ship.empower.assert_not_called()
        self.assertEqual(self.phoenix_ship.power_name, "")
        self.assertFalse(self.phoenix_ship.display_power)
        power_method.assert_not_called()
        weapon_power_method.assert_not_called()

    def test_check_powers_collisions_with_weapon_power_method(self):
        """Test the powers collisions when a weapon power is picked up."""
        power = MagicMock()
        power.health = False
        power.weapon = True

        self.thunderbird_ship.state.alive = True
        self.phoenix_ship.state.alive = True

        self.game.powers = [power]

        power_method = MagicMock()
        health_power_method = MagicMock()
        weapon_power_method = MagicMock()

        self.collision_manager.check_powers_collisions(
            power_method, health_power_method, weapon_power_method
        )

        self.assertTrue(power.kill.call_count, 2)
        self.thunderbird_ship.empower.assert_called_once()
        self.assertEqual(self.thunderbird_ship.power_name, "Weapon")
        self.assertTrue(self.thunderbird_ship.display_power)
        self.phoenix_ship.empower.assert_called_once()
        self.assertEqual(self.phoenix_ship.power_name, "Weapon")
        self.assertTrue(self.phoenix_ship.display_power)
        self.assertEqual(weapon_power_method.call_count, 2)

        power_method.assert_not_called()
        health_power_method.assert_not_called()

    def test_check_bullet_alien_collisions(self):
        """Test the check_bullet_alien_collisions method."""
        # Singleplayer test case
        self.game.singleplayer = True
        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()

        thunder_bullet = MagicMock(spec=pygame.sprite.Sprite)
        thunder_bullet.rect = MagicMock()

        phoenix_bullet = MagicMock(spec=pygame.sprite.Sprite)
        phoenix_bullet.rect = MagicMock()

        self.collision_manager._handle_alien_hits = MagicMock()
        self.game.aliens = [alien]

        self.game.thunderbird_bullets = pygame.sprite.Group(thunder_bullet)
        self.game.phoenix_bullets = pygame.sprite.Group(phoenix_bullet)

        self.collision_manager.check_bullet_alien_collisions()

        self.collision_manager._handle_alien_hits.assert_called_once()

        # Multiplayer test case
        self.collision_manager._handle_alien_hits.reset_mock()
        self.game.singleplayer = False

        self.collision_manager.check_bullet_alien_collisions()

        self.assertEqual(self.collision_manager._handle_alien_hits.call_count, 2)

    def test_update_cosmic_conflict_scores(self):
        """Test the update_cosmic_conflict_scores method."""
        # Thunderbird ship test case
        self.game.stats.phoenix_score = 0
        self.game.stats.thunderbird_score = 0
        ship = self.thunderbird_ship
        score_increment = 50

        hit_function = MagicMock()

        self.collision_manager._update_cosmic_conflict_scores(
            ship, hit_function, score_increment
        )

        self.assertEqual(self.game.stats.phoenix_score, score_increment)
        self.assertTrue(hit_function.called)
        self.assertTrue(self.game.score_board.render_scores.called)
        self.assertTrue(self.game.score_board.update_high_score.called)

        # Phoenix ship test case
        ship = self.phoenix_ship

        self.collision_manager._update_cosmic_conflict_scores(
            ship, hit_function, score_increment
        )

        self.assertEqual(self.game.stats.thunderbird_score, score_increment)
        self.assertTrue(hit_function.called)
        self.assertTrue(self.game.score_board.render_scores.called)
        self.assertTrue(self.game.score_board.update_high_score.called)

    @patch("src.game_logic.collision_detection.play_sound")
    @patch("src.game_logic.collision_detection.get_colliding_sprites")
    def test_resolve_collision_cosmic_conflict(self, mock_get_sprite, mock_play_sound):
        """Test the handle_collision method."""
        mock_get_sprite.return_value = [MagicMock(spec=Missile)]
        missile = mock_get_sprite.return_value[0]

        ship = self.thunderbird_ship
        ship.state.immune = False
        ship.state.shielded = False
        score_increment = 1000

        sprite_group = MagicMock()
        hit_function = MagicMock()
        self.collision_manager._update_cosmic_conflict_scores = MagicMock()

        self.collision_manager._resolve_collision_cosmic_conflict(
            ship, hit_function, sprite_group, score_increment
        )

        mock_get_sprite.assert_called_once_with(ship, sprite_group)
        missile.explode.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "missile"
        )
        self.collision_manager._update_cosmic_conflict_scores.assert_called_once_with(
            ship, hit_function, score_increment
        )

    def test_check_cosmic_conflict_collisions(self):
        """Test the check_cosmic_conflict collisions method."""
        self.collision_manager._resolve_collision_cosmic_conflict = MagicMock()
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()

        self.collision_manager.check_cosmic_conflict_collisions(
            thunderbird_hit, phoenix_hit
        )

        expected_calls = [
            call(self.phoenix_ship, phoenix_hit, self.game.thunderbird_bullets, 1000),
            call(
                self.thunderbird_ship, thunderbird_hit, self.game.phoenix_bullets, 1000
            ),
            call(self.phoenix_ship, phoenix_hit, self.game.thunderbird_missiles, 1000),
            call(
                self.thunderbird_ship, thunderbird_hit, self.game.phoenix_missiles, 1000
            ),
            call(self.phoenix_ship, phoenix_hit, self.game.thunderbird_laser, 1000),
            call(self.thunderbird_ship, thunderbird_hit, self.game.phoenix_laser, 1000),
        ]

        self.assertEqual(
            self.collision_manager._resolve_collision_cosmic_conflict.call_args_list,
            expected_calls,
        )

    def test_check_alien_ship_collisions(self):
        """Test the check_alien_ship_collisions method."""
        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()

        self.collision_manager._check_aliens_bottom = MagicMock()
        self.thunderbird_ship.state.alive = True
        self.thunderbird_ship.state.immune = False
        self.phoenix_ship.state.alive = True
        self.phoenix_ship.state.immune = False
        self.game.aliens = [alien]

        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()

        self.collision_manager.check_alien_ship_collisions(thunderbird_hit, phoenix_hit)

        thunderbird_hit.assert_called_once()
        phoenix_hit.assert_called_once()
        self.collision_manager._check_aliens_bottom.assert_called_once()

    def test_check_aliens_bottom_aliens_below_bottom(self):
        """Test the check_aliens_bottom when aliens have reached
        the bottom of the screen.
        """
        self.game.singleplayer = False
        self.game.screen = pygame.Surface((800, 600))
        self.game.stats.thunderbird_score = 1000
        self.game.stats.phoenix_score = 1000

        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()
        alien.rect.bottom = 700
        aliens = pygame.sprite.Group(alien)
        self.game.aliens = aliens

        self.collision_manager._check_aliens_bottom()

        alien.kill.assert_called_once()
        self.assertEqual(self.game.stats.thunderbird_score, 900)
        self.assertEqual(self.game.stats.phoenix_score, 900)
        self.game.score_board.render_scores.assert_called_once()
        self.game.score_board.update_high_score.assert_called_once()

    def test_check_aliens_bottom_aliens_above_bottom(self):
        """Test the check_aliens_bottom when aliens have not
        reached the bottom of the screen.
        """
        self.game.screen = pygame.Surface((800, 600))
        self.game.stats.thunderbird_score = 1000
        self.game.stats.phoenix_score = 1000

        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()
        alien.rect.bottom = 500
        aliens = pygame.sprite.Group(alien)
        self.game.aliens = aliens

        self.collision_manager._check_aliens_bottom()

        self.assertEqual(self.game.stats.thunderbird_score, 1000)
        self.assertEqual(self.game.stats.phoenix_score, 1000)

        alien.kill.assert_not_called()
        self.game.score_board.render_scores.assert_not_called()
        self.game.score_board.update_high_score.assert_not_called()

    def test_check_missile_alien_collisions(self):
        """Test the check_missile_alien_collisions method."""
        # Singleplayer test case
        self.game.singleplayer = True
        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()

        thunder_missile = MagicMock(spec=pygame.sprite.Sprite)
        thunder_missile.rect = MagicMock()

        phoenix_missile = MagicMock(spec=pygame.sprite.Sprite)
        phoenix_missile.rect = MagicMock()

        self.collision_manager._handle_player_missile_collisions = MagicMock()
        self.collision_manager._play_missile_sound = MagicMock()
        self.game.aliens = [alien]

        self.game.thunderbird_missiles = pygame.sprite.Group(thunder_missile)
        self.game.phoenix_missiles = pygame.sprite.Group(phoenix_missile)

        self.collision_manager.check_missile_alien_collisions()

        self.collision_manager._handle_player_missile_collisions.assert_called_once()
        self.collision_manager._play_missile_sound.assert_called_once()

        # Multiplayer test case
        self.collision_manager._handle_player_missile_collisions.reset_mock()
        self.collision_manager._play_missile_sound.reset_mock()
        self.game.singleplayer = False

        self.collision_manager.check_missile_alien_collisions()

        # Assert that the methods were called for both cases
        self.assertEqual(
            self.collision_manager._handle_player_missile_collisions.call_count, 2
        )
        self.assertEqual(self.collision_manager._play_missile_sound.call_count, 2)

    @patch("src.game_logic.collision_detection.time.time")
    def test_check_laser_alien_collisions(self, mock_time):
        """Test the check_laser_alien_collisions method."""
        self.collision_manager._update_stats = MagicMock()
        self.collision_manager._handle_boss_alien_collision = MagicMock()
        mock_time.return_value = 3

        alien = MagicMock(spec=pygame.sprite.Sprite)
        alien.rect = MagicMock()

        boss_alien = MagicMock(spec=BossAlien)
        boss_alien.rect = MagicMock()
        boss_alien.last_hit_time = 0
        boss_alien.hit_count = 0

        laser = MagicMock(spec=pygame.sprite.Sprite)
        laser.rect = MagicMock()

        self.game.thunderbird_laser = pygame.sprite.Group(laser)
        self.game.phoenix_laser = pygame.sprite.Group(laser)
        self.game.aliens = [alien, boss_alien]
        self.game.aliens[0].immune_state = False

        self.collision_manager.check_laser_alien_collisions()

        expected_calls = [
            call(
                alien,
                "thunderbird",
            ),
            call(
                alien,
                "phoenix",
            ),
        ]

        self.assertEqual(
            self.collision_manager._update_stats.call_args_list, expected_calls
        )
        self.collision_manager._handle_boss_alien_collision.assert_called_once_with(
            boss_alien, "thunderbird"
        )
        self.assertEqual(boss_alien.hit_count, 1)
        self.assertEqual(boss_alien.last_hit_time, mock_time.return_value)

    @patch("src.game_logic.collision_detection.play_sound")
    def test_play_missile_sound(self, mock_play_sound):
        """Test the play_missile_sound method."""
        alien = MagicMock()
        boss_alien = MagicMock(spec=BossAlien)

        aliens = [[alien], [boss_alien]]

        self.collision_manager._play_missile_sound(aliens)

        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "missile"
        )

    def test_handle_player_missile_collisions(self):
        """Test the handle_player_missile_collisions method."""
        self.collision_manager._check_missile_ex_collision = MagicMock()
        missile1 = MagicMock()
        missile2 = MagicMock()

        # Set up the player missile collisions
        player_missile_collisions = {
            missile1: [MagicMock()],
            missile2: [MagicMock()],
        }

        self.collision_manager._handle_player_missile_collisions(
            player_missile_collisions, "thunderbird"
        )

        # Assert that the explode method was called for each missile
        self.assertTrue(missile1.explode.called)
        self.assertTrue(missile2.explode.called)

        # Assert that the _check_missile_ex_collision method was called with the correct arguments
        self.assertEqual(
            self.collision_manager._check_missile_ex_collision.call_count, 2
        )

        expected_calls = [
            call(
                self.game.aliens,
                "thunderbird",
                missile1,
            ),
            call(
                self.game.aliens,
                "thunderbird",
                missile2,
            ),
        ]

        self.assertEqual(
            self.collision_manager._check_missile_ex_collision.call_args_list,
            expected_calls,
        )

    @patch("src.game_logic.collision_detection.pygame.sprite.spritecollideany")
    def test_check_alien_bullets_collisions(self, mock_collide):
        """Test the check_alien_bullets_collisions method."""
        # Collisions are happening and one ship is immune
        # and the other is not
        self.game.singleplayer = False
        thunderbird_hit = MagicMock()
        phoenix_hit = MagicMock()

        for ship in self.game.ships:
            ship.state.alive = True

        self.thunderbird_ship.state.immune = True
        self.phoenix_ship.state.immune = False

        alien_bullet = MagicMock(spec=pygame.sprite.Sprite)
        alien_bullet.rect = MagicMock()
        self.game.alien_bullet = [alien_bullet]

        self.collision_manager.check_alien_bullets_collisions(
            thunderbird_hit, phoenix_hit
        )

        thunderbird_hit.assert_not_called()
        phoenix_hit.assert_called_once()

        # No collision is happening
        thunderbird_hit.reset_mock()
        phoenix_hit.reset_mock()

        mock_collide.return_value = None
        for ship in self.game.ships:
            ship.state.alive = True
            ship.state.immune = False

        self.collision_manager.check_alien_bullets_collisions(
            thunderbird_hit, phoenix_hit
        )

        thunderbird_hit.assert_not_called()
        phoenix_hit.assert_not_called()

    @patch("src.game_logic.collision_detection.play_sound")
    def test_handle_boss_alien_collision(self, mock_play_sound):
        """Test the handle_boss_alien_collision method."""
        player = "thunderbird"
        self.game.settings.boss_hp = 10
        self.game.stats.thunderbird_score = 0
        self.game.stats.phoenix_score = 0
        self.game.settings.boss_points = 1500

        boss = MagicMock()
        boss.hit_count = 5
        boss.is_alive = True

        # Case when the boss hit count has not reached the
        # boss_hp so the boss is not destroyed.
        self.collision_manager._handle_boss_alien_collision(boss, player)

        boss.destroy_alien.assert_not_called()
        mock_play_sound.assert_not_called()

        # Case when the hit_count matches the boss hp so the
        # boss is destroyed.
        boss.hit_count = 10

        self.collision_manager._handle_boss_alien_collision(boss, player)

        boss.destroy_alien.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "boss_exploding"
        )
        self.game.aliens.remove.assert_called_once_with(boss)
        self.assertEqual(
            self.game.stats.thunderbird_score, self.game.settings.boss_points
        )
        self.assertEqual(self.game.stats.phoenix_score, 0)
        self.game.score_board.render_scores.assert_called_once()
        self.game.score_board.update_high_score.assert_called_once()

    def test_handle_alien_hits_boss_alien(self):
        """Test the handle_alien_hits with a boss."""
        player = "thunderbird"

        # Create mock boss
        boss_alien = MagicMock(spec=BossAlien)
        boss_alien.hit_count = 0
        boss_alien.is_baby = False
        boss_alien.immune_state = False

        # Create mock collisions
        player_ship_collisions = {"some_key": [boss_alien]}

        self.game.stats.level = 1
        self.collision_manager._handle_boss_alien_collision = MagicMock()
        self.collision_manager._update_stats = MagicMock()

        self.collision_manager._handle_alien_hits(player_ship_collisions, player)

        # Assertions
        self.assertEqual(boss_alien.hit_count, 1)
        self.collision_manager._handle_boss_alien_collision.assert_called_with(
            boss_alien, player
        )

        self.collision_manager._update_stats.assert_not_called()

    def test_handle_alien_hits_aliens(self):
        """Test the handle_alien_hits method with normal and baby
        aliens."""
        player = "phoenix"

        alien = MagicMock()
        alien.hit_count = 3
        alien.is_baby = False
        alien.immune_state = False

        # Create mock collisions
        player_ship_collisions = {"some_key": [alien]}
        self.game.stats.level = 5
        self.collision_manager._handle_boss_alien_collision = MagicMock()
        self.collision_manager._update_stats = MagicMock()

        # Normal alien test case
        self.collision_manager._handle_alien_hits(player_ship_collisions, player)

        # Assertions
        self.assertEqual(alien.hit_count, 4)
        self.collision_manager._update_stats.assert_called_once_with(alien, player)

        self.collision_manager._handle_boss_alien_collision.assert_not_called()

        # Baby alien test case
        self.collision_manager._update_stats.reset_mock()
        alien.is_baby = True

        self.collision_manager._handle_alien_hits(player_ship_collisions, player)

        self.assertEqual(alien.hit_count, 5)
        self.collision_manager._update_stats.assert_called_once_with(alien, player)

        self.collision_manager._handle_boss_alien_collision.assert_not_called()

    @patch("src.game_logic.collision_detection.play_sound")
    def test_update_stats(self, mock_play_sound):
        """Test the update_stats method."""
        player1 = "thunderbird"
        player2 = "phoenix"

        alien = MagicMock()

        self.game.settings.alien_points = 5
        self.game.stats.thunderbird_score = 0
        self.game.stats.phoenix_score = 0
        self.thunderbird_ship.aliens_killed = 0
        self.phoenix_ship.aliens_killed = 0

        # Player1 test case
        self.collision_manager._update_stats(alien, player1)

        self.assertEqual(
            self.game.stats.thunderbird_score, self.game.settings.alien_points
        )
        self.assertEqual(self.thunderbird_ship.aliens_killed, 1)
        alien.destroy_alien.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "alien_exploding"
        )
        self.game.aliens.remove.assert_called_once_with(alien)

        # Player2 test case
        alien.reset_mock()
        mock_play_sound.reset_mock()
        self.game.aliens.reset_mock()

        self.collision_manager._update_stats(alien, player2)

        self.assertEqual(self.game.stats.phoenix_score, self.game.settings.alien_points)
        self.assertEqual(self.phoenix_ship.aliens_killed, 1)
        alien.destroy_alien.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "alien_exploding"
        )
        self.game.aliens.remove.assert_called_once_with(alien)

        # Assert that the methods were called for each player one time.
        self.assertEqual(self.game.score_board.render_scores.call_count, 2)
        self.assertEqual(self.game.score_board.update_high_score.call_count, 2)

    @patch("src.game_logic.collision_detection.play_sound")
    def test_check_missile_ex_collision_with_aliens(self, mock_play_sound):
        """Test the check_missile_ex_collision with aliens."""
        player = "thunderbird"

        alien = MagicMock()
        missile = MagicMock()
        missile.rect.center = (100, 100)

        # mock ex_frame
        ex_frame = MagicMock()
        ex_frame.get_rect.return_value = MagicMock()
        ex_frame.get_rect.return_value.colliderect.return_value = True

        missile.destroy_anim.ex_frames = [ex_frame]

        self.collision_manager._update_stats = MagicMock()
        self.collision_manager._handle_boss_alien_collision = MagicMock()

        self.collision_manager._check_missile_ex_collision([alien], player, missile)

        # Assertions
        ex_frame.get_rect.assert_called_with(center=missile.rect.center)
        ex_frame.get_rect.return_value.colliderect.assert_called_with(alien.rect)
        self.collision_manager._update_stats.assert_called_with(alien, player)
        self.assertEqual(self.collision_manager.handled_collisions, {})

        self.collision_manager._handle_boss_alien_collision.assert_not_called()
        mock_play_sound.assert_not_called()

    @patch("src.game_logic.collision_detection.play_sound")
    def test_check_missile_ex_collision_with_alien_boss(self, mock_play_sound):
        """Test the check_missile_ex_collision with aliens."""
        player = "thunderbird"

        boss = MagicMock(spec=BossAlien)
        boss.rect = MagicMock()
        boss.hit_count = 0

        missile = MagicMock()
        missile.rect.center = (100, 100)

        # mock ex_frame
        ex_frame = MagicMock()
        ex_frame.get_rect.return_value = MagicMock()
        ex_frame.get_rect.return_value.colliderect.return_value = True

        missile.destroy_anim.ex_frames = [ex_frame]

        self.collision_manager._update_stats = MagicMock()
        self.collision_manager._handle_boss_alien_collision = MagicMock()

        self.collision_manager._check_missile_ex_collision([boss], player, missile)

        # Assertions
        ex_frame.get_rect.assert_called_with(center=missile.rect.center)
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "missile"
        )
        self.assertEqual(boss.hit_count, 5)
        self.collision_manager._handle_boss_alien_collision.assert_called_once_with(
            boss, player
        )
        self.assertEqual(
            self.collision_manager.handled_collisions, {(missile, boss): True}
        )

        self.collision_manager._update_stats.assert_not_called()


if __name__ == "__main__":
    unittest.main()
