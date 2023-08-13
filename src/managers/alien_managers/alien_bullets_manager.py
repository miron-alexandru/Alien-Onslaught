"""
The 'alien_bullets_manager' module contains the AlienBulletsManager class used for
managing bullets fired by aliens and bosses in the game.
"""


import random
import pygame

from src.entities.alien_entities.alien_bullets import AlienBullet, BossBullet
from src.entities.alien_entities.aliens import BossAlien


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
        """Create an alien bullet at the specified alien rect."""
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
            aliens = random.sample(
                self.aliens.sprites(), k=min(num_bullets, len(self.aliens.sprites()))
            )
            # create bullets from randomly selected aliens
            for alien in aliens:
                # check if enough time has passed since this alien fired a bullet
                if (
                    alien.last_bullet_time == 0
                    or current_time - alien.last_bullet_time >= alien_int
                ):
                    alien.last_bullet_time = current_time
                    self._create_alien_bullet(alien)

    def update_alien_bullets(self):
        """Update alien bullets and remove bullets that went off screen."""
        self.alien_bullet.update()
        for bullet in self.alien_bullet.copy():
            if bullet.rect.y > self.settings.screen_height:
                self.alien_bullet.remove(bullet)
