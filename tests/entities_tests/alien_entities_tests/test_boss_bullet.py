"""
This module tests the BossBullet class that is used for
creating boss alien bullets in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.entities.alien_entities.alien_bullets import BossBullet
from src.entities.alien_entities.aliens import BossAlien


class TestBossBullet(unittest.TestCase):
    """Test cases for the BossBullet class."""

    def setUp(self):
        self.game = MagicMock()
        self.alien = BossAlien(self.game)
        self.bullet = BossBullet(self.game, self.alien)

    def test_init(self):
        """Test the init method."""
        self.assertEqual(self.bullet.screen, self.game.screen)
        self.assertEqual(self.bullet.alien, self.alien)
        self.assertIsNotNone(self.bullet.image)
        self.assertIsInstance(self.bullet.image, pygame.Surface)
        self.assertIsNotNone(self.bullet.rect)
        self.assertIsInstance(self.bullet.rect, pygame.Rect)
        self.assertIsInstance(self.bullet.y_pos, float)
        self.assertIsInstance(self.bullet.x_vel, float)

    def test_update_image_boss_rush(self):
        """Test updating the image in boss rush game mode."""
        self.bullet.settings.game_modes.boss_rush = True

        level_image_mapping = {
            2: "boss_bullet2",
            5: "boss_bullet5",
            8: "boss_bullet8",
            10: "boss_bullet10",
            13: "boss_bullet13",
            15: "boss_bullet15",
        }

        for level, expected_image in level_image_mapping.items():
            self._check_level_mapping(level, expected_image)

    def test_update_image_normal_mode(self):
        """Test updating the image of the bullet in normal game mode."""
        self.bullet.settings.game_modes.boss_rush = False

        level_image_mapping = {
            1: "boss_bullet2",
            10: "boss_bullet2",
            15: "normal_bullet15",
            20: "normal_bullet20",
            25: "normal_bullet25",
            100: "normal_bullet25",
        }

        for level, expected_image in level_image_mapping.items():
            self._check_level_mapping(level, expected_image)

    def _check_level_mapping(self, level, expected_image):
        """Method used to help the testing for multiple level images."""
        self.game.stats.level = level
        self.bullet._update_image(self.game)
        self.assertEqual(self.bullet.image, self.bullet.bullet_images[expected_image])

    def test_update(self):
        """Test the updating of the bullet."""
        self.game.settings.alien_bullet_speed = 2
        initial_y_pos = self.bullet.y_pos
        initial_rect_y = self.bullet.rect.y
        initial_rect_x = self.bullet.rect.x

        self.bullet.update()

        # Assertions
        self.assertEqual(
            self.bullet.y_pos, initial_y_pos + self.bullet.settings.alien_bullet_speed
        )
        self.assertEqual(
            self.bullet.rect.y, initial_rect_y + self.bullet.settings.alien_bullet_speed
        )
        self.assertAlmostEqual(
            self.bullet.rect.x, initial_rect_x + round(self.bullet.x_vel)
        )

        # Test movement in the x-axis
        initial_y_pos = self.bullet.y_pos
        initial_rect_y = self.bullet.rect.y
        initial_rect_x = self.bullet.rect.x
        self.bullet.x_vel = 2.5

        self.bullet.update()

        # Assertions
        self.assertEqual(
            self.bullet.y_pos, initial_y_pos + self.bullet.settings.alien_bullet_speed
        )
        self.assertEqual(
            self.bullet.rect.y,
            initial_rect_y + int(self.bullet.settings.alien_bullet_speed),
        )
        self.assertAlmostEqual(
            self.bullet.rect.x, initial_rect_x + round(self.bullet.x_vel)
        )

    def test_draw(self):
        """Test the drawing of the bullet."""
        self.bullet.draw()

        self.bullet.screen.blit.assert_called_once_with(
            self.bullet.image, self.bullet.rect
        )


if __name__ == "__main__":
    unittest.main()
