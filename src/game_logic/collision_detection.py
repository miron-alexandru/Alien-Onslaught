"""
The 'collision_detection' module contains the CollisionManager class
that handles the collisions in the game.
"""

import time
import pygame

from src.entities.projectiles.missile import Missile
from src.entities.alien_entities.aliens import BossAlien

from src.utils.constants import ALIENS_HP_MAP
from src.utils.game_utils import play_sound, get_colliding_sprites


class CollisionManager:
    """The Collision Manager class manages the collisions
    between game entities."""

    def __init__(self, game):
        self.game = game
        self.stats = game.stats
        self.settings = game.settings
        self.score_board = game.score_board
        self.thunderbird_ship = self.game.thunderbird_ship
        self.phoenix_ship = self.game.phoenix_ship

        self.handled_collisions = {}

    def handle_shielded_ship_collisions(self, ships, aliens, bullets, asteroids):
        """Destroy aliens, bullets, or asteroids colliding with ship shields."""
        for ship in ships:
            self._handle_alien_collisions_with_shielded_ship(ship, aliens)
            self._handle_bullet_collisions_with_shielded_ship(ship, bullets)
            self._handle_asteroid_collisions_with_shielded_ship(ship, asteroids)

    def _handle_alien_collisions_with_shielded_ship(self, ship, aliens):
        """Handle collisions between aliens and ship shields."""
        for alien in aliens:
            if ship.state.shielded and ship.anims.shield_rect.colliderect(alien.rect):
                if not isinstance(alien, BossAlien):
                    self._destroy_alien_and_play_sound(alien)
                ship.state.shielded = False

    def _handle_bullet_collisions_with_shielded_ship(self, ship, bullets):
        """Handle collisions between bullets and ship shields."""
        for bullet in bullets:
            if ship.state.shielded and ship.anims.shield_rect.colliderect(bullet.rect):
                self._resolve_shield_collision(bullet, "alien_exploding", ship)

    def _handle_asteroid_collisions_with_shielded_ship(self, ship, asteroids):
        """Handle collisions between asteroids and ship shields."""
        for asteroid in asteroids:
            if ship.state.shielded and ship.anims.shield_rect.colliderect(asteroid):
                self._resolve_shield_collision(asteroid, "asteroid_exploding", ship)

    def _destroy_alien_and_play_sound(self, alien):
        """Destroy an alien and play the corresponding sound."""
        alien.kill()
        play_sound(self.game.sound_manager.game_sounds, "alien_exploding")

    def _resolve_shield_collision(self, entity, sound_key, ship):
        """Handle a collision with a shielded ship and play a sound."""
        entity.kill()
        play_sound(self.game.sound_manager.game_sounds, sound_key)
        ship.state.shielded = False

    def check_asteroids_collisions(self, thunder_hit_method, phoenix_hit_method):
        """Check for collisions between asteroids and ships, missiles, lasers"""
        for ship in self.game.ships:
            if ship.state.alive:
                self._handle_ship_asteroid_collision(
                    ship, thunder_hit_method, phoenix_hit_method
                )

        self._handle_projectile_asteroid_collisions(
            self.game.thunderbird_missiles, self.game.phoenix_missiles
        )
        self._handle_projectile_asteroid_collisions(
            self.game.thunderbird_laser, self.game.phoenix_laser
        )

    def _handle_ship_asteroid_collision(
        self, ship, thunder_hit_method, phoenix_hit_method
    ):
        """Handle collision between ship and asteroids."""
        if collision := pygame.sprite.spritecollideany(ship, self.game.asteroids):
            hit_method = (
                thunder_hit_method
                if ship is self.thunderbird_ship
                else phoenix_hit_method
            )
            self._process_ship_asteroid_collision(ship, hit_method, collision)

    def _process_ship_asteroid_collision(self, ship, hit_method, collision):
        """Process collision between ship and asteroid."""
        if not ship.state.immune:
            hit_method()
            collision.kill()
            play_sound(self.game.sound_manager.game_sounds, "asteroid_exploding")

    def _handle_projectile_asteroid_collisions(self, *projectile_groups):
        """Handle collisions between projectiles and asteroids."""
        for sprite_group in projectile_groups:
            for sprite in sprite_group:
                self._handle_projectile_asteroid_collision(sprite)

    def _handle_projectile_asteroid_collision(self, sprite):
        """Handle collision between projectile and asteroids."""
        if collision := pygame.sprite.spritecollideany(sprite, self.game.asteroids):
            collision.kill()
            play_sound(self.game.sound_manager.game_sounds, "asteroid_exploding")
            if isinstance(sprite, Missile):
                sprite.explode()

    def check_powers_collisions(
        self, power_method, health_power_method, weapon_power_method
    ):
        """Check for collisions between ships and powers."""
        player_ships = [
            ("thunderbird", self.thunderbird_ship),
            ("phoenix", self.phoenix_ship),
        ]

        for player, ship in player_ships:
            self._handle_ship_power_collision(
                player, ship, power_method, health_power_method, weapon_power_method
            )

    def _handle_ship_power_collision(
        self, player, ship, power_method, health_power_method, weapon_power_method
    ):
        """Handle collision between ship and powers."""
        if not ship.state.alive:
            return

        if collision := pygame.sprite.spritecollideany(ship, self.game.powers):
            self._activate_power(
                player,
                ship,
                collision,
                power_method,
                health_power_method,
                weapon_power_method,
            )
            collision.kill()
            ship.empower()

    def _activate_power(
        self,
        player,
        ship,
        collision,
        power_method,
        health_power_method,
        weapon_power_method,
    ):
        """Activate the appropriate power for the ship."""
        if collision.health:
            health_power_method(player)
            ship.power_name = "+1 HP"
            ship.display_power = True
        elif collision.weapon:
            weapon_power_method(player, collision.weapon_name)
            ship.power_name = "Weapon"
            ship.display_power = True
        else:
            power_method(player)

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

    def _update_cosmic_conflict_scores(self, ship, hit_function, score_increment):
        if ship == self.thunderbird_ship:
            self.stats.phoenix_score += score_increment
        else:
            self.stats.thunderbird_score += score_increment
        hit_function()
        self.score_board.render_scores()
        self.score_board.update_high_score()

    def _resolve_collision_cosmic_conflict(
        self, ship, hit_function, sprite_group, score_increment
    ):
        """Helper method used to help for checking collisions in the Cosmic
        Conflict game mode."""
        hits = get_colliding_sprites(ship, sprite_group)
        for sprite in hits:
            if not ship.state.immune:
                if isinstance(sprite, Missile):
                    sprite.explode()
                    play_sound(self.game.sound_manager.game_sounds, "missile")
                self._update_cosmic_conflict_scores(ship, hit_function, score_increment)

    def check_cosmic_conflict_collisions(self, thunderbird_hit, phoenix_hit):
        """Respond to PVP projectile collisions."""
        self._resolve_collision_cosmic_conflict(
            self.phoenix_ship, phoenix_hit, self.game.thunderbird_bullets, 1000
        )
        self._resolve_collision_cosmic_conflict(
            self.thunderbird_ship, thunderbird_hit, self.game.phoenix_bullets, 1000
        )
        self._resolve_collision_cosmic_conflict(
            self.phoenix_ship, phoenix_hit, self.game.thunderbird_missiles, 1000
        )
        self._resolve_collision_cosmic_conflict(
            self.thunderbird_ship, thunderbird_hit, self.game.phoenix_missiles, 1000
        )
        self._resolve_collision_cosmic_conflict(
            self.phoenix_ship, phoenix_hit, self.game.thunderbird_laser, 1000
        )
        self._resolve_collision_cosmic_conflict(
            self.thunderbird_ship, thunderbird_hit, self.game.phoenix_laser, 1000
        )

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
                self._decrease_player_scores()
                break

    def _decrease_player_scores(self):
        if not self.game.singleplayer:
            self.stats.phoenix_score = max(self.stats.phoenix_score - 100, 0)
        self.stats.thunderbird_score = max(self.stats.thunderbird_score - 100, 0)
        self.score_board.render_scores()
        self.score_board.update_high_score()

    def check_missile_alien_collisions(self):
        """Respond to missiles-alien collisions."""
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

    def check_laser_alien_collisions(self):
        """Respond to player laser-alien collisions."""
        laser_collisions = {
            self.game.thunderbird_laser: "thunderbird",
            self.game.phoenix_laser: "phoenix",
        }

        for laser, player in laser_collisions.items():
            collided_aliens = pygame.sprite.groupcollide(
                laser, self.game.aliens, False, False
            )

            for aliens in collided_aliens.values():
                for alien in aliens:
                    if isinstance(alien, BossAlien):
                        self._handle_boss_collisions_with_laser(alien, player)
                    elif not alien.immune_state:
                        self._update_stats(alien, player)

    def _handle_boss_collisions_with_laser(self, alien, player):
        """Handle collision between player's laser and a boss alien."""
        current_time = time.time()
        if current_time - alien.last_hit_time >= 0.2:
            alien.hit_count += 1
            alien.last_hit_time = current_time
            self._handle_boss_alien_collision(alien, player)

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
        """Manages collisions between alien bullets and players."""
        player_ships = (
            {self.thunderbird_ship: thunder_hit_method}
            if self.game.singleplayer
            else {
                self.thunderbird_ship: thunder_hit_method,
                self.phoenix_ship: phoenix_hit_method,
            }
        )

        for ship, hit_method in player_ships.items():
            self._handle_ship_alien_bullet_collision(ship, hit_method)

    def _handle_ship_alien_bullet_collision(self, ship, hit_method):
        """Handle collision between ship and alien bullet."""
        if ship.state.alive and not ship.state.immune:
            if collision := pygame.sprite.spritecollideany(
                ship, self.game.alien_bullet
            ):
                self._process_ship_bullet_collision(ship, hit_method, collision)

    def _process_ship_bullet_collision(self, ship, hit_method, collision):
        """Process collision between ship and alien bullet."""
        hit_method()
        collision.kill()

    def _handle_boss_alien_collision(self, boss, player):
        """Handles the collision between the player and the bosses."""
        if boss.hit_count >= self.settings.boss_hp and boss.is_alive:
            self._destroy_boss_alien(boss, player)
            self._update_player_score(player)

    def _destroy_boss_alien(self, boss, player):
        """Destroy the boss alien and update game stats."""
        boss.destroy_alien()
        self.game.aliens.remove(boss)
        play_sound(self.game.sound_manager.game_sounds, "boss_exploding")

    def _update_player_score(self, player):
        """Update player's score based on the boss points."""
        if player == "thunderbird":
            self.stats.thunderbird_score += self.settings.boss_points
        else:
            self.stats.phoenix_score += self.settings.boss_points

        self.score_board.render_scores()
        self.score_board.update_high_score()

    def _handle_alien_hits(self, player_ship_collisions, player):
        """Handles what happens with the score and the aliens after they have been hit."""
        max_hit_count = ALIENS_HP_MAP.get(self.stats.level, 3)

        for aliens in player_ship_collisions.values():
            for alien in aliens:
                self._update_alien_hit_count(alien, player, max_hit_count)

    def _update_alien_hit_count(self, alien, player, max_hit_count):
        """Update alien hit count and handle consequences."""
        alien.hit_count += 1
        if isinstance(alien, BossAlien):
            self._handle_boss_alien_collision(alien, player)
        elif not alien.immune_state and alien.is_baby:
            self._update_stats(alien, player)
        elif not alien.immune_state and alien.hit_count >= max_hit_count:
            self._update_stats(alien, player)

    def _update_stats(self, alien, player):
        """Update player score and remove alien."""
        match player:
            case "thunderbird":
                self.stats.thunderbird_score += self.settings.alien_points
                self.thunderbird_ship.aliens_killed += 1
            case "phoenix":
                self.stats.phoenix_score += self.settings.alien_points
                self.phoenix_ship.aliens_killed += 1

        alien.destroy_alien()
        play_sound(self.game.sound_manager.game_sounds, "alien_exploding")
        self.game.aliens.remove(alien)

        self.score_board.render_scores()
        self.score_board.update_high_score()

    def _check_missile_ex_collision(self, aliens, player, missile):
        """Check collisions between aliens and missile explosion."""
        for ex_frame in missile.destroy_anim.ex_frames:
            ex_rect = ex_frame.get_rect(center=missile.rect.center)
            self._handle_missile_explosion_collision(aliens, player, missile, ex_rect)

    def _handle_missile_explosion_collision(self, aliens, player, missile, ex_rect):
        """Handle collision between missile explosion and aliens."""
        for alien in aliens:
            if isinstance(alien, BossAlien):
                self._hande_missile_explosion_with_bosses(alien, player, missile)
            elif ex_rect.colliderect(alien.rect):
                self._update_stats(alien, player)

    def _hande_missile_explosion_with_bosses(self, alien, player, missile):
        """Handle collision between missile explosion and bosses."""
        if (missile, alien) not in self.handled_collisions:
            play_sound(self.game.sound_manager.game_sounds, "missile")
            alien.hit_count += 5
            self._handle_boss_alien_collision(alien, player)
            self.handled_collisions[(missile, alien)] = True
