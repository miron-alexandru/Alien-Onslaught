"""
This module imports all other classes and modules required to run the game.

Game description:
    - Alien Onslaught is an action-packed space shooter game that challenges
your shooting skills and reflexes. You'll have to take on fleets of aliens
to progress through increasingly challenging levels and earn a high score.
As you play, be sure to collect ship power-ups that will enhance your gameplay.
The game contains variety of game modes, including Boss Rush and Endless Onslaught,
as well as both single-player and multiplayer.

Author: [Miron Alexandru]
Contact: quality_xqs@yahoo.com

"""

import sys
import pygame

from game_logic.game_settings import Settings
from game_logic.game_stats import GameStats
from game_logic.collision_detection import CollisionManager
from game_logic.input_handling import PlayerInput
from game_logic.gameplay_handler import GameplayManager

from utils.game_utils import (
    display_high_scores,
    resize_image,
    play_sound,
)
from utils.constants import (
    GAME_MODE_SCORE_KEYS,
)

from ui.screen_manager import ScreenManager, LoadingScreen
from ui.scoreboards import ScoreBoard
from ui.game_buttons import GameButtons

from entities.ships import Thunderbird, Phoenix
from entities.alien_bullets import AlienBulletsManager
from entities.aliens import AliensManager
from entities.powers import PowerEffectsManager
from entities.asteroid import AsteroidsManager
from entities.projectiles import WeaponsManager
from audio.sounds_manager import SoundManager


