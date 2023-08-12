"""
This is the main module that imports all other classes and modules
required to run the game.

Short game description:
    - Alien Onslaught is an action-packed space shooter game that challenges
your shooting skills and reflexes. You'll have to take on fleets of aliens
to progress through increasingly challenging levels and earn a high score.
As you play, be sure to collect ship power-ups that will enhance your gameplay.
The game contains variety of game modes, including Boss Rush and Endless Onslaught,
as well as both single-player and multiplayer.

Author: [Miron Alexandru]
Contact: quality_xqs@yahoo.com

"""


import pygame

from src.game_logic.game_settings import Settings
from src.game_logic.game_stats import GameStats
from src.game_logic.collision_detection import CollisionManager
from src.game_logic.input_handling import PlayerInput
from src.game_logic.gameplay_handler import GameplayHandler

from src.utils.game_utils import (
    resize_image,
    play_sound,
    play_music,
)

from src.ui.scoreboards import ScoreBoard

from src.managers.powers_manager import PowerEffectsManager
from src.managers.asteroids_manager import AsteroidsManager
from src.managers.sounds_manager import SoundManager
from src.managers.game_over_manager import EndGameManager
from src.managers.alien_managers.alien_bullets_manager import AlienBulletsManager
from src.managers.alien_managers.aliens_manager import AliensManager
from src.managers.ui_managers.screen_manager import ScreenManager
from src.managers.ui_managers.loading_screen import LoadingScreen
from src.managers.ui_managers.buttons_manager import GameButtonsManager
from src.managers.player_managers.weapons_manager import WeaponsManager
from src.managers.high_score_manager import HighScoreManager
from src.managers.player_managers.ships_manager import ShipsManager
from src.managers.player_managers.ship_selection_manager import ShipSelection
from src.managers.save_load_manager import SaveLoadSystem


