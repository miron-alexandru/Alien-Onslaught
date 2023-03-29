"""The game_collisions module handles the collisions in the game"""

import pygame
from entities.aliens import BossAlien


class CollisionManager:
    """The Collision Manager class manages collisions between game entities like
    ships, aliens, bullets, and asteroids."""
    def __init__(self, game):
        self.game = game
        self.stats =  game.stats
        self.settings = game.settings
        self.score_board = game.score_board


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


    def check_power_ups_collisions(self, power_up_method, health_power_up_method):
        """Check for collision between ships and power-ups
        If a collision occurs, a random power up is activated for the corresponding player
        and the power up is removed.
        """
        # Define a dict that maps each player to their corresponding ship,
        # active status, and power-up functions
        player_info = {
            "thunderbird": {
                "ship": self.game.thunderbird_ship,
                "active": self.game.thunderbird_ship.state.alive,
                "power_up": power_up_method,
                "health_power_up": health_power_up_method,
            },
            "phoenix": {
                "ship": self.game.phoenix_ship,
                "active": self.game.phoenix_ship.state.alive,
                "power_up": power_up_method,
                "health_power_up": health_power_up_method,
            },
        }
        # loop through each player and check for collisions
        for player, info in player_info.items():
            collision = pygame.sprite.spritecollideany(info["ship"], self.game.power_ups)
            if info["active"] and collision:
                # play the empower effect, check the type of the power up and activate the func
                if collision.health:
                    info["health_power_up"](player)
                else:
                    info["power_up"](player)
                collision.kill()
                info["ship"].empower()


    def check_bullet_alien_collisions(self, singleplayer=False):
        """Respond to bullet-alien collisions."""
        thunderbird_ship_collisions = pygame.sprite.groupcollide(
            self.game.thunderbird_bullets, self.game.aliens, True, False)
        phoenix_ship_collisions = pygame.sprite.groupcollide(
            self.game.phoenix_bullets, self.game.aliens, True, False)

        # Thunderbird collisions
<<<<<<< HEAD
        if thunderbird_ship_collisions:
=======
        if self.game.thunderbird_ship.state.alive and thunderbird_ship_collisions:
>>>>>>> 3034d0c87f65fb882db55122af241e8ee7958458
            self.handle_player_collisions(thunderbird_ship_collisions, 'thunderbird')

        if (
            not singleplayer
<<<<<<< HEAD
=======
            and self.game.phoenix_ship.state.alive
>>>>>>> 3034d0c87f65fb882db55122af241e8ee7958458
            and phoenix_ship_collisions
        ):
            self.handle_player_collisions(phoenix_ship_collisions, 'phoenix')



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


    def handle_player_collisions(self, player_ship_collisions, player):
        """This method method handles what happens with the score, and the aliens
        after they have been hit, it also increases the hit_count of the aliens
        making them stronger as the game progresses."""
        for aliens in player_ship_collisions.values():
            for alien in aliens:
                alien.hit_count += 1
                if isinstance(alien, BossAlien):
                    if alien.hit_count >= self.settings.boss_hp and alien.is_alive:
                        alien.destroy_alien()
                        self.game.aliens.remove(alien)
                        if player == 'thunderbird':
                            self.stats.thunderbird_score += self.settings.boss_points
                        else:
                            self.stats.phoenix_score += self.settings.boss_points
                        self.score_board.render_scores()
                        self.score_board.update_high_score()
                elif (
                    self.stats.level < 5
                    and alien.hit_count >= 1
                    or self.stats.level >= 5
                    and self.stats.level < 10
                    and alien.hit_count >= 2
                    or self.stats.level >= 5
                    and self.stats.level >= 10
                    and alien.hit_count >= 3
                ):
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
