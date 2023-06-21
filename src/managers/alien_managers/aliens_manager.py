"""
The 'aliens_manager' module contains the AliensManager class that manages
the creation and update of aliens and bosses in the game.
"""

from src.entities.aliens import Alien, BossAlien


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

        # Calculate the starting y-coordinate for the first row of aliens
        start_y = 50

        # Create the full fleet of aliens.
        for row_number in range(rows):
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

    def update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Check if any aliens have reached an edge and respond
        appropriately by changing the direction and moving them down if needed.
        Boss aliens do not move down.
        """
        for alien in self.aliens.sprites():
            if isinstance(alien, BossAlien):
                if alien.check_edges():
                    alien.motion.direction *= -1
            elif alien.check_edges():
                alien.motion.direction *= -1
            elif alien.check_top_edges():
                alien.rect.y += self.settings.alien_speed
