"""
This module tests the Missile class which is used to create
player missiles in the game.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.entities.projectiles.missile import Missile


class TestMissile(unittest.TestCase):
    """Test cases for the Missile class."""

    def setUp(self):
        """Set up test environment."""
        self.game = MagicMock()
        self.game.settings.game_modes.cosmic_conflict = False
        self.ship = MagicMock()
        self.missile = Missile(self.game, self.ship)

    def test_update_missile_not_destroyed(self):
        """Test the update of the missile while not destroyed."""
        self.game.settings.missiles_speed = 4
        initial_frame_counter = self.missile.frame_counter
        initial_current_frame = self.missile.current_frame
        initial_x_pos = self.missile.x_pos
        initial_y_pos = self.missile.y_pos

        expected_current_frame = (initial_current_frame + 1) % len(self.missile.frames)
        expected_y_pos = initial_y_pos - self.missile.settings.missiles_speed

        self.missile.frame_counter = self.missile.frame_update_rate - 1

        self.missile.update()

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
        self.missile.draw()

        self.game.screen.blit.assert_called_once_with(
            self.missile.image, self.missile.rect
        )

    def test_draw_missile_destroyed(self):
        """Test the drawing of the missile while destroyed."""
        self.missile.is_destroyed = True
        self.missile.destroy_anim.draw_explosion = MagicMock()

        self.missile.draw()

        self.missile.destroy_anim.draw_explosion.assert_called_once()

    def test_explode(self):
        """Test the explode method."""
        self.missile.explode()

        self.assertTrue(self.missile.is_destroyed)

    @patch("src.entities.projectiles.missile.pygame.transform.rotate")
    def test_set_missile_frames_cosmic_conflict(self, mock_rotate):
        """Test setting the frames for cosmic conflict."""
        self.game.settings.game_modes.cosmic_conflict = True
        self.missile.ship = self.game.thunderbird_ship
        initial_image = self.missile.image

        self.missile.set_missile_frames()

        self.assertNotEqual(self.missile.image, initial_image)
        mock_rotate.assert_called_once_with(
            self.missile.frames[self.missile.current_frame], -90
        )

    @patch("src.entities.projectiles.missile.pygame.transform.rotate")
    def test_set_missile_frames_not_cosmic_conflicts(self, mock_rotate):
        """Test the setting of the frames for missiles in other game modes."""
        initial_image = self.missile.image

        self.missile.set_missile_frames()

        self.assertEqual(self.missile.image, initial_image)
        mock_rotate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
