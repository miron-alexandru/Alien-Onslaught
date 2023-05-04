"""
The 'alien_bullets' module contains classes for managing bullets fired by aliens and bosses in the game.

Classes:
    - 'AlienBullet': A class to manage bullets fired by normal aliens in the game.
    - 'BossBullet': A class to manage bullets fired by the boss alien in the game.
    - 'AlienBulletsManager': A class to manage the creation and update of alien bullets in the game.
"""

import random
import pygame

from pygame.sprite import Sprite
from utils.constants import boss_rush_bullet_map, normal_bullet_map
from utils.game_utils import load_alien_bullets
from entities.aliens import BossAlien


class AlienBullet(Sprite):
    """A class that manages bullets for the aliens."""

    bullet_images = load_alien_bullets()

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = self.bullet_images['alien_bullet']
        self.rect = self.image.get_rect()
        self._choose_random_alien(game)

    def _choose_random_alien(self, game):
        """Choose a random alien as the source of the bullet."""
        random_alien = random.choice(game.aliens.sprites())
        self.rect.centerx = random_alien.rect.centerx
        self.rect.bottom = random_alien.rect.bottom
        self.y_pos = float(self.rect.y)

    def update(self):
        """Update bullet position."""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos

    def draw(self):
        """Draw the bullet on screen."""
        self.screen.blit(self.image, self.rect)


class BossBullet(Sprite):
    """A class that manages bullets for the boss alien."""

    bullet_images = load_alien_bullets()

    def __init__(self, game, alien):
        """Initializes a new bullet for an alien."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.alien = alien
        self.image = self.bullet_images['xanathar_bullet']
        self.rect = self.image.get_rect()
        self._init_variables(alien)
        self._update_image(game)

    def _init_variables(self, alien):
        """Initializes position and speed variables."""
        self.rect.inflate_ip(-40, -40)
        self.rect.center = alien.rect.center
        self.rect.bottom = alien.rect.bottom
        self.y_pos = float(self.rect.y)
        self.x_vel = random.uniform(-4, 4)

    def _update_image(self, game):
        """Change bullet image for specific boss fights."""
        if self.settings.game_modes.boss_rush:
            level_image_map = boss_rush_bullet_map
        else:
            level_image_map = normal_bullet_map
        level = game.stats.level
        image_name = level_image_map.get(level)
        if image_name is not None:
            self.image = self.bullet_images[image_name]

    def update(self):
        """Update the bullet location on screen."""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos
        self.rect.x += round(self.x_vel)

    def draw(self):
        """Draw the bullet on screen."""
        self.screen.blit(self.image, self.rect)


class AlienBulletsManager:
    """The AlienBulletsManager manages the creation and update for the normal
    and boss bullets in the game.
    """
    def __init__(self, game):
        """Initializes the AlienBulletsManager object."""
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.alien_bullet = game.alien_bullet
        self.aliens = game.aliens
        self.thunderbird_ship = game.thunderbird_ship
        self.phoenix_ship = game.phoenix_ship

        self.last_alien_bullet_time = 0


    def _create_alien_bullet(self, alien):
        """Create an alien bullet at the specified alien rect.
        If the given alien is a BossAlien, a BossBullet will be created, 
        otherwise an AlienBullet will be created.
        """
        if isinstance(alien, BossAlien):
            bullet = BossBullet(self, alien)
        else:
            bullet = AlienBullet(self)
        bullet.rect.centerx = alien.rect.centerx
        bullet.rect.bottom = alien.rect.bottom
        self.alien_bullet.add(bullet)

    def create_alien_bullets(self, num_bullets, bullet_int, alien_int):
        """
        Create a certain number of bullets from randomly selected aliens, based on time intervals.
        
        Args:
        - num_bullets: The number of bullets to create.
        - bullet_int: The interval of time (in milliseconds) that
          must pass since any alien fired a bullet.
        - alien_int: The interval of time (in milliseconds) that
          must pass since a specific alien last fired a bullet.
        """
        current_time = pygame.time.get_ticks()
        # check if enough time has passed since any alien fired a bullet
        if current_time - self.last_alien_bullet_time >= bullet_int:
            self.last_alien_bullet_time = current_time
            aliens = random.sample(self.aliens.sprites(), k=min(num_bullets,
                                                                     len(self.aliens.sprites())))
            # create bullets from randomly selected aliens
            for alien in aliens:
                # check if enough time has passed since this alien fired a bullet
                if (alien.last_bullet_time == 0 or
                current_time - alien.last_bullet_time >= alien_int):
                    alien.last_bullet_time = current_time
                    self._create_alien_bullet(alien)

    def update_alien_bullets(self):
        """Update alien bullets and remove bullets that went off screen."""
        self.alien_bullet.update()
        for bullet in self.alien_bullet.copy():
            if bullet.rect.y > self.settings.screen_height:
                self.alien_bullet.remove(bullet)
