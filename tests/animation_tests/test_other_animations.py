"""
This module tests the DestroyAnim, MissileEx and Immune animations
that are present in the game.
"""

import copy
import unittest
from unittest.mock import Mock
import pygame

from src.animations.other_animations import DestroyAnim, MissileEx, Immune
from src.utils.animation_constants import destroy_frames, alien_immune_frames, missile_ex_frames


class DestroyAnimTests(unittest.TestCase):
    """Test cases for the DestroyAnim class."""

    def setUp(self):
        """Set up the test environment."""
        self.entity = pygame.sprite.Sprite()
        self.entity.rect = pygame.Rect(0, 0, 100, 100) # type: ignore
        self.entity.screen = pygame.Surface((800, 600)) # type: ignore

    def test_init(self):
        """Test the initialization of DestroyAnim."""
        destroy_anim = DestroyAnim(self.entity)
        self.assertEqual(destroy_anim.entity, self.entity)
        self.assertIsNone(destroy_anim.image)
        self.assertEqual(destroy_anim.screen, self.entity.screen) # type: ignore
        self.assertEqual(destroy_anim.destroy_frames, destroy_frames)
        self.assertEqual(destroy_anim.current_destroy_frame, 0)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[0])

    def test_update_destroy_animation(self):
        """Test the update of the destroy animation frames."""
        destroy_anim = DestroyAnim(self.entity)
        destroy_anim.current_destroy_frame = 0

        destroy_anim.update_destroy_animation()
        self.assertEqual(destroy_anim.current_destroy_frame, 1)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[1])
        self.assertEqual(destroy_anim.destroy_rect.center, self.entity.rect.center) # type: ignore

        # Test wrapping around to the first frame
        destroy_anim.current_destroy_frame = len(destroy_frames) - 1
        destroy_anim.update_destroy_animation()
        self.assertEqual(destroy_anim.current_destroy_frame, 0)
        self.assertEqual(destroy_anim.destroy_image, destroy_frames[0])
        self.assertEqual(destroy_anim.destroy_rect.center, self.entity.rect.center) # type: ignore

    def test_draw_animation(self):
        """Test the drawing of the destroy animation on the screen."""
        destroy_anim = DestroyAnim(self.entity)
        destroy_anim.screen = Mock()

        destroy_anim.draw_animation()
        destroy_anim.screen.blit.assert_called_once_with(destroy_anim.destroy_image, destroy_anim.destroy_rect)



class MissileExTests(unittest.TestCase):
    """Test cases for the MissileEx class."""

    def setUp(self):
        """Set up the test environment."""
        self.missile = pygame.sprite.Sprite()
        self.missile.rect = pygame.Rect(0, 0, 50, 50) # type: ignore
        self.missile.screen = pygame.Surface((800, 600)) # type: ignore

    def test_init(self):
        """Test the initialization of MissileEx."""
        missile_ex = MissileEx(self.missile)
        self.assertEqual(missile_ex.missile, self.missile)
        self.assertEqual(missile_ex.screen, self.missile.screen) # type: ignore
        self.assertEqual(missile_ex.ex_frames, missile_ex_frames)
        self.assertEqual(missile_ex.current_frame, 0)
        self.assertEqual(missile_ex.ex_image, missile_ex_frames[0])
        self.assertEqual(missile_ex.frame_update_rate, 5)
        self.assertEqual(missile_ex.frame_counter, 0)

    def test_update_animation(self):
        """Test the update of the explosion animation frames."""
        missile_ex = MissileEx(self.missile)
        missile_ex.current_frame = 0
        initial_frame = copy.copy(missile_ex.ex_image)

        missile_ex.update_animation()
        self.assertEqual(missile_ex.current_frame, 0)
        self.assertNotEqual(missile_ex.ex_image, initial_frame)
        self.assertEqual(missile_ex.ex_rect.center, self.missile.rect.center) # type: ignore

        missile_ex.current_frame = len(missile_ex_frames) - 1
        missile_ex.update_animation()
        self.assertEqual(missile_ex.current_frame, len(missile_ex_frames) - 1)
        self.assertNotEqual(missile_ex.ex_image, initial_frame)
        self.assertEqual(missile_ex.ex_rect.center, self.missile.rect.center) # type: ignore

    def test_draw_explosion(self):
        """Test the drawing of the explosion animation on the screen."""
        missile_ex = MissileEx(self.missile)
        missile_ex.screen = Mock()

        missile_ex.draw_explosion()
        missile_ex.screen.blit.assert_called_once_with(missile_ex.ex_image, missile_ex.ex_rect)


class ImmuneTests(unittest.TestCase):
    """Test cases for the Immune class."""

    def setUp(self):
        """Set up the test environment."""
        self.alien = pygame.sprite.Sprite()
        self.alien.rect = pygame.Rect(0, 0, 100, 100) # type: ignore
        self.alien.screen = pygame.Surface((800, 600)) # type: ignore

    def test_init(self):
        """Test the initialization of Immune."""
        immune = Immune(self.alien)
        self.assertEqual(immune.alien, self.alien)
        self.assertEqual(immune.screen, self.alien.screen) # type: ignore
        self.assertEqual(immune.immune_frames, alien_immune_frames)
        self.assertEqual(immune.current_immune_frame, 0)
        self.assertEqual(immune.immune_image, alien_immune_frames[0])

    def test_update_immune_anim(self):
        """Test the update of the immune animation frames."""
        immune = Immune(self.alien)
        immune.current_immune_frame = 0

        immune.update_immune_anim()
        self.assertEqual(immune.current_immune_frame, 1)
        self.assertEqual(immune.immune_image, alien_immune_frames[1])
        self.assertEqual(immune.immune_rect.center, self.alien.rect.center) # type: ignore

        # Test wrapping around to the first frame
        immune.current_immune_frame = len(alien_immune_frames) - 1
        immune.update_immune_anim()
        self.assertEqual(immune.current_immune_frame, 0)
        self.assertEqual(immune.immune_image, alien_immune_frames[0])
        self.assertEqual(immune.immune_rect.center, self.alien.rect.center) # type: ignore

    def test_draw_immune_anim(self):
        """Test the drawing of the immune animation on the screen."""
        immune = Immune(self.alien)
        immune.screen = Mock()

        immune.draw_immune_anim()
        immune.screen.blit.assert_called_once_with(immune.immune_image, immune.immune_rect)


if __name__ == '__main__':
    unittest.main()
