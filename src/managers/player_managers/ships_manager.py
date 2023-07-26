"""
The 'ships_manager' module contains the ShipsManager class which manages the ships in the game.
It handles operations related to player ships, such as responding to hits, updating ship stats, 
maintaining ship states, and resetting ships.
"""

from src.entities.player_entities.player_ships import Thunderbird, Phoenix
from src.utils.game_utils import play_sound


class ShipsManager:
    """The ShipsManager class manages the player's ships in the game."""

    def __init__(self, game, settings, singleplayer):
        self.game = game
        self.settings = settings
        self.screen = game.screen
        self.singleplayer = singleplayer

        self.thunderbird_ship = Thunderbird(self)
        self.phoenix_ship = Phoenix(self)

    def thunderbird_ship_hit(self):
        """Respond to the Thunderbird ship being hit."""
        if self.game.stats.thunderbird_hp >= 0:
            self._destroy_ship(self.thunderbird_ship)

    def phoenix_ship_hit(self):
        """Respond to the Phoenix ship being hit."""
        if self.game.stats.phoenix_hp >= 0:
            self._destroy_ship(self.phoenix_ship)

    def _destroy_ship(self, ship):
        """Destroy the given ship."""
        ship.explode()
        play_sound(self.game.sound_manager.game_sounds, "explode")
        ship.state.shielded = False

        if ship == self.thunderbird_ship:
            self._update_thunderbird_stats()
        elif ship == self.phoenix_ship:
            self._update_phoenix_stats()

        ship.set_immune()
        ship.center_ship()

        self.game.score_board.create_health()

        if self.settings.game_modes.last_bullet:
            self.game.gameplay_manager.check_remaining_bullets()

    def _update_thunderbird_stats(self):
        """Update Thunderbird ship stats after destruction."""
        self.settings.thunderbird_bullet_count -= (
            2 if self.settings.thunderbird_bullet_count >= 3 else 0
        )
        self.settings.thunderbird_bullets_allowed -= (
            1 if self.settings.thunderbird_bullets_allowed > 3 else 0
        )
        self.game.stats.thunderbird_hp -= 1

    def _update_phoenix_stats(self):
        """Update Phoenix ship stats after destruction."""
        self.settings.phoenix_bullet_count -= (
            2 if self.settings.phoenix_bullet_count >= 3 else 0
        )
        self.settings.phoenix_bullets_allowed -= (
            1 if self.settings.phoenix_bullets_allowed > 3 else 0
        )
        self.game.stats.phoenix_hp -= 1

    def update_ship_alive_states(self):
        """Update the alive state of each ship."""
        if (
            self.game.stats.thunderbird_hp < 0
            and not self.thunderbird_ship.state.exploding
        ):
            self.thunderbird_ship.state.alive = False

        if self.game.stats.phoenix_hp < 0 and not self.phoenix_ship.state.exploding:
            self.phoenix_ship.state.alive = False

    def reset_ships(self):
        """Resets ships to their initial state, updates missiles number,
        resets the player weapon and plays the warp sound effect."""
        for ship in self.game.ships:
            ship.reset_ship_size()
            ship.center_ship()
            ship.start_warp()
            ship.set_cosmic_conflict_pos()

            if not self.game.game_loaded:
                ship.reset_ship_state()
                ship.update_missiles_number()
    
                self.game.weapons_manager.reset_weapons()
                self.game.score_board.render_missiles_num()

        play_sound(self.game.sound_manager.game_sounds, "warp")

    def update_ship_state(self):
        """Update the state for the ships."""
        for ship in self.game.ships:
            ship.update_state()
