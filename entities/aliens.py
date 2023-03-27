"""
Alien module
This module contains the class for creating instances of aliens and bosses.
"""
import math
import random
import pygame

from pygame.sprite import Sprite
from utils.constants import LEVEL_PREFIX, boss_rush_image_map, normal_image_map
from utils.game_utils import load_alien_images, load_boss_images
from animations.other_animations import DestroyAnim

class Alien(Sprite):
    """A class to represent an alien."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats

        self.hit_count = 0
        self.last_bullet_time = 0

        self.motion = AlienMovement(self, game)
        self.animation = AlienAnimation(self, game)
        self.destroy = DestroyAnim(self)
        self.image = self.animation.get_current_image()
        self._init_position()


    def _init_position(self):
        self.rect = self.animation.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = self.rect.height
        self.x_pos = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right or self.rect.left <= 0)


    def check_top_edges(self):
        """Return True if alien is at the top of the screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.top <= screen_rect.top


    def update(self):
        """Update alien position on screen."""
        self.x_pos += self.settings.alien_speed * self.motion.direction
        self.rect.x = round(self.x_pos)

        self.animation.update_animation()
        self.image = self.animation.get_current_image()

        self.motion.update_vertical_position()
        self.motion.update_horizontal_position()


    def destroy_alien(self):
        """Start alien destroyed animation and start it"""
        self.destroy.update_destroy_animation()
        self.screen.blit(self.destroy.destroy_image, self.destroy.destroy_rect)


class BossAlien(Sprite):
    """A class to represent Boss Aliens"""

    boss_images = load_boss_images()

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = self.boss_images['xanathar']
        self._update_image(game)

        self.last_bullet_time = 0
        self.hit_count = 0
        self.is_alive = True

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-30, 0)
        self.rect.x =  self.rect.width
        self.rect.y = self.rect.height - self.image.get_height() + 50
        self.x_pos = float(self.rect.x)

        self.motion = AlienMovement(self, game)
        self.destroy = DestroyAnim(self)


    def _update_image(self, game):
        """Change image for specific boss fight"""
        if self.settings.gm.boss_rush:
            level_image_map = boss_rush_image_map
        else:
            level_image_map = normal_image_map
        level = game.stats.level
        image_name = level_image_map.get(level)
        if image_name is not None:
            self.image = self.boss_images[image_name]


    def update(self):
        """Update position and movement."""
        self.x_pos += self.settings.alien_speed * self.motion.direction
        self.rect.x = round(self.x_pos)

        self.motion.update_horizontal_position()

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def destroy_alien(self):
        """Update and display destroy animation."""
        self.is_alive = False
        self.destroy.update_destroy_animation()
        self.screen.blit(self.destroy.destroy_image, self.destroy.destroy_rect)



class AliensManager:
    """The AliensManager class manages the following aspects of aliens and bosses:
    creation, update and the behavior when aliens are are edges of the screen."""
    def __init__(self, game, aliens, settings, screen):
        self.game = game
        self.aliens = aliens
        self.settings = settings
        self.screen = screen
        self.stats = game.stats

    def create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Calculate the starting y-coordinate for the first row of aliens
        start_y = 50

        # Create the full fleet of aliens.
        for row_number in range(self.settings.fleet_rows):
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


    def update_aliens(self, thunderbird_hit_method, phoenix_hit_method, singleplayer=False):
        """Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if (
            pygame.sprite.spritecollideany(self.game.thunderbird_ship, self.aliens)
            and not self.game.thunderbird_ship.state['immune']
        ):
            thunderbird_hit_method()
        if (
            not singleplayer
            and pygame.sprite.spritecollideany(self.game.phoenix_ship, self.aliens)
            and not self.game.phoenix_ship.state['immune']
        ):
            phoenix_hit_method()
        self._check_aliens_bottom(thunderbird_hit_method, phoenix_hit_method)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Change the direction of each alien and drop them down."""
        # bosses are not moving down
        for alien in self.aliens.sprites():
            if isinstance(alien, BossAlien):
                if alien.check_edges():
                    alien.motion.direction *= -1
                else:
                    alien.rect.x += (self.settings.alien_speed *
                                     alien.motion.direction)
            elif alien.check_edges():
                alien.motion.direction *= -1

            elif alien.check_top_edges():
                alien.rect.y += self.settings.alien_speed


    def _check_aliens_bottom(self, thunderbird_hit_method, phoenix_hit_method):
        """Check if an alien have reached the bottom of the screen"""
        # if an alien reaches the bottom of the screen, both players are losing 1hp
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                thunderbird_hit_method()
                phoenix_hit_method()
                alien.kill()
                break



class AlienMovement:
    """A class to manage the movement of an alien."""
    def __init__(self, alien, game):
        self.alien = alien
        self.settings = game.settings

        self.direction = self.settings.alien_direction
        self.last_direction_change = pygame.time.get_ticks()
        self.direction_change_delay = 0

        self.sins = {
            "time_offset": random.uniform(0, 2*math.pi),
            "amplitude": random.randint(1, 2),
            "frequency": random.uniform(0.001, 0.02)
        }

    def update_horizontal_position(self):
        """Update the horizontal position 
        of the alien by creating random movement"""
        now = pygame.time.get_ticks()
        if now - self.last_direction_change > self.direction_change_delay:
            # Check if alien is not near the edge of the screen
            if not self.alien.check_edges():
                self.direction *= -1
            self.last_direction_change = now
            # how often the direction changes
            self.direction_change_delay = random.randint(3000, 5000) # miliseconds

    def update_vertical_position(self):
        """Update the vertical position 
        of the alien by creating random movement"""
        now = pygame.time.get_ticks()
        time = now + self.sins['time_offset']
        self.alien.rect.y = round(
            self.alien.rect.y
            + self.sins['amplitude']
            * math.sin(self.sins['frequency'] * time)
            + 0.3
        )


class AlienAnimation:
    """This class manages alien animations"""
    frames = {}

    def __init__(self, game, alien):
        self.alien = alien
        self.game = game

        self.last_update_time = pygame.time.get_ticks()
        self.animation_delay = 70
        self.current_frame = 0

        level_prefix = LEVEL_PREFIX.get(game.stats.level // 4 + 1, "Alien4")
        if level_prefix not in AlienAnimation.frames:
            AlienAnimation.frames[level_prefix] = load_alien_images(level_prefix)

        self.frames = AlienAnimation.frames[level_prefix]
        self.image = self.frames[self.current_frame]

    def update_animation(self):
        """Update animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update_time = now

    def get_current_image(self):
        """Return the current image"""
        return self.image
