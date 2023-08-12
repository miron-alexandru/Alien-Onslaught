"""
The 'aliens' module contains classes for creating aliens and boss
instances in the game.

Classes:
    - 'Alien': Class used to create normal aliens.
    - 'BossAlien': Class used to create bosses.
"""

import time
import random


from pygame.sprite import Sprite
from src.animations.entities_animations import DestroyAnim, Immune
from src.managers.alien_managers.aliens_behaviors import AlienMovement, AlienAnimation
from src.utils.game_utils import load_boss_images


class Alien(Sprite):
    """A class that represents an alien."""

    def __init__(self, game, baby_location=0, is_baby=False):
        """Initializes the Alien object and also creates instances of the
        AlienMovement, AlienAnimation, DestroyAnim, and Immune classes which manage the
        alien's movement, animation, destruction animation and immune state.
        """
        super().__init__()
        self.aliens = game.aliens
        self.screen = game.screen
        self.settings = game.settings
        self.game_modes = game.settings.game_modes
        self.stats = game.stats

        self.hit_count = 0
        self.last_bullet_time = 0
        self.immune_state = False
        self.frozen_state = False
        self.frozen_start_time = 0
        self.immune_start_time = 0
        self.is_baby = is_baby
        self.baby_location = baby_location

        self.motion = AlienMovement(self, game)
        self.animation = AlienAnimation(self, game)
        self._init_position()
        self.destroy = DestroyAnim(self)
        self.immune = Immune(self)
        self.image = self.animation.get_current_image()

    def _init_position(self):
        """Set the initial position of the alien."""
        self.rect = self.animation.image.get_rect()
        self.rect.x = (
            self.baby_location
            if self.is_baby
            else random.randint(0, self.settings.screen_width - self.rect.width)
        )
        self.rect.y = self.rect.height
        self.x_pos = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_top_edges(self):
        """Return True if alien is at the top of the screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.top <= screen_rect.top

    def update(self):
        """Updates the position, animation, and state of the alien."""
        if (
            self.frozen_state
            and time.time() - self.frozen_start_time > self.settings.frozen_time
        ):
            self.frozen_state = False

        if self.frozen_state:
            return

        self.x_pos += self.settings.alien_speed * self.motion.direction
        self.rect.x = round(self.x_pos)

        self.animation.update_animation()
        self.image = self.animation.get_current_image()

        self.motion.update_vertical_position()
        self.motion.update_horizontal_position()

        if self.immune_state:
            self.immune.draw_immune_anim()
            self.immune.update_immune_anim()

        if (
            self.immune_state
            and time.time() - self.immune_start_time > self.settings.alien_immune_time
        ):
            self.immune_state = False

    def destroy_alien(self):
        """Start the alien's destruction animation and draw it on the screen,
        and split the alien if necessary."""
        self.destroy.update_destroy_animation()
        self.destroy.draw_animation()

        if not self.game_modes.last_bullet and (
            not self.is_baby and random.random() <= 0.1
        ):
            self.split_alien()

    def split_alien(self):
        """Splits the alien into multiple smaller (baby) aliens."""
        num_splits = random.randint(1, 4)
        for _ in range(num_splits):
            baby_alien = Alien(self, baby_location=self.rect.x, is_baby=True)
            baby_alien.rect.y = self.rect.y
            baby_alien.animation.change_scale(0.5)
            self.aliens.add(baby_alien)

    def upgrade(self):
        """Set the alien's immune state to True."""
        self.immune_state = True
        self.immune.immune_rect.center = self.rect.center
        self.immune_start_time = time.time()

    def freeze(self):
        """Set's the alien's frozen state to True."""
        self.frozen_state = True
        self.frozen_start_time = time.time()

    def draw(self):
        """Draw the alien on screen."""
        self.screen.blit(self.image, self.rect)


class BossAlien(Sprite):
    """A class that represents bosses."""

    boss_images = load_boss_images()

    def __init__(self, game):
        """Initializes the BossAlien object and creates instances of AlienMovement
        and DestroyAnim classes to manage the movement and destruction animation.
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = self.boss_images["boss2"]
        self._update_image(game)

        self.last_bullet_time = 0
        self.hit_count = 0
        self.is_alive = True
        self.frozen_state = False
        self.frozen_start_time = 0
        self.immune_state = False
        self.last_hit_time = 0.0

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-30, 0)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height - self.image.get_height() + 50
        self.x_pos = float(self.rect.x)

        self.motion = AlienMovement(self, game)
        self.destroy = DestroyAnim(self)

    def _update_image(self, game):
        """Change the image for the specific boss."""
        if self.settings.game_modes.boss_rush:
            image_name = f"boss{game.stats.level}"
        else:
            image_name = f"normal{game.stats.level}"

        if image_name in self.boss_images:
            self.image = self.boss_images[image_name]

    def update(self):
        """Update position and movement."""
        if (
            self.frozen_state
            and time.time() - self.frozen_start_time > self.settings.frozen_time
        ):
            self.frozen_state = False

        if self.frozen_state:
            return

        self.x_pos += self.settings.alien_speed * self.motion.direction
        self.rect.x = round(self.x_pos)

        self.motion.update_horizontal_position()

    def check_edges(self):
        """Return True if boss is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def destroy_alien(self):
        """Set the is_alive attribute to False and display the destroy animation."""
        self.is_alive = False
        self.destroy.update_destroy_animation()
        self.destroy.draw_animation()

    def freeze(self):
        """Set's the alien's frozen state to True."""
        self.frozen_state = True
        self.frozen_start_time = time.time()

    def upgrade(self):
        """Increase boss HP."""
        self.settings.boss_hp += 15

    def draw(self):
        """Draw the alien on screen."""
        self.screen.blit(self.image, self.rect)
