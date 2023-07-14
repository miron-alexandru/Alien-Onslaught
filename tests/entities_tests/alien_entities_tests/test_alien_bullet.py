"""
This module tests the AlienBullet class that is used for
creating alien bullets in the game.
"""

import unittest
from unittest.mock import MagicMock, Mock

from src.entities.alien_entities.alien_bullets import AlienBullet


class TestAlienBullet(unittest.TestCase):
    """Test cases for the AlienBullet class."""

    def setUp(self):
        self.game = MagicMock()
        self.game.aliens.sprites = MagicMock(return_value=[MagicMock()])
        self.alien_bullet = AlienBullet(self.game)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertIsInstance(self.alien_bullet, AlienBullet)
        self.assertEqual(self.alien_bullet.screen, self.game.screen)
        self.assertEqual(self.alien_bullet.settings, self.game.settings)
        self.assertIsNotNone(self.alien_bullet.image)
        self.assertIsNotNone(self.alien_bullet.rect)

    def test_scale_bullet(self):
        """Test the scaling of the bullet."""
        initial_width, initial_height = self.alien_bullet.image.get_size()

        self.alien_bullet.scale_bullet(0.5)

        self.assertEqual(
            self.alien_bullet.image.get_size(),
            (int(initial_width * 0.5), int(initial_height * 0.5)),
        )
        self.assertEqual(
            self.alien_bullet.rect.center,
            self.alien_bullet.image.get_rect(
                center=self.alien_bullet.rect.center
            ).center,
        )

    def test_choose_random_alien_and_place_bullet(self):
        """Test the choosing of the random alien and placing the bullet."""
        mock_alien1 = Mock(rect=Mock(centerx=100, bottom=500), is_baby=False)
        mock_alien2 = Mock(rect=Mock(centerx=200, bottom=500), is_baby=False)
        self.game.aliens.sprites.return_value = [mock_alien1, mock_alien2]

        self.alien_bullet._choose_random_alien(self.game)

        # Check that the bullet is positioned correctly relative to one of the alien sprites
        self.assertIn(self.alien_bullet.rect.centerx, [100, 200])
        self.assertEqual(self.alien_bullet.rect.bottom, 500)

    def test_update(self):
        """Test the update of the bullet."""
        self.alien_bullet.y_pos = 50
        self.game.settings.alien_bullet_speed = 3
        initial_y_pos = self.alien_bullet.y_pos
        expected_y_pos = initial_y_pos + self.game.settings.alien_bullet_speed

        self.alien_bullet.update()

        self.assertAlmostEqual(self.alien_bullet.y_pos, expected_y_pos)
        self.assertEqual(self.alien_bullet.rect.y, expected_y_pos)

        self.alien_bullet.y_pos = 159
        initial_y_pos = self.alien_bullet.y_pos
        expected_y_pos = initial_y_pos + self.game.settings.alien_bullet_speed

        self.alien_bullet.update()

        self.assertAlmostEqual(self.alien_bullet.y_pos, expected_y_pos)
        self.assertEqual(self.alien_bullet.rect.y, expected_y_pos)

    def test_draw(self):
        """Test drawing of bullet."""
        self.alien_bullet.draw()

        self.alien_bullet.screen.blit.assert_called_once_with(
            self.alien_bullet.image, self.alien_bullet.rect
        )


if __name__ == "__main__":
    unittest.main()
