"""
The 'ship_animations' module provides the Animations class for managing
the animations of ships in the game. The class provides methods for creating,
updating, and rendering ship animations.
"""

from src.utils.game_utils import scale_image

from src.utils.animation_constants import (
    ship_images,
    warp_frames,
    shield_frames,
    immune_frames,
    explosion_frames,
    empower_frames,
)


class Animations:
    """A class to manage all of the animations for the ships."""

    def __init__(self, ship):
        self.ship = ship
        self.image = None

        self.ship_images = ship_images

        self.warp_frames = warp_frames
        self.warp_index = 0
        self.warp_delay = 5
        self.warp_counter = 0

        self.shield_frames = shield_frames
        self.current_shield_frame = 0
        self.shield_image = self.shield_frames[self.current_shield_frame]
        self.shield_rect = self.shield_image.get_rect()

        self.immune_frames = immune_frames
        self.current_immune_frame = 0
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()

        self.explosion_frames = explosion_frames
        self.current_explosion_frame = 0
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()

        self.empower_frames = empower_frames
        self.empower_timer = 0
        self.empower_delay = 2
        self.current_empower_frame = 0
        self.empower_image = self.empower_frames[self.current_empower_frame]
        self.empower_rect = self.empower_image.get_rect()

    def change_ship_size(self, scale_factor):
        """Change the ship image and animation frames based on the scale factor."""
        self.ship.image = scale_image(self.ship.image, scale_factor)
        self.ship.rect = self.ship.image.get_rect()

        self.ship_images = [
            scale_image(ship, scale_factor) for ship in self.ship_images
        ]
        self.immune_frames = [
            scale_image(frame, scale_factor) for frame in self.immune_frames
        ]
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()
        self.shield_frames = [
            scale_image(frame, scale_factor) for frame in self.shield_frames
        ]
        self.shield_image = self.shield_frames[self.current_immune_frame]
        self.shield_rect = self.shield_image.get_rect()
        self.explosion_frames = [
            scale_image(exp, scale_factor) for exp in self.explosion_frames
        ]
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()
        self.empower_frames = [
            scale_image(frame, scale_factor) for frame in self.empower_frames
        ]
        self.empower_image = self.empower_frames[self.current_empower_frame]
        self.empower_rect = self.empower_image.get_rect()

    def reset_size(self):
        """Reset all animations frames and ship images to their original size."""
        self.ship_images = ship_images

        self.immune_frames = immune_frames
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()

        self.explosion_frames = explosion_frames
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()

        self.empower_frames = empower_frames
        self.empower_image = self.empower_frames[self.current_empower_frame]
        self.empower_rect = self.empower_image.get_rect()

        self.shield_frames = shield_frames
        self.shield_image = self.shield_frames[self.current_immune_frame]
        self.shield_rect = self.shield_image.get_rect()

    def update_warp_animation(self):
        """Update the animation for the ship's warping state."""
        self.warp_counter += 1
        if self.warp_counter >= self.warp_delay:
            self.warp_index += 1
            if self.warp_index >= len(self.warp_frames):
                self.ship.state.warping = False
                self.warp_index = 0
            else:
                self.image = self.warp_frames[self.warp_index]
                self.warp_counter = 0

    def update_shield_animation(self):
        """Update shield animation for the ship's shielded state."""
        self.current_shield_frame = (self.current_shield_frame + 1) % len(
            self.shield_frames
        )
        self.shield_image = self.shield_frames[self.current_shield_frame]
        self.shield_rect.center = self.ship.rect.center

    def update_immune_animation(self):
        """Update immune animation for the ship's immune state."""
        self.current_immune_frame = (self.current_immune_frame + 1) % len(
            self.immune_frames
        )
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect.center = self.ship.rect.center

    def update_empower_animation(self):
        """Update empower animation for the ship's empowered state"""
        self.empower_timer += 1
        if self.empower_timer >= self.empower_delay:
            self.empower_timer = 0
            self.current_empower_frame = (self.current_empower_frame + 1) % len(
                self.empower_frames
            )
            self.empower_image = self.empower_frames[self.current_empower_frame]
            self.empower_rect.center = self.ship.rect.center
            if self.current_empower_frame == 0:
                self.ship.state.empowered = False

    def update_explosion_animation(self):
        """Update the animation for the ship's explosion effect."""
        self.current_explosion_frame = (self.current_explosion_frame + 1) % len(
            self.explosion_frames
        )
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        if self.current_explosion_frame == 0:
            self.ship.state.exploding = False