class AlienOnslaught:
    """Main class responsible for managing the game."""

    MENU_RUNNING = True
    GAME_RUNNING = True

    def __init__(self, singleplayer=False):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.singleplayer = singleplayer
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE
        )
        self.bg_img = resize_image(self.settings.bg_img, self.screen.get_size())
        self.bg_img_rect = self.bg_img.get_rect()
        self.reset_bg = self.bg_img.copy()

        self.second_bg = resize_image(self.settings.second_bg, self.screen.get_size())
        self.third_bg = resize_image(self.settings.third_bg, self.screen.get_size())
        self.fourth_bg = resize_image(self.settings.fourth_bg, self.screen.get_size())

        self.ui_options = self.settings.ui_options
        self.ships = []
        self._initialize_game_objects()
        self._initialize_sprite_groups()
        self.initialize_managers()

        self.pause_time = 0
        self.game_loaded = False

        pygame.display.set_icon(self.settings.game_icon)
        pygame.display.set_caption("Alien Onslaught")

    def _initialize_game_objects(self):
        """Initializes all game objects required."""
        self.ships_manager = ShipsManager(self, self.settings, self.singleplayer)
        self.thunderbird_ship = self.ships_manager.thunderbird_ship
        self.phoenix_ship = self.ships_manager.phoenix_ship
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.stats = GameStats(self, self.phoenix_ship, self.thunderbird_ship)
        self.score_board = ScoreBoard(self)
        self.loading_screen = LoadingScreen(self.screen)
        self.ship_selection = ShipSelection(
            self, self.screen, self.thunderbird_ship.anims.ship_images, self.settings
        )

    @property
    def singleplayer(self):
        """Getter for singleplayer attribute."""
        return self._singleplayer

    @singleplayer.setter
    def singleplayer(self, value):
        """Setter for singleplayer attribute."""
        self._singleplayer = value
        if hasattr(self, "ships_manager"):
            self.ships_manager.singleplayer = value
        if hasattr(self, "screen_manager"):
            self.screen_manager.singleplayer = value

    def _initialize_sprite_groups(self):
        """Create sprite groups for the game."""
        self.thunderbird_bullets = pygame.sprite.Group()
        self.phoenix_bullets = pygame.sprite.Group()
        self.thunderbird_missiles = pygame.sprite.Group()
        self.phoenix_missiles = pygame.sprite.Group()
        self.thunderbird_laser = pygame.sprite.Group()
        self.phoenix_laser = pygame.sprite.Group()
        self.alien_bullet = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.sprite_groups = [
            self.powers,
            self.aliens,
            self.thunderbird_bullets,
            self.thunderbird_missiles,
            self.thunderbird_laser,
            self.phoenix_bullets,
            self.phoenix_missiles,
            self.phoenix_laser,
            self.asteroids,
            self.alien_bullet,
        ]

        self.single_sprite_groups = [
            self.powers,
            self.aliens,
            self.thunderbird_bullets,
            self.thunderbird_missiles,
            self.thunderbird_laser,
            self.asteroids,
            self.alien_bullet,
        ]

    def initialize_managers(self):
        """Initialize the managers and handlers required."""
        self.sound_manager = SoundManager(self)
        self.buttons_manager = GameButtonsManager(
            self, self.screen, self.ui_options, self.settings.game_modes
        )
        self.screen_manager = ScreenManager(
            self,
            self.settings,
            self.score_board,
            self.buttons_manager,
            self.screen,
            self.singleplayer,
        )
        self.player_input = PlayerInput(self, self.ui_options)
        self.collision_handler = CollisionManager(self)
        self.powers_manager = PowerEffectsManager(self, self.score_board, self.stats)
        self.asteroids_manager = AsteroidsManager(self)
        self.alien_bullets_manager = AlienBulletsManager(self)
        self.weapons_manager = WeaponsManager(self)
        self.aliens_manager = AliensManager(
            self, self.aliens, self.settings, self.screen
        )
        self.gameplay_manager = GameplayHandler(self, self.settings, self.stats)
        self.game_over_manager = EndGameManager(
            self, self.settings, self.stats, self.screen
        )
        self.save_load_manager = SaveLoadSystem(self, "save", "save_data")
        self.high_score_manager = HighScoreManager(self)

    def run_menu(self):
        """Run the main menu."""
        self.sound_manager.load_sounds("menu_sounds")
        play_music(self.sound_manager.menu_music, "menu")
        while self.MENU_RUNNING:
            self.handle_menu_events()
            self.screen_manager.update_window_mode()
            self.screen_manager.draw_menu_objects(self.bg_img, self.bg_img_rect)
            self.screen_manager.draw_cursor()
            pygame.display.flip()

    def handle_menu_events(self):
        """Handles events for the main menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.buttons_manager.handle_quit_event()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.screen_manager.toggle_window_mode()
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_LEFT
            ):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.buttons_manager.single.rect.collidepoint(mouse_x, mouse_y):
                    self.buttons_manager.handle_single_player_button_click(
                        self.start_single_player_game
                    )
                elif self.buttons_manager.multi.rect.collidepoint(mouse_x, mouse_y):
                    self.buttons_manager.handle_multiplayer_button_click(
                        self.start_multiplayer_game
                    )
                elif self.buttons_manager.menu_quit.rect.collidepoint(mouse_x, mouse_y):
                    self.buttons_manager.handle_quit_button_click()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_menu_resize_screen_event(event.size)

    def handle_menu_resize_screen_event(self, size):
        """Handle the event to resize the menu screen."""
        self.screen_manager.resize_screen(size)
        self.screen_manager.update_buttons()
        self.screen_manager.create_controls()

    def start_single_player_game(self):
        """Switches the game to singleplayer."""
        self.singleplayer = True
        self._set_singleplayer_variables()
        self._start_game()

    def start_multiplayer_game(self):
        """Switches the game to multiplayer."""
        self.singleplayer = False
        self._set_multiplayer_variables()
        self._start_game()

    def _set_singleplayer_variables(self):
        """Set variables for the singleplayer game mode."""
        self.thunderbird_ship.state.single_player = True
        self.ships = [self.thunderbird_ship]
        self.high_score_manager.update_high_score_filename()
        self.gameplay_manager.reset_cosmic_conflict()

    def _set_multiplayer_variables(self):
        """Set variables for the multiplayer game mode."""
        self.thunderbird_ship.state.single_player = False
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.high_score_manager.update_high_score_filename()

    def _start_game(self):
        """Initialize the game."""
        self.sound_manager.load_sounds("gameplay_sounds")
        self.ui_options.paused = False
        self.sound_manager.current_sound = None
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.settings.disable_ui_flags()
        self.run_game()

    def _update_background(self, i):
        """Updates the background image of the game and scrolls it downwards
        to create the effect of movement"""
        self._handle_background_change()
        self.screen.blit(self.bg_img, [0, i])
        self.screen.blit(self.bg_img, [0, i - self.settings.screen_height])
        if i >= self.settings.screen_height:
            i = 0
        i += 1

        return i

    def run_game(self):
        """Run the main game loop."""
        i = 0
        while self.GAME_RUNNING:
            self.check_events()
            self.game_over_manager.check_game_over()
            self.screen_manager.update_window_mode()

            if self.stats.game_active:
                if not self.ui_options.paused:
                    i = self._update_background(i)
                    self._handle_game_logic()

                self._update_screen()
                self._check_for_pause()
            else:
                self.screen.blit(self.bg_img, [0, 0])
                self.game_over_manager.check_game_over()
                self._update_screen()
            self.clock.tick(60)

    def _handle_game_logic(self):
        """Call the functions that are handling the game logic."""
        self.apply_game_mode_behaviors()
        self.gameplay_manager.handle_level_progression()

        self.powers_manager.create_powers()
        self.powers_manager.update_powers()
        self.collision_handler.check_powers_collisions(
            self.powers_manager.apply_powerup_or_penalty,
            self.powers_manager.health_power_up,
            self.powers_manager.weapon_power_up,
        )
        self.powers_manager.manage_power_downs()
        self.powers_manager.display_powers_effect()

        self.gameplay_manager.create_normal_level_bullets(
            self.alien_bullets_manager.create_alien_bullets
        )
        self.alien_bullets_manager.update_alien_bullets()
        self.collision_handler.check_alien_bullets_collisions(
            self.ships_manager.thunderbird_ship_hit, self.ships_manager.phoenix_ship_hit
        )
        self.player_input.handle_ship_firing(self.weapons_manager.fire_bullet)
        self.weapons_manager.update_projectiles()
        self.collision_handler.check_bullet_alien_collisions()
        self.collision_handler.check_missile_alien_collisions()
        self.collision_handler.check_laser_alien_collisions()
        self.aliens_manager.update_aliens()
        self.collision_handler.check_alien_ship_collisions(
            self.ships_manager.thunderbird_ship_hit, self.ships_manager.phoenix_ship_hit
        )

        self.ships_manager.update_ship_state()
        self.weapons_manager.update_laser_status()
        self.weapons_manager.check_laser_availability()

        self.collision_handler.handle_shielded_ship_collisions(
            self.ships, self.aliens, self.alien_bullet, self.asteroids
        )

    def check_events(self):
        """Respond to keyboard, mouse and videoresize events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.buttons_manager.handle_quit_event()
            elif event.type == pygame.KEYDOWN:
                if self.stats.game_active:
                    self.player_input.check_keydown_events(
                        event,
                        self._reset_game,
                        self.run_menu,
                        self.game_over_manager.return_to_game_menu,
                        self.weapons_manager.fire_missile,
                        self.weapons_manager.fire_laser,
                    )
                if event.key == pygame.K_f:
                    self.screen_manager.toggle_window_mode()
            elif event.type == pygame.KEYUP:
                if self.stats.game_active:
                    self.player_input.check_keyup_events(event)
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_LEFT
            ):
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
                self.ship_selection.handle_ship_selection(mouse_pos)
            elif event.type == pygame.VIDEORESIZE:
                self.screen_manager.resize_screen(event.size)
                self.screen_manager.update_buttons()

    def _check_buttons(self, mouse_pos):
        """Check for UI buttons being clicked and act accordingly."""
        self.buttons_manager.handle_buttons_visibility()
        button_actions = self.buttons_manager.create_button_actions_dict(
            self.run_menu, self._reset_game
        )
        for button, action in button_actions.items():
            if (
                button.rect.collidepoint(mouse_pos)
                and not self.stats.game_active
                and not button.visible
            ):
                if button != self.buttons_manager.quit:
                    play_sound(self.sound_manager.game_sounds, "click")
                pygame.time.delay(200)
                action()

    def _handle_background_change(self):
        """Change the background image based on the level ranges."""
        bg_images = {
            range(1, 9): self.reset_bg,
            range(9, 17): self.second_bg,
            range(17, 26): self.third_bg,
        }

        for level_range, bg_image in bg_images.items():
            if self.stats.level in level_range:
                self.bg_img = bg_image
                break
        else:
            self.bg_img = self.fourth_bg if self.stats.level > 25 else self.bg_img

    def _check_for_pause(self):
        """Check if the game is paused and update pause time."""
        if self.ui_options.paused:
            pause_start_time = pygame.time.get_ticks()
            while self.ui_options.paused:
                self.check_events()
                if not self.ui_options.paused:
                    pause_end_time = pygame.time.get_ticks()
                    self.pause_time += pause_end_time - pause_start_time
                    break

    def apply_game_mode_behaviors(self):
        """Applies the game behaviors for the currently selected game mode."""
        game_modes = self.settings.game_modes
        if game_modes.endless_onslaught:
            self.gameplay_manager.endless_onslaught(
                self.aliens_manager.create_fleet,
                self.asteroids_manager.handle_asteroids,
            )
        elif game_modes.slow_burn:
            self.gameplay_manager.slow_burn(self.asteroids_manager.handle_asteroids)
        elif game_modes.boss_rush:
            self.gameplay_manager.boss_rush(
                self.asteroids_manager.handle_asteroids,
                self.alien_bullets_manager.create_alien_bullets,
            )
        elif game_modes.meteor_madness:
            self.gameplay_manager.meteor_madness(
                self.asteroids_manager.create_asteroids,
                self.asteroids_manager.update_asteroids,
                self.collision_handler.check_asteroids_collisions,
                self.ships_manager.thunderbird_ship_hit,
                self.ships_manager.phoenix_ship_hit,
            )
        elif game_modes.last_bullet:
            self.gameplay_manager.last_bullet(
                self.thunderbird_ship,
                self.phoenix_ship,
                self.asteroids_manager.handle_asteroids,
            )
        elif game_modes.cosmic_conflict:
            self.gameplay_manager.cosmic_conflict(
                self.collision_handler.check_cosmic_conflict_collisions,
                self.ships_manager.thunderbird_ship_hit,
                self.ships_manager.phoenix_ship_hit,
            )
        else:
            self.asteroids_manager.handle_asteroids(create_at_high_levels=True)

    def _reset_game(self):
        """Start a new game."""
        # Clear the screen of remaining entities
        self.gameplay_manager.reset_game_objects()

        # Check if a new game is started or loaded from a savefile
        self.check_game_loaded()

        # Set the appropriate flags
        self.stats.game_active = True
        self.ui_options.high_score_saved = False
        self.ui_options.game_over_sound_played = False

        # Play the warp animation and center the ships.
        self.player_input.reset_ship_flags()
        self.ships_manager.reset_ships()

        # Handle Aliens
        self.gameplay_manager.handle_boss_stats()

        # Handle bullets
        self.gameplay_manager.prepare_last_bullet_bullets()
        self.gameplay_manager.set_last_bullet_bullets()

        # Reset timed variables
        self.reset_timed_variables()

        # Prepare the scoreboard
        self.score_board.render_scores()
        self.score_board.render_missiles_num()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.create_health()

        # Prepare powers
        self.powers_manager.update_power_choices()

        # Prepare sounds
        self.sound_manager.prepare_level_music()
        play_sound(self.sound_manager.game_sounds, "warp")
        self.game_loaded = False

        if self.singleplayer:
            self.phoenix_ship.state.alive = False

    def check_game_loaded(self):
        """Check the state of the game load and
        perform appropriate actions accordingly.
        """
        if self.game_loaded:
            self.save_load_manager.update_alien_states()
            self.save_load_manager.update_player_ship_states()
            self.save_load_manager.update_player_weapon()
        else:
            self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
            self.settings.dynamic_settings()
            self.gameplay_manager.handle_alien_creation()

    def reset_timed_variables(self):
        """Resets timer-related variables for managing game events."""
        self.gameplay_manager.last_level_time = pygame.time.get_ticks()
        self.powers_manager.last_power_up_time = 0
        self.asteroids_manager.last_asteroid_time = 0

    def _draw_game_objects(self):
        """Draw game objects and the score on screen."""
        if self.singleplayer:
            sprite_groups = self.single_sprite_groups
        else:
            sprite_groups = self.sprite_groups

        self.ships_manager.update_ship_alive_states()

        for ship in self.ships:
            if ship.state.alive:
                ship.blitme()

        for group in sprite_groups:
            for sprite in group.sprites():
                sprite.draw()

        self.score_board.show_score()

    def _update_screen(self):
        """Update images on the screen"""
        if self.stats.game_active:
            self._draw_game_objects()

            if self.ui_options.paused:
                self.screen_manager.display_pause()

        else:
            self._update_game_screen_components()

        pygame.display.flip()

    def _update_game_screen_components(self):
        """Update and draw various components on the screen."""
        self.buttons_manager.draw_buttons()

        if self.ui_options.show_difficulty:
            self.buttons_manager.draw_difficulty_buttons()

        if self.ui_options.show_high_scores:
            self.screen_manager.display_high_scores_on_screen()
            self.buttons_manager.delete_scores.draw_button()

        if self.ui_options.show_game_modes:
            self.buttons_manager.draw_game_mode_buttons()

        if self.ui_options.ship_selection:
            self.ship_selection.draw()

        self.screen_manager.draw_cursor()


if __name__ == "__main__":
    start = AlienOnslaught()
    start.run_menu()
