"""
This module imports all other classes and modules required to run the game.

Game description:
    - Alien-Onslaught is an action-packed space shooter game that challenges
your shooting skills and reflexes. You'll have to take on fleets of aliens
to progress through increasingly challenging levels and earn a high score.
As you play, be sure to collect ship power-ups that will enhance your gameplay.
The game contains variety of game modes, including Boss Rush and Endless Onslaught,
as well as both single-player and multiplayer.

Author: [Miron Alexandru]
Contact: quality_xqs@yahoo.com

"""

import sys
import random
import pygame

from game_logic.game_settings import Settings
from game_logic.game_stats import GameStats
from game_logic.collision_detection import CollisionManager
from game_logic.input_handling import PlayerInput
from game_logic.game_modes import GameModesManager

from utils.game_utils import display_high_scores, resize_image, play_sound
from utils.constants import (
    BOSS_LEVELS,
    AVAILABLE_BULLETS_MAP,
    AVAILABLE_BULLETS_MAP_SINGLE,
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
from entities.projectiles import BulletsManager
from audio.sounds_manager import SoundManager


class AlienOnslaught:
    """Overall class to manage game assets and behavior for the multiplayer version."""

    def __init__(self, singleplayer=False):
        """Initialize the game, and create game resources."""
        pygame.init()
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
        self._initialize_game_objects()
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.last_increase_time = self.last_level_time = self.pause_time = 0

        pygame.display.set_caption("Alien Onslaught")

    def _initialize_game_objects(self):
        """Initializes all game objects and managers/handlers required for the game."""
        self.thunderbird_ship = Thunderbird(self)
        self.phoenix_ship = Phoenix(self)
        self.buttons = GameButtons(
            self, self.screen, self.ui_options, self.settings.game_modes
        )
        self.stats = GameStats(self, self.phoenix_ship, self.thunderbird_ship)
        self.score_board = ScoreBoard(self)

        # Sprite Groups
        self.thunderbird_bullets = pygame.sprite.Group()
        self.phoenix_bullets = pygame.sprite.Group()
        self.thunderbird_missiles = pygame.sprite.Group()
        self.phoenix_missiles = pygame.sprite.Group()
        self.alien_bullet = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        # Managers and handlers
        self.screen_manager = ScreenManager(
            self.settings, self.score_board, self.buttons, self.screen
        )
        self.player_input = PlayerInput(self, self.ui_options)
        self.collision_handler = CollisionManager(self)
        self.powers_manager = PowerEffectsManager(self, self.score_board, self.stats)
        self.asteroids_manager = AsteroidsManager(self)
        self.alien_bullets_manager = AlienBulletsManager(self)
        self.bullets_manager = BulletsManager(self)
        self.aliens_manager = AliensManager(
            self, self.aliens, self.settings, self.screen
        )
        self.gm_manager = GameModesManager(self, self.settings, self.stats)
        self.loading_screen = LoadingScreen(
            self.screen, self.settings.screen_width, self.settings.screen_height
        )
        self.sound_manager = SoundManager(self)

    def run_menu(self):
        """Run the main menu screen"""
        self.sound_manager.load_sounds("menu_sounds")
        pygame.mixer.stop()
        play_sound(self.sound_manager.menu_sounds, "menu", loop=True)
        while True:
            self.handle_menu_events()
            self.draw_menu_objects()
            self.screen_manager.draw_cursor()
            pygame.display.flip()

    def handle_menu_events(self):
        """Handles events for the menu screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

    def draw_menu_objects(self):
        """Draw the buttons, game title and controls on the menu screen"""
        self.screen.blit(self.bg_img, self.bg_img_rect)
        self.screen.blit(
            self.screen_manager.p1_controls, self.screen_manager.p1_controls_rect
        )
        self.screen.blit(
            self.screen_manager.p2_controls, self.screen_manager.p2_controls_rect
        )
        self.screen.blit(self.settings.game_title, self.settings.game_title_rect)
        self.buttons.single.draw_button()
        self.buttons.multi.draw_button()
        self.buttons.menu_quit.draw_button()

        for i, surface in enumerate(self.screen_manager.t1_surfaces):
            self.screen.blit(surface, self.screen_manager.t1_rects[i])

        for i, surface in enumerate(self.screen_manager.t2_surfaces):
            self.screen.blit(surface, self.screen_manager.t2_rects[i])

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

    def _start_game(self):
        """Initialize the game."""
        self.sound_manager.load_sounds("level_sounds")
        self.ui_options.paused = False
        self.sound_manager.current_sound = None
        self.run_game()

    def _set_singleplayer_variables(self):
        """Set variables for the singleplayer game mode."""
        self.thunderbird_ship.state.single_player = True
        self.ships = [self.thunderbird_ship]
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.score_board.update_high_score_filename()
        self.gm_manager.reset_cosmic_conflict()

    def _set_multiplayer_variables(self):
        """Set variables for the multiplayer game mode."""
        self.thunderbird_ship.state.single_player = False
        self.ships = [self.thunderbird_ship, self.phoenix_ship]
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.score_board.update_high_score_filename()

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
            self._check_for_resize()

            if self.stats.game_active:
                if not self.ui_options.paused:  # check if the game is paused
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
        self._handle_level_progression()

        self.powers_manager.manage_power_downs()
        self.powers_manager.create_powers()
        self.powers_manager.update_powers()
        self.collision_handler.check_powers_collisions(
            self._apply_powerup_or_penalty, self._health_power_up, self._weapon_power_up
        )

        self.gm_manager.create_normal_level_bullets(
            self.alien_bullets_manager.create_alien_bullets
        )
        self.alien_bullets_manager.update_alien_bullets()
        self.collision_handler.check_alien_bullets_collisions(
            self._thunderbird_ship_hit, self._phoenix_ship_hit
        )
        self.player_input.handle_ship_firing(self._fire_bullet)
        self.bullets_manager.update_projectiles()
        self.collision_handler.check_bullet_alien_collisions()
        self.collision_handler.check_missile_alien_collisions()
        self.aliens_manager.update_aliens()
        self.collision_handler.check_alien_ship_collisions(
            self._thunderbird_ship_hit, self._phoenix_ship_hit
        )

        self.update_ship_state()

        self.collision_handler.shield_collisions(
            self.ships, self.aliens, self.alien_bullet, self.asteroids
        )

    def _handle_level_progression(self):
        """Handles the progression of levels in the game for different game modes."""
        if not self.aliens:
            if self.settings.game_modes.last_bullet:
                self._prepare_last_bullet_level()
            elif not self.settings.game_modes.meteor_madness and not self.settings.game_modes.cosmic_conflict:
                self._prepare_next_level()

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
                        self._fire_missile,
                    )
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
            self.run_menu, self._reset_game, self._reset_game_single
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

        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.bg_img = resize_image(self.settings.bg_img)
        self.second_bg = resize_image(self.settings.second_bg)
        self.third_bg = resize_image(self.settings.third_bg)
        self.fourth_bg = resize_image(self.settings.fourth_bg)
        self.reset_bg = resize_image(self.settings.bg_img)

        self._set_game_end_position()
        for ship in self.ships:
            ship.screen_rect = self.screen.get_rect()
            ship.set_cosmic_conflict_pos()

    def _check_for_resize(self):
        """Choose when the window is resizable."""
        # the game window is resizable before clicking the Play button
        # players can't resize the window while the game is active.
        info = pygame.display.Info()
        if not self.stats.game_active and not self.ui_options.resizable:
            pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
            self.ui_options.resizable = True
        elif self.stats.game_active and self.ui_options.resizable:
            pygame.display.set_mode((info.current_w, info.current_h))
            self.ui_options.resizable = False

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

    def _handle_asteroids(self, start_at_level_7=True, always=False):
        """Create, update, and check collisions for asteroids.
        Args:
        start_at_level_7 (bool, optional): Whether to create asteroids when
        the current level is 7 or above.
        Defaults to True.
        always (bool, optional): Whether to always create and update asteroids.
        Defaults to False."""
        if always or (start_at_level_7 and self.stats.level >= 7):
            self.asteroids_manager.create_asteroids()
            self.asteroids_manager.update_asteroids()
            self.collision_handler.check_asteroids_collisions(
                self._thunderbird_ship_hit, self._phoenix_ship_hit
            )

    def _handle_boss_stats(self):
        """Updates stats for bosses based on the game mode."""
        if self.settings.game_modes.boss_rush:
            self.gm_manager.update_boss_rush_info()
            return

        self.gm_manager.update_normal_boss_info()

    def apply_game_behaviors(self):
        """Applies the game behaviors for the currently selected game mode."""
        if self.settings.game_modes.endless_onslaught:
            self.gm_manager.endless_onslaught(
                self.aliens_manager.create_fleet, self._handle_asteroids
            )
        elif self.settings.game_modes.slow_burn:
            self.gm_manager.slow_burn(self._handle_asteroids)
        elif self.settings.game_modes.boss_rush:
            self.gm_manager.boss_rush(
                self._handle_asteroids, self.alien_bullets_manager.create_alien_bullets
            )
        elif self.settings.game_modes.meteor_madness:
            self.gm_manager.meteor_madness(
                self.asteroids_manager.create_asteroids,
                self.asteroids_manager.update_asteroids,
                self.collision_handler.check_asteroids_collisions,
                self._thunderbird_ship_hit,
                self._phoenix_ship_hit,
            )
        elif self.settings.game_modes.last_bullet:
            self.gm_manager.last_bullet(
                self.thunderbird_ship, self.phoenix_ship, self._handle_asteroids
            )
        elif self.settings.game_modes.cosmic_conflict:
            self.gm_manager.cosmic_conflict(
                self.collision_handler.check_cosmic_conflict_collisions,
                 self._thunderbird_ship_hit,
                 self._phoenix_ship_hit
            )
        else:
            self._handle_asteroids(
                start_at_level_7=True
            )  # Handle asteroids for normal game

    def _handle_alien_creation(self):
        """Choose what aliens to create for every game mode."""
        match self.settings.game_modes.game_mode:
            case "cosmic_conflict":
                return
            case "meteor_madness":
                return
            case "boss_rush":
                self.aliens_manager.create_boss_alien()
                self.collision_handler.handled_collisions.clear()  # clear missile collisions dict
            case "last_bullet":
                self.aliens_manager.create_fleet(self.settings.last_bullet_rows)
            case _ if self.stats.level in BOSS_LEVELS:
                self.aliens_manager.create_boss_alien()
                self.collision_handler.handled_collisions.clear()  # clear missile collisions dict
            case _:
                self.aliens_manager.create_fleet(self.settings.fleet_rows)

    def _fire_bullet(self, bullets, bullets_allowed, bullet_class, num_bullets, ship):
        """Create new player bullets."""
        # Create the bullets at and position them correctly as the number of bullets increases
        if ship.remaining_bullets <= 0 or ship.state.disarmed:
            return

        bullet_fired = False
        if len(bullets) < bullets_allowed:
            new_bullets = [bullet_class(self, ship) for _ in range(num_bullets)]
            bullets.add(new_bullets)
            for i, new_bullet in enumerate(new_bullets):
                offset = 30 * (i - (num_bullets - 1) / 2)
                new_bullet.rect.centerx = ship.rect.centerx + offset
                new_bullet.rect.centery = ship.rect.centery + offset
                if self.settings.game_modes.last_bullet:
                    ship.remaining_bullets -= 1
                    self.score_board.render_bullets_num()
                bullet_fired = True

        if bullet_fired:
            play_sound(self.sound_manager.game_sounds, "bullet")

    def _fire_missile(self, missiles, ship, missile_class):
        """Fire a missile from the given ship and update the missiles number."""
        if ship.missiles_num > 0:
            new_missile = missile_class(self, ship)
            play_sound(self.sound_manager.game_sounds, "missile_launch")
            missiles.add(new_missile)
            ship.missiles_num -= 1
            self.score_board.render_scores()

    def _apply_powerup_or_penalty(self, player):
        """Powers up or applies a penalty on the specified player"""
        powerup_choices = self.powers_manager.get_powerup_choices()
        penalty_choices = self.powers_manager.get_penalty_choices()
        # randomly select one of the powers and activate it.
        effect_choice = random.choice(powerup_choices + penalty_choices)
        effect_choice(player)

        # Play sound effect
        if effect_choice in powerup_choices:
            play_sound(self.sound_manager.game_sounds, "power_up")
        elif effect_choice in penalty_choices:
            play_sound(self.sound_manager.game_sounds, "penalty")

    def _health_power_up(self, player):
        """Increases the health of the specified player"""
        player_health_attr = {
            "thunderbird": "thunderbird_hp",
            "phoenix": "phoenix_hp",
        }
        if getattr(self.stats, player_health_attr[player]) < self.stats.max_hp:
            setattr(
                self.stats,
                player_health_attr[player],
                getattr(self.stats, player_health_attr[player]) + 1,
            )
        self.score_board.create_health()
        play_sound(self.sound_manager.game_sounds, "health")

    def _weapon_power_up(self, player, weapon_name):
        """Changes the given player's weapon."""
        self.bullets_manager.set_weapon(player, weapon_name)
        play_sound(self.sound_manager.game_sounds, "weapon")

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
            if self.settings.thunderbird_bullet_count >= 3:
                self.settings.thunderbird_bullet_count -= 2
            if self.settings.thunderbird_bullets_allowed > 3:
                self.settings.thunderbird_bullets_allowed -= 1
            self.stats.thunderbird_hp -= 1
        elif ship == self.phoenix_ship:
            if self.settings.phoenix_bullet_count >= 3:
                self.settings.phoenix_bullet_count -= 2
            if self.settings.phoenix_bullets_allowed > 3:
                self.settings.phoenix_bullets_allowed -= 1
            self.stats.phoenix_hp -= 1

        ship.center_ship()
        self.score_board.create_health()
        ship.set_immune()

    def _check_game_over(self):
        """Check if the game is over and act accordingly."""
        if self.settings.game_modes.cosmic_conflict:
            self._check_cosmic_conflict_endgame()
        if self.settings.game_modes.boss_rush and self.stats.level == 15 and not self.aliens:
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
        self._reset_game_objects()
        self.score_board.update_high_score()

        if not self.ui_options.game_over_sound_played:
            pygame.mixer.stop()
            play_sound(self.sound_manager.game_sounds, "game_over", loop=True)
            self.ui_options.game_over_sound_played = True
            self.sound_manager.current_sound = self.sound_manager.game_sounds[
                "game_over"
            ]

        if self.settings.game_modes.cosmic_conflict:
            self.gm_manager.set_cosmic_conflict_high_score()

        self._check_high_score_saved()

    def _return_to_game_menu(self):
        """End the current game, save the current high score and return to game menu."""
        self.stats.game_active = False
        self._reset_game_objects()

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

    def _prepare_level(self):
        """Common level progression handler"""
        self._reset_game_objects()
        self.settings.increase_speed()
        self.stats.increase_level()
        self.score_board.prep_level()
        self._handle_alien_creation()
        self.sound_manager.prepare_level_music()
        self.gm_manager.set_max_alien_bullets(self.settings.speedup_scale)
        self.gm_manager.check_alien_bullets_num()

    def _prepare_next_level(self):
        """Level progression handler"""
        self._prepare_level()
        self._handle_boss_stats()

    def _prepare_last_bullet_level(self):
        """Level progression handler for the Last Bullet game mode"""
        self._prepare_level()
        self._prepare_last_bullet_bullets()


    def _reset_game_objects(self, *exclude_groups):
        """Clear the screen of game objects, excluding specified groups."""
        all_groups = [
            self.thunderbird_bullets,
            self.phoenix_bullets,
            self.alien_bullet,
            self.powers,
            self.aliens,
            self.asteroids,
            self.thunderbird_missiles,
            self.phoenix_missiles,
        ]
        for group in all_groups:
            if group not in exclude_groups:
                group.empty()

    def _reset_ships(self):
        """Resets ships to their initial state, updates missiles number,
        resets the player weapon and plays the warp sound effect."""
        for ship in self.ships:
            ship.reset_ship_state()
            ship.center_ship()
            ship.start_warp()
            ship.update_missiles_number()
            ship.set_cosmic_conflict_pos()
        # reset player weapons
        self.bullets_manager.reset_weapons()

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

        # Clear the screen of remaining aliens, bullets, asteroids and powers.
        self._reset_game_objects()

        # Play the warp animation and center the ships.
        self._reset_ships()

        self.player_input.reset_ship_movement_flags()

        # Create aliens
        self._handle_alien_creation()
        self._prepare_last_bullet_bullets()
        self._handle_boss_stats()

        # for resetting self.last_level_time when a new game starts.
        self.last_level_time = pygame.time.get_ticks()

        # Prepare the scoreboard
        self.score_board.render_scores()
        self.score_board.render_bullets_num()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.create_health()
        # Prepare sounds
        self.sound_manager.prepare_level_music()
        play_sound(self.sound_manager.game_sounds, "warp")

    def _reset_game_single(self):
        """Start a new game in singleplayer."""
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.phoenix_ship.state.alive = False
        self.settings.dynamic_settings()
        self.stats.game_active = True
        self.ui_options.high_score_saved = False
        self.ui_options.game_over_sound_played = False

        # Clear the screen of remaining aliens, bullets, asteroids and powers
        self._reset_game_objects(self.phoenix_bullets)

        # Reset ships
        self._reset_ships()
        self.player_input.reset_ship_movement_flags()
        # Handle alien creation.
        self._handle_alien_creation()
        self._prepare_last_bullet_bullets()
        self._handle_boss_stats()

        # This resets self.last_level_time when a new game starts.
        self.last_level_time = pygame.time.get_ticks()
        # Prepare scoreboard
        self.score_board.render_scores()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.render_bullets_num()
        self.score_board.create_health()
        # Prepare sound
        self.sound_manager.prepare_level_music()
        play_sound(self.sound_manager.game_sounds, "warp")

    def _prepare_last_bullet_bullets(self):
        """Prepare the number of bullets in the Last Bullet game mode
        based on the level"""
        level = self.stats.level
        available_bullets = (
            AVAILABLE_BULLETS_MAP_SINGLE.get(level, 50)
            if self.singleplayer
            else AVAILABLE_BULLETS_MAP.get(level, 25)
        )
        for ship in self.ships:
            ship.remaining_bullets = available_bullets

        self.score_board.render_bullets_num()

    def _draw_game_objects(self):
        """Draw game objects and the score on screen."""
        for ship in self.ships:
            # Check the state of the Thunderbird and Phoenix ships and update their "alive" state.
            if ship == self.thunderbird_ship:
                health = self.stats.thunderbird_hp
            else:
                health = self.stats.phoenix_hp
            # The ship waits for the explosion anim to finish before changing it's alive state
            if health < 0 and not ship.state.exploding:
                ship.state.alive = False
            # Draw the ships on screen only when alive.
            if ship.state.alive:
                ship.blitme()

        sprite_groups = [
            self.thunderbird_bullets,
            self.thunderbird_missiles,
            self.phoenix_bullets,
            self.phoenix_missiles,
            self.alien_bullet,
            self.powers,
            self.asteroids,
        ]

        if self.singleplayer:
            # delete phoenix related sprite groups from the list in the singleplayer mode
            del sprite_groups[2:4]

        for group in sprite_groups:
            for sprite in group.sprites():
                sprite.draw()

        self.aliens.draw(self.screen)
        self.score_board.show_score()

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
