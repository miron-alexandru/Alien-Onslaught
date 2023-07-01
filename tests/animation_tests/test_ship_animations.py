"""
This module tests the Animations class which is used to manage
ship animations in the game.
"""

import unittest
from unittest.mock import MagicMock

import pygame

from src.utils.animation_constants import (
    ship_images,
    warp_frames,
    shield_frames,
    immune_frames,
    explosion_frames,
    empower_frames,
)
from src.animations.ship_animations import Animations


class TestAnimations(unittest.TestCase):
    """Test cases for the Animations class."""

    def setUp(self):
        self.ship = MagicMock()
        self.ship.rect = pygame.Rect(0, 0, 100, 100)
        self.animations = Animations(self.ship)

    def test_init(self):
        """Test for the init method."""
        self.assertEqual(self.animations.ship, self.ship)
        self.assertIsNone(self.animations.image)
        self.assertEqual(self.animations.ship_images, ship_images)
        self.assertEqual(self.animations.warp_frames, warp_frames)
        self.assertEqual(self.animations.warp_index, 0)
        self.assertEqual(self.animations.warp_delay, 5)
        self.assertEqual(self.animations.warp_counter, 0)
        self.assertEqual(self.animations.shield_frames, shield_frames)
        self.assertEqual(self.animations.current_shield_frame, 0)
        self.assertEqual(self.animations.shield_image, shield_frames[0])
        self.assertEqual(self.animations.shield_rect, shield_frames[0].get_rect())
        self.assertEqual(self.animations.immune_frames, immune_frames)
        self.assertEqual(self.animations.current_immune_frame, 0)
        self.assertEqual(self.animations.immune_image, immune_frames[0])
        self.assertEqual(self.animations.immune_rect, immune_frames[0].get_rect())
        self.assertEqual(self.animations.explosion_frames, explosion_frames)
        self.assertEqual(self.animations.current_explosion_frame, 0)
        self.assertEqual(self.animations.explosion_image, explosion_frames[0])
        self.assertEqual(self.animations.explosion_rect, explosion_frames[0].get_rect())
        self.assertEqual(self.animations.empower_frames, empower_frames)
        self.assertEqual(self.animations.empower_timer, 0)
        self.assertEqual(self.animations.empower_delay, 2)
        self.assertEqual(self.animations.current_empower_frame, 0)
        self.assertEqual(self.animations.empower_image, empower_frames[0])
        self.assertEqual(self.animations.empower_rect, empower_frames[0].get_rect())

    def test_reset_size(self):
        """Test the reset size method."""
        self.animations.ship_images = ["image1", "image2", "image3"]
        self.animations.immune_frames = ["frame1", "frame2", "frame3"]
        self.animations.immune_image = "frame1"
        self.animations.immune_rect = MagicMock()
        self.animations.explosion_frames = ["frame4", "frame5"]
        self.animations.explosion_image = "frame4"
        self.animations.explosion_rect = MagicMock()
        self.animations.empower_frames = ["frame6", "frame7"]
        self.animations.empower_image = "frame6"
        self.animations.empower_rect = MagicMock()
        self.animations.shield_frames = ["frame8", "frame9"]
        self.animations.shield_image = "frame8"
        self.animations.shield_rect = MagicMock()

        # Reset the attributes
        self.animations.reset_size()

        self.assertEqual(self.animations.ship_images, ship_images)
        self.assertEqual(self.animations.immune_frames, immune_frames)
        self.assertEqual(self.animations.immune_image, immune_frames[0])
        self.assertEqual(self.animations.immune_rect, immune_frames[0].get_rect())
        self.assertEqual(self.animations.explosion_frames, explosion_frames)
        self.assertEqual(self.animations.explosion_image, explosion_frames[0])
        self.assertEqual(self.animations.explosion_rect, explosion_frames[0].get_rect())
        self.assertEqual(self.animations.empower_frames, empower_frames)
        self.assertEqual(self.animations.empower_image, empower_frames[0])
        self.assertEqual(self.animations.empower_rect, empower_frames[0].get_rect())
        self.assertEqual(self.animations.shield_frames, shield_frames)
        self.assertEqual(self.animations.shield_image, shield_frames[0])
        self.assertEqual(self.animations.shield_rect, shield_frames[0].get_rect())

    def test_change_ship_size(self):
        """Test the change ship size method."""

        scale_factor = 1.5

        # Save the original ship images and animation frames
        original_ship_images = self.animations.ship_images[:]
        original_immune_frames = self.animations.immune_frames[:]
        original_shield_frames = self.animations.shield_frames[:]
        original_explosion_frames = self.animations.explosion_frames[:]
        original_empower_frames = self.animations.empower_frames[:]

        # Mock the necessary objects and functions
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.get_rect.return_value = MagicMock()
        pygame.transform.smoothscale = MagicMock(return_value=mock_surface)

        self.animations.change_ship_size(scale_factor)

        # Verify that the ship images and animation frames have been modified
        self.assertNotEqual(original_ship_images, self.animations.ship_images)
        self.assertNotEqual(original_immune_frames, self.animations.immune_frames)
        self.assertNotEqual(original_shield_frames, self.animations.shield_frames)
        self.assertNotEqual(original_explosion_frames, self.animations.explosion_frames)
        self.assertNotEqual(original_empower_frames, self.animations.empower_frames)

        # Assert that the ship image and rect are updated correctly
        self.assertEqual(self.animations.ship.image, mock_surface)
        self.assertEqual(self.animations.ship.rect, mock_surface.get_rect.return_value)

        # Iterate over the ship images and animation frames, checking for equality with the mock surface
        for ship_image in self.animations.ship_images:
            self.assertEqual(ship_image, mock_surface)

        for immune_frame in self.animations.immune_frames:
            self.assertEqual(immune_frame, mock_surface)

        for shield_frame in self.animations.shield_frames:
            self.assertEqual(shield_frame, mock_surface)

        for explosion_frame in self.animations.explosion_frames:
            self.assertEqual(explosion_frame, mock_surface)

        for empower_frame in self.animations.empower_frames:
            self.assertEqual(empower_frame, mock_surface)

        # Verify that pygame.transform.smoothscale was called on all frames.

        total_frames = (
            len(self.animations.ship_images)
            + len(self.animations.immune_frames)
            + len(self.animations.shield_frames)
            + len(self.animations.explosion_frames)
            + len(self.animations.empower_frames)
        ) + 1

        self.assertEqual(pygame.transform.smoothscale.call_count, total_frames)

    def test_update_warp_animation(self):
        """Test the update of the warp animation."""
        self.ship.state.warping = True
        self.animations.warp_counter = self.animations.warp_delay

        self.animations.update_warp_animation()

        self.assertEqual(self.animations.warp_index, 1)
        self.assertEqual(self.animations.image, self.animations.warp_frames[1])
        self.assertEqual(self.animations.warp_counter, 0)

        # Test warp animation completed
        self.animations.warp_counter = self.animations.warp_delay
        self.animations.warp_index = len(self.animations.warp_frames) - 1

        self.animations.update_warp_animation()

        self.assertFalse(self.ship.state.warping)
        self.assertEqual(self.animations.warp_index, 0)
        self.assertEqual(self.animations.image, self.animations.warp_frames[1])

    def test_update_shield_animation(self):
        """Test the update of the shield animation."""
        initial_frame = self.animations.current_shield_frame

        self.animations.update_shield_animation()

        self.assertEqual(
            self.animations.current_shield_frame,
            (initial_frame + 1) % len(self.animations.shield_frames),
        )
        self.assertEqual(
            self.animations.shield_image,
            self.animations.shield_frames[self.animations.current_shield_frame],
        )
        self.assertEqual(self.animations.shield_rect.center, self.ship.rect.center)

    def test_update_immune_animation(self):
        """Test the update of the immune animation."""
        initial_frame = self.animations.current_immune_frame

        self.animations.update_immune_animation()

        self.assertEqual(
            self.animations.current_immune_frame,
            (initial_frame + 1) % len(self.animations.immune_frames),
        )
        self.assertEqual(
            self.animations.immune_image,
            self.animations.immune_frames[self.animations.current_immune_frame],
        )
        self.assertEqual(self.animations.immune_rect.center, self.ship.rect.center)

    def test_update_empower_animation(self):
        """Test the update of the empower animation."""
        initial_frame = self.animations.current_empower_frame

        self.ship.state.empowered = True
        self.animations.empower_timer = self.animations.empower_delay

        self.animations.update_empower_animation()

        self.assertEqual(
            self.animations.current_empower_frame,
            (initial_frame + 1) % len(self.animations.empower_frames),
        )
        self.assertEqual(
            self.animations.empower_image,
            self.animations.empower_frames[self.animations.current_empower_frame],
        )
        self.assertEqual(self.animations.empower_rect.center, self.ship.rect.center)

        # Test empower animation completed
        self.animations.empower_timer = self.animations.empower_delay
        self.animations.current_empower_frame = len(self.animations.empower_frames) - 1

        self.animations.update_empower_animation()

        self.assertEqual(self.animations.current_empower_frame, 0)
        self.assertEqual(
            self.animations.empower_image, self.animations.empower_frames[0]
        )
        self.assertFalse(self.ship.state.empowered)

    def test_update_explosion_animation(self):
        """Test the update of the explosion animation."""
        initial_frame = self.animations.current_explosion_frame

        self.animations.update_explosion_animation()

        self.assertEqual(
            self.animations.current_explosion_frame,
            (initial_frame + 1) % len(self.animations.explosion_frames),
        )
        self.assertEqual(
            self.animations.explosion_image,
            self.animations.explosion_frames[self.animations.current_explosion_frame],
        )

        # Test completed explosion animation.
        self.animations.current_explosion_frame = (
            len(self.animations.explosion_frames) - 1
        )

        self.animations.update_explosion_animation()

        self.assertEqual(self.animations.current_explosion_frame, 0)
        self.assertEqual(
            self.animations.explosion_image, self.animations.explosion_frames[0]
        )
        self.assertFalse(self.ship.state.exploding)


if __name__ == "__main__":
    unittest.main()
