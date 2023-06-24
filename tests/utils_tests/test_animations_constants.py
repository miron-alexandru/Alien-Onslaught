"""
This module tests the animations constants (frames used for animations)
that are present in the game.
"""

import unittest

from src.utils.animation_constants import (
    destroy_frames,
    ship_images,
    warp_frames,
    shield_frames,
    immune_frames,
    explosion_frames,
    asteroid_frames,
    empower_frames,
    missile_frames,
    missile_ex_frames,
    alien_immune_frames,
    laser_frames,
)


class AnimationConstantsTests(unittest.TestCase):
    """
    Test case for the 'animation_constants' module.
    """

    def test_destroy_frames(self):
        """
        Test the destroy_frames constant.
        """
        self.assertIsInstance(
            destroy_frames, list, "Failed: destroy_frames is not an instance of list"
        )
        self.assertEqual(
            len(destroy_frames),
            15,
            "Failed: Number of frames in destroy_frames is not equal to 15",
        )

    def test_ship_images(self):
        """
        Test the ship_images constant.
        """
        self.assertIsInstance(
            ship_images, list, "Failed: ship_images is not an instance of list"
        )
        self.assertEqual(
            len(ship_images),
            6,
            "Failed: Number of frames in ship_images is not equal to 6",
        )

    def test_warp_frames(self):
        """
        Test the warp_frames constant.
        """
        self.assertIsInstance(
            warp_frames, list, "Failed: warp_frames is not an instance of list"
        )
        self.assertEqual(
            len(warp_frames),
            9,
            "Failed: Number of frames in warp_frames is not equal to 9",
        )

    def test_shield_frames(self):
        """
        Test the shield_frames constant.
        """
        self.assertIsInstance(
            shield_frames, list, "Failed: shield_frames is not an instance of list"
        )
        self.assertEqual(
            len(shield_frames),
            11,
            "Failed: Number of frames in shield_frames is not equal to 11",
        )

    def test_immune_frames(self):
        """
        Test the immune_frames constant.
        """
        self.assertIsInstance(
            immune_frames, list, "Failed: immune_frames is not an instance of list"
        )
        self.assertEqual(
            len(immune_frames),
            11,
            "Failed: Number of frames in immune_frames is not equal to 11",
        )

    def test_explosion_frames(self):
        """
        Test the explosion_frames constant.
        """
        self.assertIsInstance(
            explosion_frames,
            list,
            "Failed: explosion_frames is not an instance of list",
        )
        self.assertEqual(
            len(explosion_frames),
            89,
            "Failed: Number of frames in explosion_frames is not equal to 89",
        )

    def test_asteroid_frames(self):
        """
        Test the asteroid_frames constant.
        """
        self.assertIsInstance(
            asteroid_frames, list, "Failed: asteroid_frames is not an instance of list"
        )
        self.assertEqual(
            len(asteroid_frames),
            120,
            "Failed: Number of frames in asteroid_frames is not equal to 120",
        )

    def test_empower_frames(self):
        """
        Test the empower_frames constant.
        """
        self.assertIsInstance(
            empower_frames, list, "Failed: empower_frames is not an instance of list"
        )
        self.assertEqual(
            len(empower_frames),
            6,
            "Failed: Number of frames in empower_frames is not equal to 6",
        )

    def test_missile_frames(self):
        """
        Test the missile_frames constant.
        """
        self.assertIsInstance(
            missile_frames, list, "Failed: missile_frames is not an instance of list"
        )
        self.assertEqual(
            len(missile_frames),
            9,
            "Failed: Number of frames in missile_frames is not equal to 9",
        )

    def test_missile_ex_frames(self):
        """
        Test the missile_ex_frames constant.
        """
        self.assertIsInstance(
            missile_ex_frames,
            list,
            "Failed: missile_ex_frames is not an instance of list",
        )
        self.assertEqual(
            len(missile_ex_frames),
            9,
            "Failed: Number of frames in missile_ex_frames is not equal to 9",
        )

    def test_alien_immune_frames(self):
        """
        Test the alien_immune_frames constant.
        """
        self.assertIsInstance(
            alien_immune_frames,
            list,
            "Failed: alien_immune_frames is not an instance of list",
        )
        self.assertEqual(
            len(alien_immune_frames),
            20,
            "Failed: Number of frames in alien_immune_frames is not equal to 20",
        )

    def test_laser_frames(self):
        """
        Test the laser_frames constant.
        """
        self.assertIsInstance(
            laser_frames, list, "Failed: laser_frames is not an instance of list"
        )
        self.assertEqual(
            len(laser_frames),
            9,
            "Failed: Number of frames in laser_frames is not equal to 9",
        )


if __name__ == "__main__":
    unittest.main()
