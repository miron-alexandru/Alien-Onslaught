"""
This module tests the BossAlien class which is used for creating
alien bosses in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.entities.alien_entities.aliens import BossAlien


class TestBossAlien(unittest.TestCase):
    """Test cases for BossAlien."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.game.screen = pygame.Surface((800, 600))
        self.boss_alien = BossAlien(self.game)
        self.boss_alien.destroy = MagicMock()

    def test_init(self):
        """Test the initialization of the boss alien."""
        self.assertIsNotNone(self.boss_alien.screen)
        self.assertIsNotNone(self.boss_alien.settings)
        self.assertIsNotNone(self.boss_alien.image)
        self.assertIsNotNone(self.boss_alien.motion)
        self.assertIsNotNone(self.boss_alien.destroy)
        self.assertFalse(self.boss_alien.frozen_state)
        self.assertFalse(self.boss_alien.immune_state)
        self.assertTrue(self.boss_alien.is_alive)

    def test_update_image_boss_rush(self):
        """Test the update of the image in boss rush."""
        self.boss_alien.settings.game_modes.boss_rush = True

        level_image_mapping = {
            2: "boss2",
            5: "boss5",
            8: "boss8",
            10: "boss10",
            13: "boss13",
            15: "boss15",
        }

        for level, expected_image in level_image_mapping.items():
            self._check_level_mapping(level, expected_image)

    def test_update_image_normal(self):
        """Test the update of the image in normal game mode."""
        self.boss_alien.settings.game_modes.boss_rush = False

        level_image_mapping = {
            1: "boss2",
            10: "boss2",
            15: "normal15",
            20: "normal20",
            25: "normal25",
            9999: "normal25",
        }

        for level, expected_image in level_image_mapping.items():
            self._check_level_mapping(level, expected_image)

    def _check_level_mapping(self, level, expected_image):
        """Method used to help the testing for multiple level images."""
        self.game.stats.level = level

        self.boss_alien._update_image(self.game)

        self.assertEqual(
            self.boss_alien.image, self.boss_alien.boss_images[expected_image]
        )

    def test_update_movement(self):
        """Test the update movement of the boss alien."""
        # Test case: Boss alien not frozen, moving in positive direction
        self.boss_alien.frozen_state = False
        self.boss_alien.motion.direction = 1
        self.boss_alien.x_pos = 0.0
        self.game.settings.alien_speed = 2
        self.game.settings.frozen_time = 30

        self.boss_alien.update()

        self.assertEqual(self.boss_alien.x_pos, self.boss_alien.settings.alien_speed)
        self.assertEqual(self.boss_alien.rect.x, round(self.boss_alien.x_pos))

        # Test case: Boss alien not frozen, moving in negative direction
        self.boss_alien.motion.direction = -1
        self.boss_alien.x_pos = 4.0

        self.boss_alien.update()

        self.assertEqual(
            self.boss_alien.x_pos, 4.0 - self.boss_alien.settings.alien_speed
        )
        self.assertEqual(self.boss_alien.rect.x, round(self.boss_alien.x_pos))

        # Test case: Boss alien frozen, should not move
        self.boss_alien.freeze()
        self.boss_alien.x_pos = 4.0
        self.boss_alien.rect.x = 4

        self.boss_alien.update()

        self.assertEqual(self.boss_alien.x_pos, 4.0)  # No change expected
        self.assertEqual(self.boss_alien.rect.x, 4)  # No change expected

    def test_check_edges(self):
        """Test the check_edges method of the boss alien."""
        # Test case: Boss alien at the right edge of the screen
        self.boss_alien.rect.right = self.game.screen.get_rect().right

        self.assertTrue(self.boss_alien.check_edges())

        # Test case: Boss alien at the left edge of the screen
        self.boss_alien.rect.left = 0

        self.assertTrue(self.boss_alien.check_edges())

        # Test case: Boss alien not at the edge of the screen
        self.boss_alien.rect.right = 100
        self.boss_alien.rect.left = 100

        self.assertFalse(self.boss_alien.check_edges())

    def test_destroy_alien(self):
        """Test the destroy_alien method."""
        self.boss_alien.is_alive = True

        self.boss_alien.destroy_alien()

        self.assertFalse(self.boss_alien.is_alive)
        self.boss_alien.destroy.update_destroy_animation.assert_called_once()
        self.boss_alien.destroy.draw_animation.assert_called_once()

    def test_freeze(self):
        """Test the freeze method."""
        self.assertFalse(self.boss_alien.frozen_state)
        self.assertEqual(self.boss_alien.frozen_start_time, 0)

        self.boss_alien.freeze()

        self.assertTrue(self.boss_alien.frozen_state)
        self.assertNotEqual(self.boss_alien.frozen_start_time, 0)

    def test_upgrade(self):
        """Test the upgrade method."""
        self.game.settings.boss_hp = 50
        initial_boss_hp = self.boss_alien.settings.boss_hp

        self.boss_alien.upgrade()

        self.assertEqual(self.boss_alien.settings.boss_hp, initial_boss_hp + 15)

    def test_draw(self):
        """Test the drawing of the boss alien."""
        self.boss_alien.screen = MagicMock()

        self.boss_alien.draw()

        self.boss_alien.screen.blit.assert_called_once_with(
            self.boss_alien.image, self.boss_alien.rect
        )


if __name__ == "__main__":
    unittest.main()
