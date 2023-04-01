"""This is the animation module where other animations for different
parts of the game are located."""

from utils.frames import destroy_frames, missile_ex_frames

class DestroyAnim:
    """Class that manages the animation for when an entity get's destroyed."""
    def __init__(self, entity):
        self.entity = entity
        self.image = None
        self.screen = entity.screen


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

    def draw_animation(self):
        """Draws the animation on screen."""
        self.screen.blit(self.destroy_image, self.destroy_rect)


class MissileEx:
    """The MissileEx class manages the explosion effect for the missiles"""
    def __init__(self, missile):
        super().__init__()
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
        """Draw the image on screen."""
        self.screen.blit(self.ex_image, self.ex_rect)
                    