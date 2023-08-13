"""
The 'aliens_manager' module contains the AliensManager class that manages
the creation and update of aliens and bosses in the game.
"""

from src.entities.alien_entities.aliens import Alien, BossAlien


class AliensManager:
    """ "Manages the creation, update of a fleet of aliens
    and bosses in a game.
    """

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

        # Create the full fleet of aliens.
        for row_number in range(rows):
            for alien_number in range(self.settings.aliens_num):
                alien = Alien(self)
                alien.rect.x = alien_width + 2 * alien_width * alien_number
                alien.rect.y = 50 - (2 * alien_height * row_number)

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
        """Check if any aliens have reached an edge and respond appropriately."""
        for alien in self.aliens.sprites():
            self._handle_alien_edge(alien)

    def _handle_alien_edge(self, alien):
        """Handle the edge behavior of a single alien."""
        if isinstance(alien, BossAlien):
            self._handle_boss_alien_edge(alien)
        else:
            self._handle_regular_alien_edge(alien)

    def _handle_boss_alien_edge(self, boss_alien):
        """Handle edge behavior for a boss alien."""
        if boss_alien.check_edges():
            boss_alien.motion.direction *= -1

    def _handle_regular_alien_edge(self, regular_alien):
        """Handle edge behavior for a regular alien."""
        if regular_alien.check_edges():
            regular_alien.motion.direction *= -1
        elif regular_alien.check_top_edges():
            regular_alien.rect.y += self.settings.alien_speed
