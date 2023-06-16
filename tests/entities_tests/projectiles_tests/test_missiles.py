"""
This module tests the Missile class which is used to create
player missiles in the game.
"""

import unittest
from unittest.mock import MagicMock
import pygame
from src.entities.projectiles import Missile
from src.game_logic.game_settings import Settings


class TestMissile(unittest.TestCase):
    """Test cases for the Missile class."""

    def setUp(self):
        """Set up test environment."""
        self.screen = MagicMock(spec=pygame.Surface)
        self.settings = Settings()
        self.game = MagicMock()
        self.game.screen = self.screen
        self.game.settings = self.settings
        self.ship = MagicMock()
        self.missile = Missile(self.game, self.ship)

    def test_update_missile_not_destroyed(self):
        """Test the update of the missile while not destroyed."""
        initial_frame_counter = self.missile.frame_counter
        initial_current_frame = self.missile.current_frame
        initial_x_pos = self.missile.x_pos
        initial_y_pos = self.missile.y_pos

        self.missile.frame_counter = self.missile.frame_update_rate - 1

        self.missile.update()

        expected_current_frame = (initial_current_frame + 1) % len(self.missile.frames)
        expected_y_pos = initial_y_pos - self.missile.settings.missiles_speed

        self.assertEqual(self.missile.frame_counter, initial_frame_counter)
        self.assertEqual(self.missile.current_frame, expected_current_frame)
        self.assertEqual(self.missile.x_pos, initial_x_pos)
        self.assertEqual(self.missile.y_pos, expected_y_pos)

    def test_update_missile_destroyed(self):
        """Test the update of the missile while destroyed."""
        self.missile.is_destroyed = True
        self.missile.kill = MagicMock()

        self.missile.destroy_delay = -1
        initial_destroy_delay = self.missile.destroy_delay

        self.missile.update()

        self.assertEqual(self.missile.destroy_delay, initial_destroy_delay)

        self.missile.kill.assert_called_once()

    def test_draw_missile_not_destroyed(self):
        """Test the drawing of the missile while not destroyed."""
        initial_blit_calls = self.screen.blit.call_count

        self.missile.draw()

        self.assertEqual(self.screen.blit.call_count, initial_blit_calls + 1)

    def test_draw_missile_destroyed(self):
        """Test the drawing of the missile while destroyed."""
        self.missile.is_destroyed = True
        self.missile.destroy_anim.draw_explosion = (
            MagicMock()
        )  # Mocking the draw_explosion function
        initial_explosion_calls = self.missile.destroy_anim.draw_explosion.call_count

        self.missile.draw()

        self.missile.destroy_anim.draw_explosion.assert_called_once()  # Checking if draw_explosion was called once
        self.assertEqual(
            self.missile.destroy_anim.draw_explosion.call_count,
            initial_explosion_calls + 1,
        )

    def test_explode(self):
        """Test the explode method."""
        self.missile.explode()

        self.assertTrue(self.missile.is_destroyed)

    def test_set_missile_frames_cosmic_conflict(self):
        """Test setting the frames for cosmic conflict."""
        self.settings.game_modes.cosmic_conflict = True
        self.missile.ship = self.game.thunderbird_ship
        initial_image = self.missile.image

        self.missile.set_missile_frames()

        self.assertNotEqual(self.missile.image, initial_image)

    def test_set_missile_frames_not_cosmic_conflicts(self):
        """Test the setting of the frames for missiles in other game modes."""
        self.settings.game_modes.cosmic_conflict = False
        initial_image = self.missile.image

        self.missile.set_missile_frames()

        self.assertEqual(self.missile.image, initial_image)


if __name__ == "__main__":
    unittest.main()
