"""This is the animation module where other animations for different
parts of the game are located."""

from utils.frames import destroy_frames

class DestroyAnim:
    """Class that manages the animation for when an entity get's destroyed."""
    def __init__(self, entity):
        self.entity = entity
        self.image = None


        # Initialize frames
        self.destroy_frames = destroy_frames

        self.current_destroy_frame = 0
        self.destroy_image = self.destroy_frames[self.current_destroy_frame]
        self.destroy_rect = self.destroy_image.get_rect()

    def update_destroy_animation(self):
        """Update destroy animation"""
        self.current_destroy_frame = (self.current_destroy_frame + 1) % len(self.destroy_frames)
        self.destroy_image = self.destroy_frames[self.current_destroy_frame]
        self.destroy_rect.center = self.entity.rect.center
