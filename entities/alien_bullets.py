"""The alien_bullets module contains the classes for creating and
managing aliens and boss alien bullets."""

import random
import math
import pygame

from pygame.sprite import Sprite
from utils.constants import boss_rush_bullet_map, normal_bullet_map
from utils.game_utils import load_alien_bullets
from entities.aliens import BossAlien


class AlienBullet(Sprite):
    """A class to manage bullets for the aliens."""

    bullet_images = load_alien_bullets()

    def __init__(self, game, target_ship=None):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = self.bullet_images['alien_bullet']
        self.rect = self.image.get_rect()
        self._choose_random_alien(game)
        self.target_ship = target_ship


    def _choose_random_alien(self, game):
        """Choose a random alien as the source of the bullet"""
        random_alien = random.choice(game.aliens.sprites())
        self.rect.centerx = random_alien.rect.centerx
        self.rect.bottom = random_alien.rect.bottom
        self.y_pos = float(self.rect.y)

    def update(self):
        """Update bullet position"""
        if self.target_ship:
            # Check if bullet has passed the target ship's y-coordinate
            if self.rect.y > self.target_ship.rect.centery:
                # Move the bullet downwards
                self.rect.y += self.settings.alien_bullet_speed
                return

            # Update bullet position based on target ship's location
            x_diff = self.target_ship.rect.centerx - self.rect.centerx
            y_diff = self.target_ship.rect.centery - self.rect.centery
            angle = math.atan2(y_diff, x_diff)
            move_x = math.cos(angle) * self.settings.alien_bullet_speed
            self.rect.x += move_x

        # Update bullet position if no target ship is set
        self.rect.y += self.settings.alien_bullet_speed

    def draw(self):
        """Draw the bullet"""
        self.screen.blit(self.image, self.rect)



class BossBullet(Sprite):
    """A class to manage bullets for the boss alien."""

    bullet_images = load_alien_bullets()

    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.alien = alien
        self.image = self.bullet_images['xanathar_bullet']
        self.rect = self.image.get_rect()
        self._init_variables(alien)
        self._update_image(game)

    def _init_variables(self, alien):
        """Initializes position and speed variables"""
        self.rect.inflate_ip(-50, -50)
        self.rect.center = alien.rect.center
        self.rect.bottom = alien.rect.bottom
        self.y_pos = float(self.rect.y)
        self.x_vel = random.uniform(-4, 4)

    def _update_image(self, game):
        """Change image for specific boss fight"""
        if self.settings.game_modes.boss_rush:
            level_image_map = boss_rush_bullet_map
        else:
            level_image_map = normal_bullet_map
        level = game.stats.level
        image_name = level_image_map.get(level)
        if image_name is not None:
            self.image = self.bullet_images[image_name]

    def update(self):
        """Update the bullet location"""
        self.y_pos += self.settings.alien_bullet_speed
        self.rect.y = self.y_pos
        self.rect.x += round(self.x_vel)

    def draw(self):
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
        self.thunderbird_ship = game.thunderbird_ship
        self.phoenix_ship = game.phoenix_ship

        self.last_alien_bullet_time = 0


    def _create_alien_bullet(self, alien, target_ship):
        """Create an alien bullet at the specified alien rect,
        targeting the given ship.
        """
        # create different bullets for bosses
        if isinstance(alien, BossAlien):
            bullet = BossBullet(self, alien)
        else:
            bullet = AlienBullet(self)
            bullet.target_ship = target_ship
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
            if valid_ships := [
                ship for ship in self.game.ships if ship.state.alive
            ]:
                aliens = random.sample(self.aliens.sprites(), k=min(num_bullets,
                                                            len(self.aliens.sprites())))
                for alien in aliens:
                    # calculate the time since a specific alien fired a bullet
                    if (alien.last_bullet_time == 0 or
                    current_time - alien.last_bullet_time >= alien_int):
                        alien.last_bullet_time = current_time
                        target_ship = random.choice(valid_ships)
                        self._create_alien_bullet(alien, target_ship)



    def update_alien_bullets(self):
        """Update alien bullets and remove bullets that went off screen"""
        self.alien_bullet.update()
        for bullet in self.alien_bullet.copy():
            if bullet.rect.y > self.settings.screen_height:
                self.alien_bullet.remove(bullet)
