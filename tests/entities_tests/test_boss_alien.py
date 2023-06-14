"""
This module tests the BossAlien class that is used
to create bosses in the game.
"""


import unittest
from unittest.mock import MagicMock

from pygame import Surface
from src.game_logic.game_settings import Settings
from src.entities.aliens import BossAlien


class TestBossAlien(unittest.TestCase):
    """Test cases for BossAlien."""
    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.settings = Settings()
        self.game.screen = Surface((800, 600))
        self.game.settings = self.settings
        self.boss_alien = BossAlien(self.game)

    def test_init(self):
        """Test the initialization of the boss alien."""
        self.assertIsNotNone(self.boss_alien.screen)
        self.assertIsNotNone(self.boss_alien.settings)
        self.assertIsNotNone(self.boss_alien.image)
        self.assertIsNotNone(self.boss_alien.motion)
        self.assertIsNotNone(self.boss_alien.destroy)

    def test__update_image(self):
        """Test the update of the image."""
        self.boss_alien.settings.game_modes.boss_rush = True
        self.game.stats.level = 2
        self.boss_alien._update_image(self.game)
        self.assertEqual(self.boss_alien.image, self.boss_alien.boss_images["boss2"])

        self.boss_alien.settings.game_modes.boss_rush = False
        self.game.stats.level = 15
        self.boss_alien._update_image(self.game)
        self.assertEqual(self.boss_alien.image, self.boss_alien.boss_images["normal15"])

    def test_check_edges(self):
        """Test the check_edges method."""
        self.boss_alien.rect.right = self.game.screen.get_rect().right
        self.assertTrue(self.boss_alien.check_edges())
        self.boss_alien.rect.right = 10
        self.boss_alien.rect.left = 10
        self.assertFalse(self.boss_alien.check_edges())

    def test_freeze(self):
        """Test the freeze method."""
        self.assertFalse(self.boss_alien.frozen_state)
        self.assertEqual(self.boss_alien.frozen_start_time, 0)

        self.boss_alien.freeze()

        self.assertTrue(self.boss_alien.frozen_state)
        self.assertNotEqual(self.boss_alien.frozen_start_time, 0)

    def test_upgrade(self):
        """Teste the upgrade method."""
        initial_boss_hp = self.boss_alien.settings.boss_hp

        self.boss_alien.upgrade()

        self.assertEqual(
            self.boss_alien.settings.boss_hp,
            initial_boss_hp + 15
        )

    def test_update_movement(self):
        """Teste the update movement of the boss alien."""
        self.boss_alien.frozen_state = False
        self.boss_alien.settings.alien_speed = 2.0
        self.boss_alien.motion.direction = 1
        self.boss_alien.x_pos = 0.0

        self.boss_alien.update()

        self.assertEqual(self.boss_alien.x_pos, 2.0)
        self.assertEqual(self.boss_alien.rect.x, 2)

    def test_destroy_alien(self):
        """Teste the destroy method."""
        self.boss_alien.is_alive = True
        self.boss_alien.destroy.update_destroy_animation = MagicMock()
        self.boss_alien.destroy.draw_animation = MagicMock()

        self.boss_alien.destroy_alien()

        self.assertFalse(self.boss_alien.is_alive)
        self.boss_alien.destroy.update_destroy_animation.assert_called_once()
        self.boss_alien.destroy.draw_animation.assert_called_once()

    def test_draw(self):
        """Test the drawing of the boss alien."""
        screen = MagicMock()
        self.boss_alien.screen = screen
        self.boss_alien.draw()
        screen.blit.assert_called_once_with(self.boss_alien.image, self.boss_alien.rect)


if __name__ == "__main__":
    unittest.main()
