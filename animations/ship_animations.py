"""The Animations class in this module manages the animations for the ships"""

from utils.game_utils import load_frames


class Animations:
    """A class to manage all of the animations for the ships"""
    def __init__(self, ship):
        self.ship = ship
        self.image = None

        # Initialize ship images
        self.ship_images = []
        load_frames('ships/ship{}.png', 6, self.ship_images, start=1)

        # Initialize warp frames
        self.warp_frames = []
        load_frames('warp/warp_{}.png', 9, self.warp_frames)

        self.warp_index = 0
        self.warp_delay = 5
        self.warp_counter = 0

        # Initialize shield frames
        self.shield_frames = []
        load_frames('shield/shield-0{}.png', 11, self.shield_frames)

        self.current_shield_frame = 0
        self.shield_image = self.shield_frames[self.current_shield_frame]
        self.shield_rect = self.shield_image.get_rect()

        # Initialize explosion frames
        self.explosion_frames = []
        load_frames('explosionn/explosion1_{:04d}.png', 89, self.explosion_frames, start=2)

        self.current_explosion_frame = 0
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        self.explosion_rect = self.explosion_image.get_rect()


    def update_warp_animation(self, ship_img):
        """Update the animation for the ship's warp effect.
        ship_img (int): The index of the ship image to display
        when the warp effect is finished."""
        self.warp_counter += 1
        if self.warp_counter >= self.warp_delay:
            self.warp_index += 1
            if self.warp_index >= len(self.warp_frames):
                self.ship.state['warping'] = False
                self.warp_index = 0
                self.image = self.ship_images[ship_img]
            else:
                self.image = self.warp_frames[self.warp_index]
            self.warp_counter = 0

    def update_shield_animation(self):
        """Update the animation for the ship's shield effect."""
        self.current_shield_frame = (
            (self.current_shield_frame + 1) % len(self.shield_frames)
        )
        self.shield_image = self.shield_frames[self.current_shield_frame]
        self.shield_rect.center = self.ship.rect.center

    def update_explosion_animation(self):
        """Update the animation for the ship's explosion effect."""
        self.current_explosion_frame = (
            (self.current_explosion_frame + 1) % len(self.explosion_frames)
        )
        self.explosion_image = self.explosion_frames[self.current_explosion_frame]
        if self.current_explosion_frame == 0:
            self.ship.state['exploding'] = False
