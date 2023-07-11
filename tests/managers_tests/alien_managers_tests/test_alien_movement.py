"""
This module tests the AlienMovement class which manages
the movement behaviors of the aliens.
"""

import math

import unittest
from unittest.mock import MagicMock, patch

from src.managers.alien_managers.aliens_behaviors import AlienMovement


class AlienMovementTestCase(unittest.TestCase):
    """Test cases for the AlienMovement class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.alien = MagicMock()

        self.alien_movement = AlienMovement(self.alien, self.game)

    @patch("pygame.time.get_ticks", return_value=15000)
    @patch("random.randint", return_value=10)
    def test_update_horizontal_position_direction_change(self, mock_random, mock_time):
        """Test case for when the alien is not at the edge of the screen."""
        self.alien_movement.direction_change_delay = 0
        self.alien_movement.direction = 1
        self.alien.check_edges = MagicMock(return_value=False)

        self.alien_movement.update_horizontal_position()

        self.assertEqual(self.alien_movement.direction, -1)
        self.assertEqual(
            self.alien_movement.last_direction_change, mock_time.return_value
        )
        self.assertEqual(
            self.alien_movement.direction_change_delay, mock_random.return_value
        )

    @patch("pygame.time.get_ticks", return_value=10000)
    @patch("random.randint", return_value=5)
    def test_update_horizontal_position_edge_true(self, mock_random, mock_time):
        """Test case for when the alien is at the edge of the screen."""
        self.alien_movement.direction = 1
        self.alien.check_edges = MagicMock(return_value=True)

        self.alien_movement.update_horizontal_position()

        self.assertEqual(self.alien_movement.direction, 1)
        self.assertEqual(
            self.alien_movement.last_direction_change, mock_time.return_value
        )
        self.assertEqual(
            self.alien_movement.direction_change_delay, mock_random.return_value
        )

    @patch("pygame.time.get_ticks", return_value=3000)
    def test_update_vertical_position(self, _):
        """Test the update vertical position method."""
        self.alien_movement.sins = {
            "time_offset": 1 * math.pi,
            "amplitude": 12,
            "frequency": 0.003,
        }
        self.alien.rect.y = -2

        self.alien_movement.update_vertical_position()

        self.assertEqual(self.alien.rect.y, 3)


if __name__ == "__main__":
    unittest.main()
