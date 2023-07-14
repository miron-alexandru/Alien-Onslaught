"""
This module tests the AliensManager class that is used to manage
the aliens in the game.
"""

import unittest
from unittest.mock import MagicMock

from src.entities.alien_entities.aliens import Alien, BossAlien
from src.managers.alien_managers.aliens_manager import AliensManager


class AliensManagerTest(unittest.TestCase):
    """Test cases for the AliensManager class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.manager = AliensManager(
            self.game, self.game.aliens, self.game.settings, self.game.screen
        )

    def test_create_fleet(self):
        """Test the creation of the fleet."""
        self.game.settings.aliens_num = 8
        rows = 3
        self.manager.create_fleet(rows)

        # Assert that the correct number of aliens were created
        self.assertEqual(
            len(self.game.aliens.add.call_args_list),
            rows * self.game.settings.aliens_num,
        )

        # Assert that each alien's position was set correctly
        calls = self.game.aliens.add.call_args_list
        for row_number in range(rows):
            for alien_number in range(self.game.settings.aliens_num):
                alien = calls[
                    row_number * self.game.settings.aliens_num + alien_number
                ][0][0]
                expected_x = alien.rect.width + 2 * alien.rect.width * alien_number
                expected_y = 50 - (2 * alien.rect.height * row_number)
                self.assertEqual(alien.rect.x, expected_x)
                self.assertEqual(alien.rect.y, expected_y)

    def test_create_boss_alien(self):
        """Test the creation of boss aliens."""
        self.manager.create_boss_alien()

        # Assert that a boss alien was added to the aliens group
        self.assertTrue(self.game.aliens.add.called)
        added_alien = self.game.aliens.add.call_args[0][0]
        self.assertIsInstance(added_alien, BossAlien)

    def test_update_aliens(self):
        """Test the update of aliens."""
        self.manager._check_fleet_edges = MagicMock()
        self.game.aliens.update = MagicMock()

        self.manager.update_aliens()

        # Assert that the _check_fleet_edges and update methods were called
        self.manager._check_fleet_edges.assert_called_once()
        self.game.aliens.update.assert_called_once()

    def test__check_fleet_edges(self):
        """Test the check_fleet_edges method."""
        alien1 = MagicMock(spec=Alien)
        alien1.check_edges.return_value = True
        alien1.motion = MagicMock()
        alien1.motion.direction = 1

        alien2 = MagicMock(spec=Alien)
        alien2.check_edges.return_value = False
        alien2.check_top_edges.return_value = True
        alien2.rect = MagicMock()
        alien2.rect.y = 100
        alien2.motion = MagicMock()
        alien2.motion.direction = 1

        boss_alien = MagicMock(spec=BossAlien)
        boss_alien.check_edges.return_value = True
        boss_alien.motion = MagicMock()
        boss_alien.motion.direction = 1

        boss_alien2 = MagicMock(spec=BossAlien)
        boss_alien2.motion = MagicMock()
        boss_alien2.motion.direction = 1
        boss_alien2.check_edges.return_value = False

        self.game.aliens.sprites.return_value = [
            alien1,
            alien2,
            boss_alien,
            boss_alien2,
        ]

        self.manager._check_fleet_edges()

        # Assert that the direction when it was supposed to.
        self.assertEqual(alien1.motion.direction, -1)
        self.assertEqual(alien2.motion.direction, 1)

        self.assertEqual(boss_alien.motion.direction, -1)
        self.assertEqual(boss_alien2.motion.direction, 1)

        self.assertEqual(alien2.rect.y, 100 + self.game.settings.alien_speed)


if __name__ == "__main__":
    unittest.main()
