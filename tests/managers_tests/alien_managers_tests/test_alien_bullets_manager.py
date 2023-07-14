"""
This module tests the ALienBulletsManager class that is used to manage
alien bullets in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.managers.alien_managers.alien_bullets_manager import AlienBulletsManager
from src.entities.alien_entities.aliens import Alien, BossAlien


class AlienBulletsManagerTestCase(unittest.TestCase):
    """Test cases for AlienBulletsManager."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.manager = AlienBulletsManager(self.game)

    def test_init(self):
        """Test the initialization of the class."""
        self.assertEqual(self.manager.game, self.game)
        self.assertEqual(self.manager.screen, self.game.screen)
        self.assertEqual(self.manager.settings, self.game.settings)
        self.assertEqual(self.manager.stats, self.game.stats)
        self.assertEqual(self.manager.alien_bullet, self.game.alien_bullet)
        self.assertEqual(self.manager.aliens, self.game.aliens)
        self.assertEqual(self.manager.thunderbird_ship, self.game.thunderbird_ship)
        self.assertEqual(self.manager.phoenix_ship, self.game.phoenix_ship)
        self.assertEqual(self.manager.last_alien_bullet_time, 0)

    @patch("src.managers.alien_managers.alien_bullets_manager.BossBullet")
    def test_create_alien_bullet_boss(self, mock_boss_bullet):
        """Test the creation of a BossBullet."""
        self.manager.alien_bullet.add = MagicMock()
        alien = MagicMock(spec=BossAlien)
        alien.rect = MagicMock()

        mock_boss_bullet_instance = MagicMock()
        mock_boss_bullet.return_value = mock_boss_bullet_instance
        alien.rect.centerx = 15
        alien.rect.bottom = 5

        self.manager._create_alien_bullet(alien)

        mock_boss_bullet.assert_called_once_with(self.manager, alien)
        self.assertEqual(mock_boss_bullet_instance.rect.centerx, alien.rect.centerx)
        self.assertEqual(mock_boss_bullet_instance.rect.bottom, alien.rect.bottom)
        self.manager.alien_bullet.add.assert_called_once_with(mock_boss_bullet_instance)

    @patch("src.managers.alien_managers.alien_bullets_manager.AlienBullet")
    def test_create_alien_bullet_normal(self, mock_alien_bullet):
        """Test the creation of the normal alien bullet."""
        self.manager.alien_bullet.add = MagicMock()
        alien = MagicMock(spec=Alien)
        alien.rect = MagicMock()

        mock_alien_bullet_instance = MagicMock()
        mock_alien_bullet.return_value = mock_alien_bullet_instance
        alien.rect.centerx = 15
        alien.rect.bottom = 5

        self.manager._create_alien_bullet(alien)

        mock_alien_bullet.assert_called_once_with(self.manager)
        self.assertEqual(mock_alien_bullet_instance.rect.centerx, alien.rect.centerx)
        self.assertEqual(mock_alien_bullet_instance.rect.bottom, alien.rect.bottom)
        self.manager.alien_bullet.add.assert_called_once_with(
            mock_alien_bullet_instance
        )

    @patch("random.sample")
    @patch("pygame.time.get_ticks")
    def test_create_alien_bullets(self, mock_get_ticks, mock_sample):
        """Test the creation of multiple alien bullets."""
        num_bullets = 3
        bullet_int = 1000
        alien_int = 500
        current_time = 5000

        mock_get_ticks.return_value = current_time

        alien1 = MagicMock()
        alien1.last_bullet_time = 0
        alien2 = MagicMock()
        alien2.last_bullet_time = 4000
        alien3 = MagicMock()
        alien3.last_bullet_time = 2000
        aliens = [alien1, alien2, alien3]

        self.game.aliens.sprites.return_value = aliens

        selected_aliens = [alien1, alien3]
        mock_sample.return_value = selected_aliens

        self.manager._create_alien_bullet = MagicMock()

        self.manager.create_alien_bullets(num_bullets, bullet_int, alien_int)

        mock_get_ticks.assert_called_once()
        mock_sample.assert_called_once_with(
            self.game.aliens.sprites(),
            k=min(num_bullets, len(self.game.aliens.sprites())),
        )

        self.assertEqual(alien1.last_bullet_time, current_time)
        self.assertEqual(alien2.last_bullet_time, 4000)
        self.assertEqual(alien3.last_bullet_time, current_time)
        self.assertEqual(self.manager._create_alien_bullet.call_count, 2)

    def test_update_alien_bullets(self):
        """Test the update of the alien bullets."""
        self.game.settings.screen_height = 780
        bullet1 = MagicMock()
        bullet1.rect.y = 200
        bullet2 = MagicMock()
        bullet2.rect.y = 800

        self.manager.alien_bullet.copy.return_value = [bullet1, bullet2]

        self.manager.update_alien_bullets()

        self.manager.alien_bullet.update.assert_called_once()
        self.manager.alien_bullet.remove.assert_called_once_with(bullet2)


if __name__ == "__main__":
    unittest.main()
