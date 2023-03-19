"""
The alien_bullets module contains the classes for creating and
managing aliens and boss alien bullets."""

import random
import pygame

from pygame.sprite import Sprite
from utils.constants import ALIENS
from entities.aliens import BossAlien


class AlienBullet(Sprite):
    """A class to manage bullets for the aliens."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load(ALIENS['alien_bullet'])
        self.rect = self.image.get_rect()
        self._choose_random_alien(game)


    def _choose_random_alien(self, game):
        """Choose a random alien as the source of the bullet"""
        random_alien = random.choice(game.aliens.sprites())
        self.rect.centerx = random_alien.rect.centerx
        self.rect.bottom = random_alien.rect.bottom
        self.y_pos = float(self.rect.y)

    def update(self):
        """Update bullet position"""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos

    def draw_bullet(self):
        """Draw the bullet"""
        self.screen.blit(self.image, self.rect)


class BossBullet(Sprite):
    """A class to manage bullets for the boss alien."""
    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.alien = alien
        self.image = self._get_bullet_image(game)
        self.rect = self.image.get_rect()
        self._init_variables(alien)


    def _init_variables(self, alien):
        """Initializes position and speed variables"""
        self.rect.inflate_ip(-50, -50)
        self.rect.center = alien.rect.center
        self.y_pos = float(self.rect.y)
        self.x_vel = random.uniform(-4, 4)

    def _get_bullet_image(self, game):
        """Return the bullet image based on the current level"""
        images = ALIENS
        level = game.stats.level
        if level == 15:
            return pygame.image.load(images['scorpion_bullet'])
        if level == 20:
            return pygame.image.load(images['mothership_bullet'])
        return pygame.image.load(images['xanathar_bullet'])

    def update(self):
        """Update the bullet location"""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos
        self.rect.x += round(self.x_vel)

    def draw_bullet(self):
        """Draw the bullet"""
        self.screen.blit(self.image, self.rect)


class AlienBulletsManager:
    """The AlienBulletsManager manages the creation and update for the normal
    and boss bullets in the game."""
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.alien_bullet = game.alien_bullet
        self.aliens = game.aliens

        self.last_alien_bullet_time = 0


    def _create_alien_bullet(self, alien):
        """Create an alien bullet at the specified alien rect"""
        # create different bullets for bosses
        if isinstance(alien, BossAlien):
            bullet = BossBullet(self, alien)
        else:
            bullet = AlienBullet(self)
        bullet.rect.centerx = alien.rect.centerx
        bullet.rect.bottom = alien.rect.bottom
        self.alien_bullet.add(bullet)

    def create_alien_bullets(self, num_bullets, bullet_int, alien_int):
        """Create a certain number of bullets at a certain time.
        bullet_int - for adjusting how often aliens fire bullets.
        alien_int - for adjusting how often a specific alien fires a bullet.
        """
        current_time = pygame.time.get_ticks()
        # calculate the time since any alien fired a bullet
        if current_time - self.last_alien_bullet_time >= bullet_int:
            self.last_alien_bullet_time = current_time
            aliens = random.sample(self.aliens.sprites(), k=min(num_bullets,
                                                                     len(self.aliens.sprites())))
            for alien in aliens:
                # calculate the time since a specific alien fired a bullet
                if (alien.last_bullet_time == 0 or
                current_time - alien.last_bullet_time >= alien_int):
                    alien.last_bullet_time = current_time
                    self._create_alien_bullet(alien)

    def update_alien_bullets(self):
        """Update alien bullets and remove bullets that went off screen"""
        self.alien_bullet.update()
        for bullet in self.alien_bullet.copy():
            if bullet.rect.bottom <= 0:
                self.alien_bullet.remove(bullet)
