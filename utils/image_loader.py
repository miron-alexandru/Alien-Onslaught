"""This module provides functions to load images for aliens and bullets in the game.
Functions:
- load_boss_images(): Loads and returns a dictionary of boss alien images
with their respective names as keys.
- load_alien_bullets(): Loads and returns a dictionary of alien bullet images
with their respective names as keys.
"""

import pygame
from .constants import BOSS_RUSH, ALIEN_BULLETS_IMG

def load_boss_images():
    """Loads and returns a dict of boss images"""
    return {
        alien_name: pygame.image.load(alien_image_path)
        for alien_name, alien_image_path in BOSS_RUSH.items()
    }

def load_alien_bullets():
    """Loads and returns a dict of alien bullet images."""
    return {
        bullet_name: pygame.image.load(bullet_image_path)
        for bullet_name, bullet_image_path in ALIEN_BULLETS_IMG.items()
    }
