"""
This module tests the Alien class that manages the aliens in the
game.
"""

import unittest
from unittest.mock import MagicMock, patch

import time
import random

import pygame

from src.entities.alien_entities.aliens import Alien


class TestAlien(unittest.TestCase):
    """Test cases for the Alien class."""

    def setUp(self):
        """Set up the test environment."""
        self.game = MagicMock()
        self.screen = MagicMock(spec=pygame.Surface)
        self.screen.get_rect.return_value = pygame.Rect(0, 0, 800, 600)
        self.game.screen = self.screen
        self.alien = Alien(self.game)

    def test_init(self):
        """Test the initialization of the Alien."""
        self.assertEqual(self.alien.aliens, self.game.aliens)
        self.assertEqual(self.alien.screen, self.game.screen)
        self.assertEqual(self.alien.settings, self.game.settings)
        self.assertEqual(self.alien.game_modes, self.game.settings.game_modes)
        self.assertEqual(self.alien.hit_count, 0)
        self.assertEqual(self.alien.last_bullet_time, 0)
        self.assertFalse(self.alien.immune_state)
        self.assertFalse(self.alien.frozen_state)
        self.assertEqual(self.alien.frozen_start_time, 0)
        self.assertEqual(self.alien.immune_start_time, 0)
        self.assertFalse(self.alien.is_baby)
        self.assertEqual(self.alien.baby_location, 0)
        self.assertIsNotNone(self.alien.motion)
        self.assertIsNotNone(self.alien.animation)
        self.assertIsNotNone(self.alien.destroy)
        self.assertIsNotNone(self.alien.immune)
        self.assertIsInstance(self.alien.image, pygame.Surface)

    def test_init_position(self):
        """Test the _init_position method."""
        self.alien._init_position()

        self.assertIsInstance(self.alien.rect, pygame.Rect)
        self.assertGreaterEqual(self.alien.rect.x, 0)
        self.assertEqual(self.alien.rect.y, self.alien.rect.height)
        self.assertEqual(self.alien.x_pos, float(self.alien.rect.x))

    def test_check_edges(self):
        """Test the check_edges method of the Alien."""
        # Test case: Alien at the right edge of the screen
        self.alien.rect.right = self.game.screen.get_rect().right

        self.assertTrue(self.alien.check_edges())

        # Test case: Alien at the left edge of the screen
        self.alien.rect.left = 0

        self.assertTrue(self.alien.check_edges())

        # Test case: Alien not at the edge of the screen
        self.alien.rect.right = 100
        self.alien.rect.left = 100

        self.assertFalse(self.alien.check_edges())

    def test_check_top_edges(self):
        """Test the check_top_edges method of the Alien."""
        # Test case: Alien at the top edge of the screen
        self.alien.rect.top = 0
        self.assertTrue(self.alien.check_top_edges())

        # Test case: Alien not at the top edge of the screen
        self.alien.rect.top = 10

        screen_rect = pygame.Rect(0, 0, 800, 600)
        self.alien.screen.get_rect.return_value = screen_rect

        self.assertFalse(self.alien.check_top_edges())

    def test_update(self):
        """Test the update method."""
        self.game.settings.alien_speed = 3
        self.game.settings.alien_direction = 1
        self.alien.motion.direction = 1
        self.game.settings.frozen_time = 4
        self.game.settings.alien_immune_time = 30

        initial_x_pos = self.alien.x_pos
        initial_image = self.alien.image.copy()
        initial_frozen_state = self.alien.frozen_state
        initial_immune_state = self.alien.immune_state

        # Test when the alien is not in the frozen state
        self.alien.update()

        # Verify position update
        self.assertAlmostEqual(
            self.alien.x_pos,
            initial_x_pos
            + self.alien.settings.alien_speed * self.alien.motion.direction,
        )
        self.assertEqual(self.alien.rect.x, self.alien.x_pos)

        # Verify animation update
        self.assertNotEqual(self.alien.image, initial_image)

        # Verify other state changes
        self.assertEqual(self.alien.frozen_state, initial_frozen_state)
        self.assertEqual(self.alien.immune_state, initial_immune_state)

        # Test when the alien is in the frozen state
        self.alien.frozen_state = True
        initial_time = time.time()
        self.alien.frozen_start_time = (
            initial_time - self.alien.settings.frozen_time - 1
        )

        self.alien.update()

        # Verify that the frozen state is deactivated after the specified frozen time
        self.assertEqual(self.alien.frozen_state, False)

        # Test when the alien is in the immune state
        self.alien.immune_state = True
        initial_time = time.time()
        self.alien.immune_start_time = (
            initial_time - self.alien.settings.alien_immune_time - 1
        )

        self.alien.update()

        # Verify that the immune state is deactivated after the specified immune time
        self.assertEqual(self.alien.immune_state, False)

    def test_destroy_alien(self):
        """Test the destroy_alien method."""
        self.alien.destroy = MagicMock()

        self.alien.destroy_alien()

        self.alien.destroy.update_destroy_animation.assert_called_once()
        self.alien.destroy.draw_animation.assert_called_once()

    def test_split_alien(self):
        """Test the split_alien method."""
        with patch("src.entities.alien_entities.aliens.Alien") as mock_alien:
            # Generate a random number of splits between 1 and 4
            actual_splits = random.randint(1, 4)

            with patch("random.randint") as mock_randint:
                mock_randint.return_value = actual_splits
                self.alien.split_alien()
                # Verify that the Alien class is called the expected number of times
                self.assertEqual(mock_alien.call_count, actual_splits)

    def test_upgrade(self):
        """Test the upgrade method."""
        self.alien.immune = MagicMock()

        self.alien.upgrade()

        self.assertTrue(self.alien.immune_state)
        self.assertEqual(self.alien.immune.immune_rect.center, self.alien.rect.center)
        self.assertNotEqual(self.alien.immune_start_time, 0)

    def test_freeze(self):
        """Test the freeze method."""
        self.alien.freeze()

        self.assertTrue(self.alien.frozen_state)
        self.assertNotEqual(self.alien.frozen_start_time, 0)

    def test_draw(self):
        """Test the draw method."""
        self.alien.draw()

        self.screen.blit.assert_called_once_with(self.alien.image, self.alien.rect)


if __name__ == "__main__":
    unittest.main()
