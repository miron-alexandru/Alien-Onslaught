"""The Animations class in this module manages the animations for the ships"""

import pygame
from utils.frames import (
    ship_images,
    warp_frames,
    shield_frames,
    immune_frames,
    explosion_frames,
    empower_frames,
)


class Animations:
    """A class to manage all of the animations for the ships"""
    def __init__(self, ship):
        self.ship = ship
        self.image = None

        # Initialize ship images
        self.ship_images = ship_images

        # Initialize warp frames
        self.warp_frames = warp_frames

        self.warp_index = 0
        self.warp_delay = 5
        self.warp_counter = 0

        # Initialize shield frames
        self.shield_frames = shield_frames

        self.current_shield_frame = 0
        self.shield_image = self.shield_frames[self.current_shield_frame]
        self.shield_rect = self.shield_image.get_rect()

        # Initialize immune frames
        self.immune_frames = immune_frames

        self.current_immune_frame = 0
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()

        # Initialize explosion frames
        self.explosion_frames = explosion_frames

        self.current_explosion_frame = 0
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()

        # Empower
        self.empower_frames = empower_frames

        self.empower_timer = 0
        self.empower_delay = 2

        self.current_empower_frame = 0
        self.empower_image = self.empower_frames[self.current_empower_frame]
        self.empower_rect = self.empower_image.get_rect()

    def change_ship_size(self, scale_factor):
        """Change the ship size based on the scale_factor."""
        self.ship.image = pygame.transform.smoothscale(self.ship.image,
                                                (int(self.ship.image.get_width() * scale_factor),
                                                int(self.ship.image.get_height() * scale_factor)))
        self.ship.rect = self.ship.image.get_rect()
        self.ship_images = [pygame.transform.scale(ship, (int(ship.get_width() * scale_factor),
                                    int(ship.get_height() * scale_factor))) for ship in ship_images]

        self.immune_frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor),
                                int(frame.get_height() * scale_factor))) for frame in immune_frames]
        self.immune_image = self.immune_frames[self.current_immune_frame]
        self.immune_rect = self.immune_image.get_rect()

        self.explosion_frames = [pygame.transform.scale(exp, (int(exp.get_width() * scale_factor),
                            int(exp.get_height() * scale_factor))) for exp in explosion_frames]
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()

        self.empower_frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor),
                            int(frame.get_height() * scale_factor))) for frame in empower_frames]
        self.empower_image = self.empower_frames[self.current_empower_frame]
        self.empower_rect = self.empower_image.get_rect()


    def update_warp_animation(self):
        """Update the animation for the ship's warp effect.
        ship_img (int): The index of the ship image to display
        when the warp effect is finished."""
        self.warp_counter += 1
        if self.warp_counter >= self.warp_delay:
            self.warp_index += 1
            if self.warp_index >= len(self.warp_frames):
                self.ship.state.warping = False
                self.warp_index = 0
            else:
                self.image = self.warp_frames[self.warp_index]
                self.warp_counter = 0

    def update_animation(self, animation_type):
        """Update the animation for the specified type."""
        if animation_type == "shield":
            self.current_shield_frame = (self.current_shield_frame + 1) % len(self.shield_frames)
            self.shield_image = self.shield_frames[self.current_shield_frame]
            self.shield_rect.center = self.ship.rect.center
        elif animation_type == "immune":
            self.current_immune_frame = (self.current_immune_frame + 1) % len(self.immune_frames)
            self.immune_image = self.immune_frames[self.current_immune_frame]
            self.immune_rect.center = self.ship.rect.center
        elif animation_type == "empower":
            self.empower_timer += 1
            if self.empower_timer >= self.empower_delay:
                self.empower_timer = 0
                self.current_empower_frame = (
                    (self.current_empower_frame + 1) % len(self.empower_frames))
                self.empower_image = self.empower_frames[self.current_empower_frame]
                self.empower_rect.center = self.ship.rect.center
                if self.current_empower_frame == 0:  # animation played once
                    self.ship.state.empowered = False

    def update_explosion_animation(self):
        """Update the animation for the ship's explosion effect."""
        self.current_explosion_frame = (
            (self.current_explosion_frame + 1) % len(self.explosion_frames)
        )
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        if self.current_explosion_frame == 0:
            self.ship.state.exploding = False
