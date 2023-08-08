"""
This module contains test cases for the Bullet class which is the base class
for creating bullets for each player.
"""

from unittest.mock import MagicMock
import unittest

import pygame

from src.entities.projectiles.bullet import Bullet


class TestBullet(unittest.TestCase):
    """Test cases for the Bullet class."""

    def setUp(self):
        """Set up the necessary objects for testing."""
        self.game = MagicMock()
        self.game.settings.player_bullet_speed = 5
        self.ship = MagicMock()
        self.ship.rect = pygame.Rect(400, 500, 50, 50)
        self.bullet_image = pygame.Surface((10, 10))
        self.bullet = Bullet(
            self.game,
            self.bullet_image,
            self.ship,
            self.game.settings.player_bullet_speed,
        )

    def test_init(self):
        """Test the initialization of the bullet."""
        self.assertEqual(self.bullet.game, self.game)
        self.assertEqual(self.bullet.ship, self.ship)
        self.assertEqual(self.bullet.image, self.bullet_image)
        self.assertEqual(
            self.bullet.rect.midtop, (self.ship.rect.centerx, self.ship.rect.top)
        )
        self.assertAlmostEqual(self.bullet.y_pos, float(self.ship.rect.y))

        # assert with an offset from the ship
        self.assertLessEqual(self.bullet.x_pos, self.ship.rect.x + 20)
        self.assertGreaterEqual(self.bullet.x_pos, self.ship.rect.x + 5)
        self.assertEqual(self.bullet.speed, self.game.settings.player_bullet_speed)

    def test_update_cosmic_conflict_mode(self):
        """Test the update method in cosmic conflict mode."""
        self.game.settings.game_modes.cosmic_conflict = True
        self.bullet.x_pos = self.ship.rect.x
        expected_x_pos = (
            self.ship.rect.x + self.game.settings.player_bullet_speed
            if self.ship == self.game.thunderbird_ship
            else self.ship.rect.x - self.game.settings.player_bullet_speed
        )

        self.bullet.update()

        self.assertAlmostEqual(self.bullet.x_pos, expected_x_pos)
        self.assertEqual(self.bullet.rect.x, int(expected_x_pos))

    def test_update_other_modes(self):
        """Test the update method in other modes."""
        self.game.settings.game_modes.cosmic_conflict = False
        self.bullet.y_pos = self.ship.rect.y
        expected_y_pos = self.ship.rect.y - self.game.settings.player_bullet_speed

        self.bullet.update()

        self.assertAlmostEqual(self.bullet.y_pos, expected_y_pos)
        self.assertEqual(self.bullet.rect.y, int(expected_y_pos))

    def test_draw(self):
        """Test the draw method."""
        self.bullet.draw()

        self.game.screen.blit.assert_called_once_with(
            self.bullet_image, self.bullet.rect
        )

    def test_scale_bullet(self):
        """Test the scale_bullet method."""
        original_width, original_height = self.bullet.image.get_size()
        scale = 0.5
        expected_width = int(original_width * scale)
        expected_height = int(original_height * scale)

        self.bullet.scale_bullet(scale)

        self.assertEqual(
            self.bullet.image.get_size(), (expected_width, expected_height)
        )
        self.assertEqual(
            self.bullet.rect.center,
            self.bullet.image.get_rect(center=self.bullet.rect.center).center,
        )


if __name__ == "__main__":
    unittest.main()
