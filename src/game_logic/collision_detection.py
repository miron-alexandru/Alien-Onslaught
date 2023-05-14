"""
The 'game_collisions' module contains the CollisionManager class
that handles the collisions in the game.
"""

import pygame
from entities.aliens import BossAlien
from utils.constants import ALIENS_HP_MAP
from utils.game_utils import play_sound, get_colliding_sprites


class CollisionManager:
    """The Collision Manager class manages collisions
    between game entities like ships, aliens, bullets."""

    def __init__(self, game):
        self.game = game
        self.stats = game.stats
        self.settings = game.settings
        self.score_board = game.score_board
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

        self.handled_collisions = {}

    def shield_collisions(self, ships, aliens, bullets, asteroids):
        """Destroy any aliens that collide with the shield of any of the given ships."""
        # Loop through each player and check if the shield is on, if it is, kill the
        # alien, alien bullet or asteroid that collided with it and turn the shield off.
        for ship in ships:
            for alien in aliens:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(
                    alien.rect
                ):
                    if not isinstance(alien, BossAlien):
                        alien.kill()
                    ship.state.shielded = False
            for bullet in bullets:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(
                    bullet.rect
                ):
                    bullet.kill()
                    ship.state.shielded = False
            for asteroid in asteroids:
                if ship.state.shielded and ship.anims.shield_rect.colliderect(asteroid):
                    asteroid.kill()
                    ship.state.shielded = False

    def check_asteroids_collisions(self, thunder_hit_method, phoenix_hit_method):
        """Check for collisions between the ships, missiles and asteroids."""
        # loop through each player and check if it's alive,
        # then check for collisions with asteroids and which player collided
        # and activate the corresponding method
        for ship in self.game.ships:
            if ship.state.alive:
                if collision := pygame.sprite.spritecollideany(
                    ship, self.game.asteroids
                ):
                    if ship is self.thunderbird_ship and not ship.state.immune:
                        thunder_hit_method()
                        collision.kill()
                    if ship is self.phoenix_ship and not ship.state.immune:
                        phoenix_hit_method()
                        collision.kill()

        missiles = pygame.sprite.Group(
            self.game.thunderbird_missiles, self.game.phoenix_missiles
        )
        # Check for collisions between missiles and asteroids
        for missile in missiles:
            if collision := pygame.sprite.spritecollideany(
                missile, self.game.asteroids
            ):
                missile.explode()
                collision.kill()

    def check_powers_collisions(
        self, power_method, health_power_method, weapon_power_method
    ):
        """Check for collision between ships and powers
        If a collision occurs, a random power is activated for the corresponding player
        and the power is removed.
        """
        # Define a dict that maps each player to their corresponding ship,
        # active status, and power functions
        player_info = {
            "thunderbird": {
                "ship": self.thunderbird_ship,
                "active": self.thunderbird_ship.state.alive,
                "power": power_method,
                "health_power_up": health_power_method,
                "weapon": weapon_power_method,
            },
            "phoenix": {
                "ship": self.phoenix_ship,
                "active": self.phoenix_ship.state.alive,
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
                elif collision.weapon:
                    info["weapon"](player, collision.weapon_name)
                else:
                    info["power"](player)
                collision.kill()
                info["ship"].empower()

    def check_bullet_alien_collisions(self):
        """Respond to player bullet-alien collisions."""
        thunderbird_ship_collisions = pygame.sprite.groupcollide(
            self.game.thunderbird_bullets, self.game.aliens, True, False
        )
        phoenix_ship_collisions = pygame.sprite.groupcollide(
            self.game.phoenix_bullets, self.game.aliens, True, False
        )

        # Thunderbird collisions
        if thunderbird_ship_collisions:
            self._handle_alien_hits(thunderbird_ship_collisions, "thunderbird")

        if not self.game.singleplayer and phoenix_ship_collisions:
            self._handle_alien_hits(phoenix_ship_collisions, "phoenix")

    def check_cosmic_conflict_collisions(self, thunderbird_hit, phoenix_hit):
        """Respond to PVP projectile collisions."""
        thunderbird_bullet_hits = get_colliding_sprites(
            self.game.phoenix_ship, self.game.thunderbird_bullets
        )
        phoenix_bullet_hits = get_colliding_sprites(
            self.game.thunderbird_ship, self.game.phoenix_bullets
        )

        if thunderbird_bullet_hits and not self.game.phoenix_ship.state.immune:
            phoenix_hit()
            self.stats.thunderbird_score += 1000
            self.score_board.render_scores()
            self.score_board.update_high_score()

        if phoenix_bullet_hits and not self.game.thunderbird_ship.state.immune:
            thunderbird_hit()
            self.stats.phoenix_score += 1000
            self.score_board.render_scores()
            self.score_board.update_high_score()

        thunderbird_missile_hits = get_colliding_sprites(
            self.game.phoenix_ship, self.game.thunderbird_missiles
        )
        phoenix_missile_hits = get_colliding_sprites(
            self.game.thunderbird_ship, self.game.phoenix_missiles
        )

        for missile in thunderbird_missile_hits:
            if not self.game.phoenix_ship.state.immune:
                phoenix_hit()
                missile.explode()
                print('asd')
                play_sound(self.game.sound_manager.game_sounds, "missile")

        for missile in phoenix_missile_hits:
            if not self.game.thunderbird_ship.state.immune:
                thunderbird_hit()
                missile.explode()
                play_sound(self.game.sound_manager.game_sounds, "missile")


    def check_alien_ship_collisions(self, thunderbird_hit, phoenix_hit):
        """Respond to collisions between aliens and ships and also check if
        any aliens have reached the bottom of the screen.
        """
        for ship in self.game.ships:
            if (
                pygame.sprite.spritecollideany(ship, self.game.aliens)
                and not ship.state.immune
            ):
                if ship is self.thunderbird_ship:
                    thunderbird_hit()
                else:
                    phoenix_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.game.screen.get_rect()
        for alien in self.game.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                alien.kill()
                if not self.game.singleplayer:
                    self.stats.phoenix_score = max(self.stats.phoenix_score - 100, 0)
                self.stats.thunderbird_score = max(
                    self.stats.thunderbird_score - 100, 0
                )
                self.game.score_board.render_scores()
                self.score_board.update_high_score()
                break

    def check_missile_alien_collisions(self):
        """Respond to player missiles-alien collisions."""
        # Collisions with Thunderbird missiles
        thunderbird_missile_collisions = pygame.sprite.groupcollide(
            self.game.thunderbird_missiles, self.game.aliens, False, False
        )

        # Collisions with Phoenix missiles
        phoenix_missile_collisions = pygame.sprite.groupcollide(
            self.game.phoenix_missiles, self.game.aliens, False, False
        )

        # Handle Thunderbird missile collisions
        if thunderbird_missile_collisions:
            self._handle_player_missile_collisions(
                thunderbird_missile_collisions, "thunderbird"
            )
            self._play_missile_sound(thunderbird_missile_collisions.values())

        # Handle Phoenix missile collisions
        if not self.game.singleplayer and phoenix_missile_collisions:
            self._handle_player_missile_collisions(
                phoenix_missile_collisions, "phoenix"
            )
            self._play_missile_sound(phoenix_missile_collisions.values())

    def _play_missile_sound(self, aliens):
        """Helper method that plays the missile sound when
        colliding with normal aliens.
        """
        for alien_list in aliens:
            for alien in alien_list:
                if not isinstance(alien, BossAlien):
                    play_sound(self.game.sound_manager.game_sounds, "missile")

    def _handle_player_missile_collisions(self, player_missile_collisions, player):
        """This method handles what happens with the score and the aliens
        after they have been hit by a player missile.
        """
        for missile in player_missile_collisions.keys():
            missile.explode()
            self._check_missile_ex_collision(self.game.aliens, player, missile)

    def check_alien_bullets_collisions(self, thunder_hit_method, phoenix_hit_method):
        """Manages collisions between the alien bullets and the players."""
        if not self.game.singleplayer:
            player_ships = [self.thunderbird_ship, self.phoenix_ship]
            player_methods = [thunder_hit_method, phoenix_hit_method]
        else:
            player_ships = [self.thunderbird_ship]
            player_methods = [thunder_hit_method]

        player_methods = [thunder_hit_method, phoenix_hit_method]

        for ship, hit_method in zip(player_ships, player_methods):
            if (
                ship.state.alive
                and not ship.state.immune
                and (
                    collision := pygame.sprite.spritecollideany(
                        ship, self.game.alien_bullet
                    )
                )
            ):
                hit_method()
                collision.kill()

    def _handle_boss_alien_collision(self, alien, player):
        """Handles the collision between the player and the bosses"""
        if alien.hit_count >= self.settings.boss_hp and alien.is_alive:
            play_sound(self.game.sound_manager.game_sounds, "boss_exploding")
            alien.destroy_alien()
            self.game.aliens.remove(alien)
            if player == "thunderbird":
                self.stats.thunderbird_score += self.settings.boss_points
            else:
                self.stats.phoenix_score += self.settings.boss_points
            self.score_board.render_scores()
            self.score_board.update_high_score()

    def _handle_alien_hits(self, player_ship_collisions, player):
        """This method handles what happens with the score and the aliens
        after they have been hit.It also increases the hit_count of the aliens
        making them stronger as the game progresses."""
        level = self.stats.level
        max_hit_count = ALIENS_HP_MAP.get(level, 3)
        for aliens in player_ship_collisions.values():
            for alien in aliens:
                alien.hit_count += 1
                if isinstance(alien, BossAlien):
                    self._handle_boss_alien_collision(alien, player)
                elif not alien.immune_state and alien.hit_count >= max_hit_count:
                    self._update_stats(alien, player)

    def _update_stats(self, alien, player):
        """Update player score and remove alien."""
        # when collision happen, update the stats and remove the alien that
        # collided with the bullet
        # method used in _handle_alien_hits
        match player:
            case "thunderbird":
                self.stats.thunderbird_score += self.settings.alien_points
            case "phoenix":
                self.stats.phoenix_score += self.settings.alien_points
        alien.destroy_alien()
        play_sound(self.game.sound_manager.game_sounds, "alien_exploding")
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
                        play_sound(self.game.sound_manager.game_sounds, "missile")
                        alien.hit_count += 5
                        self._handle_boss_alien_collision(alien, player)
                        self.handled_collisions[(missile, alien)] = True
                elif ex_rect.colliderect(alien.rect):
                    self._update_stats(alien, player)
