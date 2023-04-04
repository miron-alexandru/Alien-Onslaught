"""The game_collisions module handles the collisions in the game"""

import pygame
from entities.aliens import BossAlien
from utils.constants import ALIENS_HP_MAP


class CollisionManager:
    """The Collision Manager class manages collisions between game entities like
    ships, aliens, bullets, and asteroids."""
    def __init__(self, game):
        self.game = game
        self.stats =  game.stats
        self.settings = game.settings
        self.score_board = game.score_board

        self.handled_collisions = {}

    def shield_collisions(self, ships, aliens, bullets, asteroids):
        """Destroy any aliens that collide with the shield of any of the given ships."""
        # Loop through each player and check if the shield is on, if it is, kill the
        # alien, alien bullet or asteroid that collided with it and turn the shield off.
        for ship in ships:
            for alien in aliens:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(alien.rect):
                    if not isinstance(alien, BossAlien):
                        alien.kill()
                    ship.state.shielded = False
            for bullet in bullets:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(bullet.rect):
                    bullet.kill()
                    ship.state.shielded = False
            for asteroid in asteroids:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(asteroid):
                    asteroid.kill()
                    ship.state.shielded = False

    def check_asteroids_collisions(self, thunderbird_hit, phoenix_hit):
        """Check for collisions between the ships and asteroids"""
        # loop through each player and check if it's alive,
        # then check for collisions with asteroids and which player collided
        # and activate the corresponding method
        for ship in self.game.ships:
            if ship.state.alive:
                if collision := pygame.sprite.spritecollideany(
                    ship, self.game.asteroids
                ):
                    if (ship is self.game.thunderbird_ship
                        and not self.game.thunderbird_ship.state.immune):
                        thunderbird_hit()
                        collision.kill()
                    if (ship is self.game.phoenix_ship
                        and not self.game.phoenix_ship.state.immune):
                        phoenix_hit()
                        collision.kill()

    def check_powers_collisions(self, power_method, health_power_method, weapon_power_method):
        """Check for collision between ships and powers
        If a collision occurs, a random power is activated for the corresponding player
        and the power is removed.
        """
        # Define a dict that maps each player to their corresponding ship,
        # active status, and power functions
        player_info = {
            "thunderbird": {
                "ship": self.game.thunderbird_ship,
                "active": self.game.thunderbird_ship.state.alive,
                "power": power_method,
                "health_power_up": health_power_method,
                "weapon": weapon_power_method,
            },
            "phoenix": {
                "ship": self.game.phoenix_ship,
                "active": self.game.phoenix_ship.state.alive,
                "power": power_method,
                "health_power_up": health_power_method,
                "weapon": weapon_power_method,
            },
        }
        # loop through each player and check for collisions
        for player, info in player_info.items():
            collision = pygame.sprite.spritecollideany(info["ship"], self.game.powers)
            if info["active"] and collision:
                # play the empower effect, check the type of the power and activate the func
                if collision.health:
                    info["health_power_up"](player)
                if collision.weapon:
                    info["weapon"](player)
                else:
                    info["power"](player)
                collision.kill()
                info["ship"].empower()


    def check_bullet_alien_collisions(self, singleplayer=False):
        """Respond to bullet-alien collisions."""
        thunderbird_ship_collisions = pygame.sprite.groupcollide(
            self.game.thunderbird_bullets, self.game.aliens, True, False)
        phoenix_ship_collisions = pygame.sprite.groupcollide(
            self.game.phoenix_bullets, self.game.aliens, True, False)

        # Thunderbird collisions
        if thunderbird_ship_collisions:
            self._handle_player_collisions(thunderbird_ship_collisions, 'thunderbird')

        if (
            not singleplayer
            and phoenix_ship_collisions
        ):
            self._handle_player_collisions(phoenix_ship_collisions, 'phoenix')


    def check_missile_alien_collisions(self, singleplayer=False):
        """Respond to missile-alien collisions."""
        # Collisions with Thunderbird missiles
        thunderbird_missile_collisions = pygame.sprite.groupcollide(
            self.game.thunderbird_missiles, self.game.aliens, False, False)

        # Collisions with Phoenix missiles
        phoenix_missile_collisions = pygame.sprite.groupcollide(
            self.game.phoenix_missiles, self.game.aliens, False, False)

        # Handle Thunderbird missile collisions
        if thunderbird_missile_collisions:
            self._handle_player_missile_collisions(thunderbird_missile_collisions, 'thunderbird')
        # Handle Phoenix missile collisions
        if not singleplayer and phoenix_missile_collisions:
            self._handle_player_missile_collisions(phoenix_missile_collisions, 'phoenix')


    def _handle_player_missile_collisions(self, player_missile_collisions, player):
        """This method handles what happens with the score and the aliens
        after they have been hit by a player missile. It also increases the
        hit_count of the aliens, making them stronger as the game progresses."""
        for missile in player_missile_collisions.keys():
            missile.explode()
            self._check_missile_ex_collision(self.game.aliens, player, missile)


    def check_alien_bullets_collisions(self, thunderbird_hit, phoenix_hit):
        """Manages collisions between the alien bullets and the players"""
        # check for collisions between each player and alien bullet and if a collision
        # occurrs, call the appropriate method and kill the collision.
        thunderbird_collision = pygame.sprite.spritecollideany(self.game.thunderbird_ship,
                                                                 self.game.alien_bullet)
        phoenix_collision = pygame.sprite.spritecollideany(self.game.phoenix_ship,
                                                                  self.game.alien_bullet)

        if (self.game.thunderbird_ship.state.alive
            and not self.game.thunderbird_ship.state.immune
            and thunderbird_collision):
            thunderbird_hit()
            thunderbird_collision.kill()

        if (self.game.phoenix_ship.state.alive
         and not self.game.phoenix_ship.state.immune
         and phoenix_collision):
            phoenix_hit()
            phoenix_collision.kill()


    def _handle_boss_alien_collision(self, alien, player):
        if alien.hit_count >= self.settings.boss_hp and alien.is_alive:
            alien.destroy_alien()
            self.game.aliens.remove(alien)
            if player == 'thunderbird':
                self.stats.thunderbird_score += self.settings.boss_points
            else:
                self.stats.phoenix_score += self.settings.boss_points
            self.score_board.render_scores()
            self.score_board.update_high_score()


    def _handle_player_collisions(self, player_ship_collisions, player):
        """This method handles what happens with the score and the aliens
        after they have been hit.It also increases the hit_count of the aliens
        making them stronger as the game progresses."""
        for aliens in player_ship_collisions.values():
            for alien in aliens:
                alien.hit_count += 1
                if isinstance(alien, BossAlien):
                    self._handle_boss_alien_collision(alien, player)
                else:
                    level = self.stats.level
                    max_hit_count = ALIENS_HP_MAP.get(level, 3)
                    if alien.hit_count >= max_hit_count:
                        self._update_stats(alien, player)


    def _update_stats(self, alien, player):
        """Update player score and remove alien"""
        # when collision happen, update the stats and remove the alien that
        # collided with the bullet
        # method used in _handle_player_collisions
        match player:
            case 'thunderbird':
                self.stats.thunderbird_score += self.settings.alien_points
            case 'phoenix':
                self.stats.phoenix_score += self.settings.alien_points
        alien.destroy_alien()
        self.game.aliens.remove(alien)
        self.score_board.render_scores()
        self.score_board.update_high_score()


    def _check_missile_ex_collision(self, aliens, player, missile):
        """Checks collisions between aliens and missile explosion."""
        for ex_frame in missile.destroy_anim.ex_frames:
            ex_rect = ex_frame.get_rect(center=missile.rect.center)
            for alien in aliens:
                if isinstance(alien, BossAlien):
                    if (missile, alien) not in self.handled_collisions:
                        alien.hit_count += 5
                        self._handle_boss_alien_collision(alien, player)
                        self.handled_collisions[(missile, alien)] = True
                elif ex_rect.colliderect(alien.rect):
                    self._update_stats(alien, player)