class AlienOnslaught:
    """Overall class to manage game assets and behavior for the multiplayer version."""

    def __init__(self, singleplayer=False):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.singleplayer = singleplayer
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.full_screen = False
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
        self._initialize_game_objects()
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self._initialize_sprite_groups()
        self.initialize_managers()

        self.pause_time = 0

        pygame.display.set_icon(self.settings.game_icon)
        pygame.display.set_caption("Alien Onslaught")

    def _initialize_game_objects(self):
        """Initializes all game objects required in the game."""
        self.thunderbird_ship = Thunderbird(self)
        self.phoenix_ship = Phoenix(self)
        self.buttons = GameButtons(
            self, self.screen, self.ui_options, self.settings.game_modes
        )
        self.stats = GameStats(self, self.phoenix_ship, self.thunderbird_ship)
        self.score_board = ScoreBoard(self)
        self.loading_screen = LoadingScreen(self.screen)

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
            self.thunderbird_bullets,
            self.thunderbird_missiles,
            self.thunderbird_laser,
            self.asteroids,
            self.alien_bullet,
        ]

    def initialize_managers(self):
        """Initialize managers/handlers for the game."""
        self.sound_manager = SoundManager(self)
        self.screen_manager = ScreenManager(
            self, self.settings, self.score_board, self.buttons, self.screen
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
        self.gameplay_manager = GameplayManager(self, self.settings, self.stats)

    def run_menu(self):
        """Run the main menu screen"""
        self.sound_manager.load_sounds("menu_sounds")
        pygame.mixer.stop()
        play_sound(self.sound_manager.menu_sounds, "menu", loop=True)
        while True:
            self.handle_menu_events()
            self.screen_manager.update_window_mode()
            self.screen_manager.draw_menu_objects(self.bg_img, self.bg_img_rect)
            self.screen_manager.draw_cursor()
            pygame.display.flip()

    def handle_menu_events(self):
        """Handles events for the menu screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.screen_manager.toggle_window_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.buttons.single.rect.collidepoint(mouse_x, mouse_y):
                    play_sound(self.sound_manager.menu_sounds, "click_menu")
                    self.start_single_player_game()
                elif self.buttons.multi.rect.collidepoint(mouse_x, mouse_y):
                    play_sound(self.sound_manager.menu_sounds, "click_menu")
                    self.start_multiplayer_game()
                elif self.buttons.menu_quit.rect.collidepoint(mouse_x, mouse_y):
                    play_sound(self.sound_manager.menu_sounds, "quit_effect")
                    pygame.time.delay(800)
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)
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
        self.score_board.update_high_score_filename()
        self.gameplay_manager.reset_cosmic_conflict()

    def _set_multiplayer_variables(self):
        """Set variables for the multiplayer game mode."""
        self.thunderbird_ship.state.single_player = False
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.score_board.update_high_score_filename()

    def _start_game(self):
        """Initialize the game."""
        self.sound_manager.load_sounds("level_sounds")
        self.ui_options.paused = False
        self.sound_manager.current_sound = None
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
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
        """Main loop for the game."""
        running = True
        i = 0
        while running:
            self.check_events()
            self._check_game_over()
            self.screen_manager.update_window_mode()

            if self.stats.game_active:
                if not self.ui_options.paused:
                    i = self._update_background(i)
                    self._handle_game_logic()

                self._update_screen()
                self._check_for_pause()
            else:
                self.screen.blit(self.bg_img, [0, 0])
                self._check_game_over()
                self._update_screen()
            self.clock.tick(60)

    def _handle_game_logic(self):
        """Handle the game logic for each game iteration."""
        self.apply_game_behaviors()
        self.gameplay_manager.handle_level_progression()

        self.powers_manager.create_powers()
        self.powers_manager.update_powers()
        self.collision_handler.check_powers_collisions(
            self.powers_manager.apply_powerup_or_penalty,
            self.powers_manager.health_power_up,
            self.powers_manager.weapon_power_up,
        )
        self.powers_manager.manage_power_downs()

        self.gameplay_manager.create_normal_level_bullets(
            self.alien_bullets_manager.create_alien_bullets
        )
        self.alien_bullets_manager.update_alien_bullets()
        self.collision_handler.check_alien_bullets_collisions(
            self._thunderbird_ship_hit, self._phoenix_ship_hit
        )
        self.player_input.handle_ship_firing(self.weapons_manager.fire_bullet)
        self.weapons_manager.update_projectiles()
        self.collision_handler.check_bullet_alien_collisions()
        self.collision_handler.check_missile_alien_collisions()
        self.collision_handler.check_laser_alien_collisions()
        self.aliens_manager.update_aliens()
        self.collision_handler.check_alien_ship_collisions(
            self._thunderbird_ship_hit, self._phoenix_ship_hit
        )

        self.update_ship_state()
        self.weapons_manager.update_laser_status()
        self.weapons_manager.check_laser_availability()

        self.collision_handler.shield_collisions(
            self.ships, self.aliens, self.alien_bullet, self.asteroids
        )

    def check_events(self):
        """Respond to keypresses, mouse and videoresize events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.stats.game_active:
                    self.player_input.check_keydown_events(
                        event,
                        self._reset_game,
                        self.run_menu,
                        self._return_to_game_menu,
                        self.weapons_manager.fire_missile,
                        self.weapons_manager.fire_laser,
                    )
                if event.key == pygame.K_f:
                    self.screen_manager.toggle_window_mode()
            elif event.type == pygame.KEYUP:
                if self.stats.game_active:
                    self.player_input.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)
                self.screen_manager.update_buttons()

    def _check_buttons(self, mouse_pos):
        """Check for buttons being clicked and act accordingly."""
        self.buttons.handle_buttons_visibility()
        button_actions = self.buttons.create_button_actions_dict(
            self.run_menu, self._reset_game
        )
        for button, action in button_actions.items():
            if (
                button.rect.collidepoint(mouse_pos)
                and not self.stats.game_active
                and not button.visible
            ):
                if button != self.buttons.quit:
                    play_sound(self.sound_manager.game_sounds, "click")
                pygame.time.delay(200)
                action()

    def _resize_screen(self, size):
        """Resize the game screen and update relevant game objects.
        Screen has max width and max height."""
        min_width, min_height = 1260, 700
        max_width, max_height = 1920, 1080
        width = max(min(size[0], max_width), min_width)
        height = max(min(size[1], max_height), min_height)
        size = (width, height)

        self.screen = pygame.display.set_mode(size, self.screen_manager.screen_flag)

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.bg_img = resize_image(self.bg_img)
        self.second_bg = resize_image(self.settings.second_bg)
        self.third_bg = resize_image(self.settings.third_bg)
        self.fourth_bg = resize_image(self.settings.fourth_bg)
        self.reset_bg = resize_image(self.settings.bg_img)

        self._set_game_end_position()
        for ship in self.ships:
            ship.screen_rect = self.screen.get_rect()
            ship.set_cosmic_conflict_pos()

    def _handle_background_change(self):
        """Change the background image based on the current level."""
        bg_images = {
            1: self.reset_bg,
            9: self.second_bg,
            17: self.third_bg,
            25: self.fourth_bg,
        }

        self.bg_img = bg_images.get(self.stats.level, self.bg_img)

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

    def _handle_asteroids(self, create_at_high_levels=True, force_creation=False):
        """Create, update, and check collisions for asteroids.
        Args:
            create_at_high_levels (bool, optional): Whether to create asteroids when
                the current level is 7 or above. Defaults to True.
            force_creation (bool, optional): Whether to always create and update asteroids.
                Defaults to False.
        """
        if force_creation or (create_at_high_levels and self.stats.level >= 7):
            self.asteroids_manager.create_asteroids()
            self.asteroids_manager.update_asteroids()
            self.collision_handler.check_asteroids_collisions(
                self._thunderbird_ship_hit, self._phoenix_ship_hit
            )

    def apply_game_behaviors(self):
        """Applies the game behaviors for the currently selected game mode."""
        game_modes = self.settings.game_modes
        if game_modes.endless_onslaught:
            self.gameplay_manager.endless_onslaught(
                self.aliens_manager.create_fleet, self._handle_asteroids
            )
        elif game_modes.slow_burn:
            self.gameplay_manager.slow_burn(self._handle_asteroids)
        elif game_modes.boss_rush:
            self.gameplay_manager.boss_rush(
                self._handle_asteroids, self.alien_bullets_manager.create_alien_bullets
            )
        elif game_modes.meteor_madness:
            self.gameplay_manager.meteor_madness(
                self.asteroids_manager.create_asteroids,
                self.asteroids_manager.update_asteroids,
                self.collision_handler.check_asteroids_collisions,
                self._thunderbird_ship_hit,
                self._phoenix_ship_hit,
            )
        elif game_modes.last_bullet:
            self.gameplay_manager.last_bullet(
                self.thunderbird_ship, self.phoenix_ship, self._handle_asteroids
            )
        elif game_modes.cosmic_conflict:
            self.gameplay_manager.cosmic_conflict(
                self.collision_handler.check_cosmic_conflict_collisions,
                self._thunderbird_ship_hit,
                self._phoenix_ship_hit,
            )
        else:
            self._handle_asteroids(create_at_high_levels=True)

    def _thunderbird_ship_hit(self):
        """Respond to the Thunderbird ship being hit."""
        if self.stats.thunderbird_hp >= 0:
            self.destroy_ship(self.thunderbird_ship)

    def _phoenix_ship_hit(self):
        """Respond to the Phoenix ship being hit."""
        if self.stats.phoenix_hp >= 0:
            self.destroy_ship(self.phoenix_ship)

    def destroy_ship(self, ship):
        """Destroy the given ship."""
        ship.explode()
        play_sound(self.sound_manager.game_sounds, "explode")
        ship.state.shielded = False

        if ship == self.thunderbird_ship:
            self._update_thunderbird_stats()
        elif ship == self.phoenix_ship:
            self._update_phoenix_stats()

        ship.center_ship()
        self.score_board.create_health()
        ship.set_immune()

    def _update_thunderbird_stats(self):
        """Update Thunderbird ship stats after destruction."""
        self.settings.thunderbird_bullet_count -= (
            2 if self.settings.thunderbird_bullet_count >= 3 else 0
        )
        self.settings.thunderbird_bullets_allowed -= (
            1 if self.settings.thunderbird_bullets_allowed > 3 else 0
        )
        self.stats.thunderbird_hp -= 1

    def _update_phoenix_stats(self):
        """Update Phoenix ship stats after destruction."""
        self.settings.phoenix_bullet_count -= (
            2 if self.settings.phoenix_bullet_count >= 3 else 0
        )
        self.settings.phoenix_bullets_allowed -= (
            1 if self.settings.phoenix_bullets_allowed > 3 else 0
        )
        self.stats.phoenix_hp -= 1

    def _check_game_over(self):
        """Check if the game is over and act accordingly."""
        if self.settings.game_modes.cosmic_conflict:
            self._check_cosmic_conflict_endgame()
        if (
            self.settings.game_modes.boss_rush
            and self.stats.level == 15
            and not self.aliens
        ):
            self._display_endgame("victory")
            self.score_board.render_high_score()
        elif not any(
            [self.thunderbird_ship.state.alive, self.phoenix_ship.state.alive]
        ):
            self._display_endgame("gameover")

    def _display_game_over(self):
        """Display the end game image on screen play the game over sound
        and save the high score for the active game mode."""
        self.bg_img = self.reset_bg
        self._set_game_end_position()
        self.screen.blit(self.settings.game_end_img, self.settings.game_end_rect)
        self.gameplay_manager.reset_game_objects()
        self.score_board.update_high_score()

        if not self.ui_options.game_over_sound_played:
            pygame.mixer.stop()
            play_sound(self.sound_manager.game_sounds, "game_over", loop=True)
            self.ui_options.game_over_sound_played = True
            self.sound_manager.current_sound = self.sound_manager.game_sounds[
                "game_over"
            ]

        if self.settings.game_modes.cosmic_conflict:
            self.gameplay_manager.set_cosmic_conflict_high_score()

        self._check_high_score_saved()

    def _return_to_game_menu(self):
        """End the current game, save the current high score and return to game menu."""
        self.stats.game_active = False
        self.gameplay_manager.reset_game_objects()

    def _set_game_end_position(self):
        """Set the location of the end game image on the screen"""
        self.settings.game_end_rect.centerx = self.settings.screen_width // 2
        self.settings.game_end_rect.centery = self.settings.screen_height // 2 - 200

    def _display_endgame(self, image_name):
        self.stats.game_active = False
        self.settings.game_end_img = self.settings.misc_images[image_name]
        self._display_game_over()

    def _check_cosmic_conflict_endgame(self):
        """Check which player won in Cosmic Conflict
        and display the appropriate end game.
        """
        if not self.thunderbird_ship.state.alive:
            self._display_endgame("phoenix_win")
        elif not self.phoenix_ship.state.alive:
            self._display_endgame("thunder_win")

    def _reset_ships(self):
        """Resets ships to their initial state, updates missiles number,
        resets the player weapon and plays the warp sound effect."""
        for ship in self.ships:
            ship.reset_ship_state()
            ship.reset_ship_size()
            ship.center_ship()
            ship.start_warp()
            ship.update_missiles_number()
            ship.set_cosmic_conflict_pos()
        # reset player weapons
        self.weapons_manager.reset_weapons()

        play_sound(self.sound_manager.game_sounds, "warp")

    def _display_pause(self):
        """Display the pause screen."""
        pause_rect = self.settings.pause.get_rect()
        pause_rect.centerx = self.screen.get_rect().centerx
        pause_rect.centery = self.screen.get_rect().centery
        self.screen.blit(self.settings.pause, pause_rect)

    def _check_high_score_saved(self):
        """Save the high score for the current game_mode."""
        if not self.ui_options.high_score_saved:
            game_mode = self.settings.game_modes.game_mode or "normal"
            high_score_key = GAME_MODE_SCORE_KEYS.get(game_mode, "high_scores")
            self.score_board.save_high_score(high_score_key)
            self.ui_options.high_score_saved = True

    def _display_high_scores_on_screen(self):
        """Display the high scores for the current game mode active"""
        game_mode = self.settings.game_modes.game_mode or "normal"
        high_score_key = GAME_MODE_SCORE_KEYS[game_mode]
        display_high_scores(self, self.screen, high_score_key)

    def _reset_game(self):
        """Start a new game."""
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.settings.dynamic_settings()
        self.stats.game_active = True
        self.ui_options.high_score_saved = False
        self.ui_options.game_over_sound_played = False

        # Clear the screen of remaining aliens, bullets, asteroids, and powers.
        self.gameplay_manager.reset_game_objects()

        # Play the warp animation and center the ships.
        self._reset_ships()

        self.player_input.reset_ship_flags()

        # Handle Alien Creation
        self.gameplay_manager.handle_alien_creation()
        self.gameplay_manager.prepare_last_bullet_bullets()
        self.gameplay_manager.handle_boss_stats()

        # Reset self.last_level_time when a new game starts.
        self.reset_timed_variables()

        # Prepare the scoreboard
        self.score_board.render_scores()
        self.score_board.render_bullets_num()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.create_health()
        # Prepare sounds
        self.sound_manager.prepare_level_music()
        play_sound(self.sound_manager.game_sounds, "warp")

        if self.singleplayer:
            self.phoenix_ship.state.alive = False

    def reset_timed_variables(self):
        """Resets timer-related variables for managing game events."""
        self.gameplay_manager.last_level_time = pygame.time.get_ticks()
        self.powers_manager.last_power_up_time = 0
        self.asteroids_manager.last_asteroid_time = 0

    def _draw_game_objects(self):
        """Draw game objects and the score on screen."""
        self._update_ship_alive_states()

        for ship in self.ships:
            if ship.state.alive:
                ship.blitme()

        if self.singleplayer:
            sprite_groups = self.single_sprite_groups
        else:
            sprite_groups = self.sprite_groups

        for group in sprite_groups:
            for sprite in group.sprites():
                sprite.draw()

        self.aliens.draw(self.screen)
        self.score_board.show_score()

    def _update_ship_alive_states(self):
        if self.stats.thunderbird_hp < 0 and not self.thunderbird_ship.state.exploding:
            self.thunderbird_ship.state.alive = False

        if self.stats.phoenix_hp < 0 and not self.phoenix_ship.state.exploding:
            self.phoenix_ship.state.alive = False

    def update_ship_state(self):
        """Update the state for the ships."""
        for ship in self.ships:
            ship.update_state()

    def _update_screen(self):
        """Update images on the screen"""
        # Draw game objects if game is active
        if self.stats.game_active:
            self._draw_game_objects()

            if self.ui_options.paused:
                self._display_pause()

        else:
            # Draw buttons and cursor if game is not active
            self.buttons.draw_buttons()

            if self.ui_options.show_difficulty:
                self.buttons.draw_difficulty_buttons()

            if self.ui_options.show_high_scores:
                self._display_high_scores_on_screen()
                self.buttons.delete_scores.draw_button()

            if self.ui_options.show_game_modes:
                self.buttons.draw_game_mode_buttons()

            self.screen_manager.draw_cursor()

        pygame.display.flip()


if __name__ == "__main__":
    start = AlienOnslaught()
    start.run_menu()
