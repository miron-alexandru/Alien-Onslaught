"""
The 'aliens' module contains classes for managing aliens and bosses in the game.

Classes:
    - 'Alien': A class that represents aliens in the game.
    - 'BossAlien': A class that represents alien bosses in the game.
    - 'AliensManager': A class that manages the creation, update and behavior of aliens and bosses.
    - 'AlienMovement': A class that manages the movement of a single alien.
    - 'AlienAnimation': This class manages the animation for normal aliens.
"""

import math
import random
import pygame

from pygame.sprite import Sprite
from animations.other_animations import DestroyAnim, Immune
from utils.constants import LEVEL_PREFIX
from utils.game_utils import load_alien_images, load_boss_images


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
        self.immune_start_time = 0
        self.is_baby = is_baby
        self.baby_location = baby_location

        self.motion = AlienMovement(self, game)
        self.animation = AlienAnimation(self, game)
        self._init_position()
        self.destroy = DestroyAnim(self)
        self.immune = Immune(self)
        self.image = self.animation.get_current_image()
        # self._init_position()

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
        """Updates the position, animation, and state of the alien.
        It also creates random movement for the alien.
        """
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
            and pygame.time.get_ticks() - self.immune_start_time
            > self.settings.alien_immune_time
        ):
            self.immune_state = False

    def destroy_alien(self):
        """Start the alien's destruction animation and draw it on the screen,
        and split the alien."""
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
        self.immune_start_time = pygame.time.get_ticks()


class BossAlien(Sprite):
    """A class to represent alien bosses in the game."""

    boss_images = load_boss_images()

    def __init__(self, game):
        """Initializes the BossAlien object, creates instances of AlienMovement
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
        self.immune_state = False

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-30, 0)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height - self.image.get_height() + 50
        self.x_pos = float(self.rect.x)

        self.motion = AlienMovement(self, game)
        self.destroy = DestroyAnim(self)

    def _update_image(self, game):
        """Change the image for specific boss fights."""
        if self.settings.game_modes.boss_rush:
            image_name = f"boss{game.stats.level}"
        else:
            image_name = f"normal{game.stats.level}"

        if image_name in self.boss_images:
            self.image = self.boss_images[image_name]

    def update(self):
        """Update position and movement."""
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

    def upgrade(self):
        """Increase boss HP."""
        self.settings.boss_hp += 15


class AliensManager:
    """The AliensManager class manages the following aspects of aliens and bosses:
    creation, update and the behavior when aliens are are edges of the screen."""

    def __init__(self, game, aliens, settings, screen):
        self.game = game
        self.aliens = aliens
        self.settings = settings
        self.screen = screen
        self.stats = game.stats

    def create_fleet(self, rows):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Calculate the starting y-coordinate for the first row of aliens
        start_y = 50

        # Create the full fleet of aliens.
        for row_number in range(rows):
            for alien_number in range(self.settings.aliens_num):
                # Create the alien and set its starting position above the top of the screen
                alien = Alien(self)
                alien.rect.x = alien_width + 2 * alien_width * alien_number
                alien.rect.y = start_y - (2 * alien_height * row_number)
                # Add the alien to the group of aliens
                self.aliens.add(alien)

    def create_boss_alien(self):
        """Create a boss alien and add it to the aliens group."""
        boss_alien = BossAlien(self)
        self.aliens.add(boss_alien)

    def update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change the direction of the fleet of aliens and move
        them down if they reach the screen's edge.
        Boss aliens do not move down.
        """
        for alien in self.aliens.sprites():
            if isinstance(alien, BossAlien):
                if alien.check_edges():
                    alien.motion.direction *= -1
                else:
                    alien.rect.x += self.settings.alien_speed * alien.motion.direction
            elif alien.check_edges():
                alien.motion.direction *= -1

            elif alien.check_top_edges():
                alien.rect.y += self.settings.alien_speed


class AlienMovement:
    """Manages the creation, update, and behavior
    of a fleet of aliens and bosses in a game.
    """

    def __init__(self, alien, game):
        self.alien = alien
        self.settings = game.settings

        self.direction = self.settings.alien_direction
        self.last_direction_change = pygame.time.get_ticks()
        self.direction_change_delay = 0

        self.sins = {
            "time_offset": random.uniform(0, 2 * math.pi),
            "amplitude": random.randint(1, 2),
            "frequency": random.uniform(0.001, 0.005),
        }

    def update_horizontal_position(self):
        """Update the horizontal position of the alien and
        create random movement.
        """
        now = pygame.time.get_ticks()
        if now - self.last_direction_change > self.direction_change_delay:
            # Check if alien is not near the edge of the screen
            if not self.alien.check_edges():
                self.direction *= -1
            self.last_direction_change = now
            # how often the direction changes
            self.direction_change_delay = random.randint(3000, 5000)  # miliseconds

    def update_vertical_position(self):
        """Update the vertical position of the alien and
        create random movement.
        """
        now = pygame.time.get_ticks()
        time = now + self.sins["time_offset"]
        self.alien.rect.y = round(
            self.alien.rect.y
            + self.sins["amplitude"] * math.sin(self.sins["frequency"] * time)
            + 0.1
        )


class AlienAnimation:
    """This class manages the animation of an alien,
    based on its level prefix. The alien frames are chosen
    based on the current level in the game.
    """

    def __init__(self, game, alien, scale=1.0):
        self.alien = alien
        self.game = game
        self.scale = scale

        self.frame_update_rate = 6
        self.frame_counter = 0
        self.current_frame = 0

        self.frames = {}

        level_prefix = LEVEL_PREFIX.get(game.stats.level // 4 + 1, "Alien7")
        if level_prefix not in self.frames:
            self.frames[level_prefix] = load_alien_images(level_prefix)

        self.frames = self.frames[level_prefix]
        self.image = self.frames[self.current_frame]

    def _update_scale(self):
        """Scale the alien frames."""
        scaled_w = int(self.image.get_width() * self.scale)
        scaled_h = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        self.frames = [
            pygame.transform.scale(frame, (scaled_w, scaled_h)) for frame in self.frames
        ]

    def update_animation(self):
        """Update alien animation."""
        self.frame_counter += 1
        if self.frame_counter % self.frame_update_rate == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.frame_counter = 0

    def change_scale(self, scale):
        """Update scale of Alien."""
        self.scale = scale
        self._update_scale()

    def get_current_image(self):
        """Return the current alien image."""
        return self.image
