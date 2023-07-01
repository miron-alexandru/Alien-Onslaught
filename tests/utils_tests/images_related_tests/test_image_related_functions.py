"""
This module tests various functions from the game_utils modules
that are related to images, loading images or creating dictionary of images.
"""

import os
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

import pygame

from src.utils.game_utils import (
    draw_image,
    load_alien_bullets,
    load_alien_images,
    load_boss_bullets,
    load_boss_images,
    load_button_imgs,
    load_controls_image,
    load_images,
    load_single_image,
    resize_image,
)

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


# Define test image paths
TEST_IMAGE_PATH = os.path.join(BASE_PATH, "test_image.png")
TEST_ALIEN_IMAGE_PATH = os.path.join(BASE_PATH, "aliens/test_alien_0.png")
TEST_BUTTON_IMAGE_PATH = os.path.join(BASE_PATH, "test_button.png")


class ImageLoaderTest(unittest.TestCase):
    """Test cases for image related functions from the game_utils module."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary image files for testing
        pygame.image.save(pygame.Surface((100, 100)), TEST_IMAGE_PATH)
        pygame.image.save(pygame.Surface((100, 100)), TEST_ALIEN_IMAGE_PATH)
        pygame.image.save(pygame.Surface((100, 100)), TEST_BUTTON_IMAGE_PATH)

        self.test_alien_image_paths = []

        for i in range(6):
            alien_image_path = os.path.join(
                os.path.dirname(__file__), f"aliens/test_alien_{i+1}.png"
            )
            pygame.image.save(pygame.Surface((100, 100)), alien_image_path)
            self.test_alien_image_paths.append(alien_image_path)

    def tearDown(self):
        # Remove the temporary image files
        os.remove(TEST_IMAGE_PATH)
        os.remove(TEST_ALIEN_IMAGE_PATH)
        os.remove(TEST_BUTTON_IMAGE_PATH)

        for alien_image_path in self.test_alien_image_paths:
            os.remove(alien_image_path)

    def test_load_single_image(self):
        """Test loading a single image."""
        relative_path = os.path.join(BASE_PATH, "test_image.png")

        loaded_image = load_single_image(relative_path)

        # Assert that the loaded image is not None
        self.assertIsNotNone(loaded_image)
        self.assertIsInstance(loaded_image, pygame.Surface)

    @patch("src.utils.game_utils.BASE_PATH", BASE_PATH)
    def test_load_images(self):
        """Test loading multiple images."""
        image_dict = {"alien": "aliens/test_alien_0.png", "button": "test_button.png"}

        loaded_images = load_images(image_dict)

        # Assert that the loaded images are not None
        self.assertIsNotNone(loaded_images)
        self.assertIn("alien", loaded_images)
        self.assertIn("button", loaded_images)

    @patch("src.utils.game_utils.BASE_PATH", BASE_PATH)
    def test_load_alien_images(self):
        """Test loading alien images."""
        alien_prefix = "test_alien"

        loaded_frames = load_alien_images(alien_prefix)

        # Assert that the loaded frames are not None and contain 6 frames
        self.assertIsNotNone(loaded_frames)
        self.assertEqual(len(loaded_frames), 6)

    def test_resize_image(self):
        """Test the resize of an image."""
        image = pygame.Surface((100, 100))

        with mock.patch("pygame.display.get_surface") as mock_get_surface:
            mock_surface = pygame.Surface((800, 600))
            mock_get_surface.return_value = mock_surface

            resized_image = resize_image(image)

            # Assert that the resized image is not None
            self.assertIsNotNone(resized_image)

    def test_load_button_imgs(self):
        """Test loading the button images."""
        button_names = ["test_button"]

        button_images = load_button_imgs(button_names)

        # Assert that the loaded button images are not None and contain the test button
        self.assertIsInstance(button_images, dict)
        self.assertIn("test_button", button_images)

    def test_load_controls_image(self):
        """Test loading the controls image."""
        image_surface = pygame.Surface((100, 100))
        position = {"left": 10, "top": 20}

        loaded_image, rect = load_controls_image(image_surface, position)

        # Assert that the loaded image and rect are not None
        self.assertIsInstance(loaded_image, pygame.Surface)
        self.assertIsInstance(rect, pygame.Rect)

    def test_load_boss_images(self):
        """Test loading the boss images."""
        boss_images = load_boss_images()

        # Assert that the loaded boss images are not None and contain boss names
        self.assertIsInstance(boss_images, dict)
        self.assertIn("boss1", boss_images)
        self.assertIn("boss10", boss_images)

    def test_load_alien_bullets(self):
        """Test loading the alien bullets."""
        alien_bullets = load_alien_bullets()

        # Assert that the loaded alien bullets are not None and contain bullet names
        self.assertIsInstance(alien_bullets, dict)
        self.assertIn("alien_bullet1", alien_bullets)
        self.assertIn("alien_bullet5", alien_bullets)

    def test_load_boss_bullets(self):
        """Test loading the boss bullets."""
        boss_bullets = load_boss_bullets()

        # Assert that the loaded boss bullets are not None and contain bullet names
        self.assertIsInstance(boss_bullets, dict)
        self.assertIn("boss_bullet1", boss_bullets)
        self.assertIn("boss_bullet8", boss_bullets)

    def test_draw_image(self):
        """Test drawing an image."""
        screen = MagicMock(spec=pygame.Surface)
        image = MagicMock(spec=pygame.Surface)
        rect = pygame.Rect(0, 0, 50, 50)

        draw_image(screen, image, rect)

        screen.blit.assert_called_once_with(image, rect)


if __name__ == "__main__":
    unittest.main()
