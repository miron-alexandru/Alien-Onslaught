"""
The 'entities_animations' module provides classes for managing animations for
different entities in the game.

Classes:
- DestroyAnim: Manages the animation for an entity getting destroyed.
- MissileEx: Manages the explosion effect for missiles.
- Immune: Manages the immune animation for the aliens.
"""

from src.utils.animation_constants import (
    destroy_frames,
    missile_ex_frames,
    alien_immune_frames,
)


class DestroyAnim:
    """Class that manages the animation for an entity destroyed."""

    def __init__(self, entity):
        self.entity = entity
        self.image = None
        self.screen = entity.screen

        self.destroy_frames = destroy_frames
        self.current_destroy_frame = 0
        self.destroy_image = self.destroy_frames[self.current_destroy_frame]
        self.destroy_rect = self.destroy_image.get_rect()

    def update_destroy_animation(self):
        """Update the animation for the destruction the entity.
        Updates the current frame of the animation, centered on the position of the entity
        """
        self.current_destroy_frame = (self.current_destroy_frame + 1) % len(
            self.destroy_frames
        )
        self.destroy_image = self.destroy_frames[self.current_destroy_frame]
        self.destroy_rect.center = self.entity.rect.center

    def draw_animation(self):
        """Draws the animation on screen."""
        self.screen.blit(self.destroy_image, self.destroy_rect)


class MissileEx:
    """The MissileEx class manages the explosion effect for the missiles."""

    def __init__(self, missile):
        self.missile = missile
        self.screen = missile.screen

        self.ex_frames = missile_ex_frames
        self.current_frame = 0
        self.ex_image = self.ex_frames[self.current_frame]
        self.ex_rect = self.ex_frames[0].get_rect(center=self.missile.rect.center)

        self.frame_update_rate = 5
        self.frame_counter = 0

    def update_animation(self):
        """Update and center the animation."""
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.ex_frames)
            self.ex_image = self.ex_frames[self.current_frame]
            self.frame_counter = 0
        self.ex_rect.center = self.missile.rect.center

    def draw_explosion(self):
        """Draw the explosin on the screen."""
        self.screen.blit(self.ex_image, self.ex_rect)


class Immune:
    """The Immune class manages the Immune animation for the aliens."""

    def __init__(self, alien):
        self.alien = alien
        self.screen = alien.screen
        self.boss = False

        self.immune_frames = alien_immune_frames
        self.current_immune_frame = 0
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()

    def update_immune_anim(self):
        """Update the animation for an alien being immune."""
        self.current_immune_frame = (self.current_immune_frame + 1) % len(
            self.immune_frames
        )
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect.center = self.alien.rect.center

    def draw_immune_anim(self):
        """Draw the immune animation."""
        self.screen.blit(self.immune_image, self.immune_rect)
