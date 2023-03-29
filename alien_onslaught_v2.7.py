"""The Alien Onslaught game module contains the multiplayer and singleplayer versions of the game.
This module imports all other classes and modules required to run the game.


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

from utils.game_utils import display_high_scores
from utils.constants import (
    DIFFICULTIES, GAME_CONSTANTS,
<<<<<<< HEAD
    BOSS_LEVELS, AVAILABLE_BULLETS_MAP,
    AVAILABLE_BULLETS_MAP_SINGLE,
=======
    BOSS_LEVELS, BULLETS_AVAILABLE
>>>>>>> 3034d0c87f65fb882db55122af241e8ee7958458
)

from ui.screen_manager import ScreenManager
from ui.scoreboards import ScoreBoard, SecondScoreBoard
from ui.game_buttons import GameButtons

from entities.ships import Thunderbird, Phoenix
from entities.alien_bullets import AlienBulletsManager
from entities.aliens import AliensManager
from entities.power_ups import PowerUpsManager
from entities.asteroid import AsteroidsManager


class AlienOnslaught:
    """Overall class to manage game assets and behavior for the multiplayer version."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                self.settings.screen_height), pygame.RESIZABLE)
        self.bg_img = pygame.transform.smoothscale(self.settings.bg_img,
                                                            self.screen.get_size())
        self.bg_img_rect = self.bg_img.get_rect()
        self.reset_bg = self.bg_img.copy()
        self.second_bg = pygame.transform.smoothscale(self.settings.second_bg,
                                                            self.screen.get_size())
        self.third_bg = pygame.transform.smoothscale(self.settings.third_bg,
                                                            self.screen.get_size())
        self.ui_options = self.settings.ui_options
        self._initialize_game_objects()
        self.ships = [self.thunderbird_ship, self.phoenix_ship]

        # Initialize game state variables
        self.last_increase_time, self.last_level_time, self.pause_time = 0, 0, 0

        pygame.display.set_caption("Alien Onslaught")


    def _initialize_game_objects(self):
        """Initializes all game objects and managers/handlers required for the game."""
        self.thunderbird_ship = Thunderbird(self)
        self.phoenix_ship = Phoenix(self)
        self.buttons = GameButtons(self, self.screen, self.ui_options, self.settings.gm)
        self.stats = GameStats(self, self.phoenix_ship, self.thunderbird_ship)
        self.score_board = ScoreBoard(self)
        # Sprite Groups
        self.thunderbird_bullets = pygame.sprite.Group()
        self.phoenix_bullets = pygame.sprite.Group()
        self.alien_bullet = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        # Managers and handlers
        self.manage_screen = ScreenManager(self.settings, self.score_board,
                                        self.buttons, self.screen)
        self.player_input = PlayerInput(self, self.ui_options)
        self.collision_handler = CollisionManager(self)
        self.power_ups_manager = PowerUpsManager(self)
        self.asteroids_manager = AsteroidsManager(self)
        self.alien_bullets_manager = AlienBulletsManager(self)
        self.aliens_manager = AliensManager(self, self.aliens, self.settings, self.screen)
        self.gm_manager = GameModesManager(self, self.settings, self.stats)

    def run_menu(self):
        """Runs the menu screen"""
        self.screen = pygame.display.set_mode(self.screen.get_size())
        while True:
            # Check for mouse click events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.buttons.single.rect.collidepoint(mouse_x, mouse_y):
                        # Start single player game
                        single_player_game = SingleplayerAlienOnslaught()
                        single_player_game.run_game()
                    elif self.buttons.multi.rect.collidepoint(mouse_x, mouse_y):
                        # Start multiplayer game
                        multiplayer_game = AlienOnslaught()
                        multiplayer_game.run_game()
                    elif self.buttons.menu_quit.rect.collidepoint(mouse_x, mouse_y):
                        # Quit menu
                        pygame.quit()
                        sys.exit()

            # Draw the buttons and controls on the screen
            self.screen.blit(self.bg_img, self.bg_img_rect)
            self.screen.blit(self.buttons.p1_controls, self.buttons.p1_controls_rect)
            self.screen.blit(self.buttons.p2_controls, self.buttons.p2_controls_rect)
            self.screen.blit(self.settings.game_title, self.settings.game_title_rect)
            self.buttons.single.draw_button()
            self.buttons.multi.draw_button()
            self.buttons.menu_quit.draw_button()

            for i, surface in enumerate(self.buttons.t1_surfaces):
                self.screen.blit(surface, self.buttons.t1_rects[i])

            for i, surface in enumerate(self.buttons.t2_surfaces):
                self.screen.blit(surface, self.buttons.t2_rects[i])

            pygame.display.flip()


    def run_game(self):
        """Main loop for the game."""
        running = True
        i = 0
        while running:
            if not self.ui_options.paused:  # check if the game is paused
                self._handle_background_change()
                self.screen.blit(self.bg_img, [0, i])
                self.screen.blit(self.bg_img, [0, i  - self.settings.screen_height])
                if i >= self.settings.screen_height:
                    i = 0
                i += 1

                self.check_events()
                self._check_game_over()
                self._check_for_resize()

                if self.stats.game_active:
                    self._handle_game_logic()


                self._update_screen()
                self._check_for_pause()
                self.clock.tick(60)


    def _handle_game_logic(self):
        """Handle the game logic for each game iteration."""
        self.start_game_mode()
        self._handle_level_progression()
        self._handle_normal_game()

        self.power_ups_manager.create_power_ups()
        self.power_ups_manager.update_power_ups()
        self.collision_handler.check_power_ups_collisions(
                                self._power_up_player, self._health_power_up)

        self.alien_bullets_manager.update_alien_bullets()
        self.collision_handler.check_alien_bullets_collisions(
                                self._thunderbird_ship_hit, self._phoenix_ship_hit)

        self._update_bullets()
        self.collision_handler.check_bullet_alien_collisions()
        self.aliens_manager.update_aliens(self._thunderbird_ship_hit, self._phoenix_ship_hit)

        self.thunderbird_ship.update_state()
        self.phoenix_ship.update_state()

        self.collision_handler.shield_collisions(self.ships, self.aliens,
                                 self.alien_bullet, self.asteroids)



    def _handle_level_progression(self):
        """Handles the progression of levels in the game, for different game modes."""
        if self.settings.gm.boss_rush and self.stats.level == 16:
            self.stats.game_active = False
            return

        if self.settings.gm.last_bullet and not self.aliens:
            self._prepare_last_bullet_level()

        if not self.settings.gm.meteor_madness and not self.aliens:
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
                                    event, self._fire_bullet,
                                    self._reset_game, self.run_menu)
            elif event.type == pygame.KEYUP:
                if self.stats.game_active:
                    self.player_input.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)
                self.manage_screen.update_buttons()

    def kill_aliens(self):
        for alien in self.aliens.sprites():
            alien.kill()


    def _create_button_actions_dict(self):
        """Create a dictionary mapping buttons to their corresponding actions."""
        return {
            self.buttons.play: lambda: self.buttons.handle_play_button(self._reset_game),
            self.buttons.quit: self.buttons.handle_quit_button,
            self.buttons.menu: self.run_menu,
            self.buttons.high_scores: self.buttons.handle_high_scores_button,
            self.buttons.game_modes: self.buttons.handle_game_modes_button,
            self.buttons.endless: self.buttons.handle_endless_button,
            self.buttons.meteor_madness: self.buttons.handle_meteor_madness_button,
            self.buttons.boss_rush: self.buttons.handle_boss_rush_button,
            self.buttons.last_bullet: self.buttons.handle_last_bullet_button,
            self.buttons.slow_burn: self.buttons.handle_slow_burn_button,
            self.buttons.normal: self.buttons.handle_normal_button,
            self.buttons.easy: self.buttons.handle_difficulty_button(DIFFICULTIES['EASY']),
            self.buttons.medium: self.buttons.handle_difficulty_button(DIFFICULTIES['MEDIUM']),
            self.buttons.hard: self.buttons.handle_difficulty_button(DIFFICULTIES['HARD']),
            self.buttons.difficulty: self.buttons.handle_difficulty_toggle
        }


    def _check_buttons(self, mouse_pos):
        """Check for buttons being clicked and act accordingly."""
        button_actions = self._create_button_actions_dict()
        for button, action in button_actions.items():
            if button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
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
        self.bg_img = pygame.transform.smoothscale(self.settings.bg_img, self.screen.get_size())
        self.second_bg = pygame.transform.smoothscale(self.settings.second_bg,
                                                                self.screen.get_size())
        self.third_bg = pygame.transform.smoothscale(self.settings.third_bg,
                                                               self.screen.get_size())
        self.reset_bg = pygame.transform.smoothscale(self.settings.bg_img,
                                                      self.screen.get_size())

        self._set_game_over()
        self.thunderbird_ship.screen_rect = self.screen.get_rect()
        self.phoenix_ship.screen_rect = self.screen.get_rect()


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
        """Change the background for different levels."""
        bg_images = {
            1: self.reset_bg,
            9: self.second_bg,
            17: self.third_bg,
        }
        self.bg_img = bg_images.get(self.stats.level, self.bg_img)


    def _check_for_pause(self):
        """Check if the game is paused and update pause time."""
        if self.ui_options.paused:
            self.pause_start_time = pygame.time.get_ticks()
            while self.ui_options.paused:
                self.check_events()
                if not self.ui_options.paused:
                    self.pause_end_time = pygame.time.get_ticks()
                    self.pause_time += self.pause_end_time - self.pause_start_time
                    break


    def _handle_asteroids(self, create_when_7=True, always=False):
        """Create, update, and check collisions for asteroids.
        Args:
            create_when_7 (bool, optional): Whether to create asteroids when 
            the current level is 7 or above.
            Defaults to True.
            always (bool, optional): Whether to always create and update asteroids.
              Defaults to False."""
        if always or (create_when_7 and self.stats.level >= 7):
            self.asteroids_manager.create_asteroids()
            self.asteroids_manager.update_asteroids()
            self.collision_handler.check_asteroids_collisions(self._thunderbird_ship_hit,
                                                                self._phoenix_ship_hit)

    def _handle_boss_stats(self):
        """Updates stats for bosses based on the game mode."""
        if self.settings.gm.boss_rush:
            self.gm_manager.update_boss_rush_info()
            return
        self.gm_manager.update_normal_boss_info()


    def _handle_normal_game(self):
        """Handle behaviors for different levels."""
        self._handle_asteroids(create_when_7=True)
        self.gm_manager.create_normal_level_bullets(self.alien_bullets_manager.create_alien_bullets)


    def start_game_mode(self):
        """Starts the selected game mode."""
        if self.settings.gm.endless_onslaught:
            self.gm_manager.endless_onslaught(
                self.aliens_manager.create_fleet, self._handle_asteroids)
        elif self.settings.gm.slow_burn:
            self.gm_manager.slow_burn(self._handle_asteroids)
        elif self.settings.gm.boss_rush:
            self.gm_manager.boss_rush(
                self._handle_asteroids, self.alien_bullets_manager.create_alien_bullets)
        elif self.settings.gm.meteor_madness:
            self.gm_manager.meteor_madness(
                        self.asteroids_manager.create_asteroids,
                        self.asteroids_manager.update_asteroids,
                        self.collision_handler.check_asteroids_collisions,
                        self._prepare_asteroids_level,
                        self._thunderbird_ship_hit,
                        self._phoenix_ship_hit)
        elif self.settings.gm.last_bullet:
            self.gm_manager.last_bullet(self.thunderbird_ship, self.phoenix_ship)


    def _handle_alien_creation(self):
        """Choose what aliens to create for every game mode."""
        # Don't create any aliens in Meteor Madness
        if self.settings.gm.meteor_madness:
            return

        # If Boss Rush game mode, create boss_aliens and return.
        if self.settings.gm.boss_rush:
            self.aliens_manager.create_boss_alien()
            return

        if self.settings.gm.last_bullet:
            self.aliens_manager.create_fleet(self.settings.last_bullet_rows)
<<<<<<< HEAD
=======
            for ship in self.ships:
                ship.remaining_bullets = BULLETS_AVAILABLE
            self.score_board.render_bullets_num()
>>>>>>> 3034d0c87f65fb882db55122af241e8ee7958458
            return

        # Create Bosses at the specified levels.
        if self.stats.level in BOSS_LEVELS:
            self.aliens_manager.create_boss_alien()

        # Create normal fleets of aliens.
        else:
            self.aliens_manager.create_fleet(self.settings.fleet_rows)


    def _fire_bullet(self, bullets, bullets_allowed, bullet_class, num_bullets, ship):
        """Create new player bullets."""
        # Create the bullets at and position them correctly as the number of bullets increases
        if len(bullets) < bullets_allowed:
            offset_amount = 25
            for i in range(num_bullets):
                new_bullet = bullet_class(self)
                bullets.add(new_bullet)
                offset_x = offset_amount * (i - (num_bullets - 1) / 2)
                offset_y = offset_amount * (i - (num_bullets - 1) / 2)
                new_bullet.rect.centerx = ship.rect.centerx + offset_x
                new_bullet.rect.centery = ship.rect.centery + offset_y
                if self.settings.gm.last_bullet:
                    ship.remaining_bullets -= 1
                    self.score_board.render_bullets_num()


    def _update_bullets(self):
        """Update position of bullets and get rid of bullets that went of screen."""
        self.thunderbird_bullets.update()
        self.phoenix_bullets.update()

        # Get rid of bullets that went off screen.
        for bullet in self.thunderbird_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.thunderbird_bullets.remove(bullet)

        for bullet in self.phoenix_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.phoenix_bullets.remove(bullet)


    def _power_up_player(self, player):
        """Powers up the specified player"""
        # each lambda function performs a different power up on the player.
        power_up_choices = [
            lambda: setattr(self.settings, f"{player}_ship_speed",
                             getattr(self.settings, f"{player}_ship_speed") + 0.3),
            lambda: setattr(self.settings, f"{player}_bullet_speed",
                             getattr(self.settings, f"{player}_bullet_speed") + 0.3),
            lambda: setattr(self.settings, f"{player}_bullets_allowed",
                             getattr(self.settings, f"{player}_bullets_allowed") + 2),
            lambda: setattr(self.settings, f"{player}_bullet_count",
                             getattr(self.settings, f"{player}_bullet_count") + 1),
            lambda: getattr(self, f"{player}_ship").draw_shield(),
            lambda: setattr(self.settings, "alien_speed",
                        getattr(self.settings, "alien_speed") - 0.1) \
                        if self.settings.alien_speed > 0 else None,
            lambda: setattr(self.settings, "alien_bullet_speed",
                        getattr(self.settings, "alien_bullet_speed") - 0.1) \
                        if self.settings.alien_bullet_speed > 0 else None,

        ]
        # randomly select one of the power ups and activate it.
        power_up_choice = random.choice(power_up_choices)
        power_up_choice()


    def _health_power_up(self, player):
        """Increases the health of the specified player"""
        player_health_attr = {
            "thunderbird": "thunderbird_hp",
            "phoenix": "phoenix_hp",
        }
        if getattr(self.stats, player_health_attr[player]) < self.stats.max_hp:
            setattr(self.stats, player_health_attr[player],
                     getattr(self.stats, player_health_attr[player]) + 1)
        self.score_board.create_health()


    def _thunderbird_ship_hit(self):
        """Respond to the Thunderbird ship being hit by an alien, bullet or asteroid."""
        if self.thunderbird_ship.state.exploding:
            return

        if self.stats.thunderbird_hp:
            self._destroy_thunderbird()
            self.thunderbird_ship.set_immune()
        else:
            # player becomes inactive when loses all hp
            self.thunderbird_ship.state.alive = False
            # if the other player is active, remove bullets and continue
            # until both players are dead
            if self.phoenix_ship.state.alive:
                return
            else:
                # game over if both player are inactive.
                self.stats.game_active = False


    def _destroy_thunderbird(self):
        """Destroy the thunderbird ship then center it."""
        self.thunderbird_ship.explode()
        self.thunderbird_ship.state.shielded = False
        self.settings.thunderbird_bullet_count = 1
        if self.settings.thunderbird_bullets_allowed > 1:
            self.settings.thunderbird_bullets_allowed -= 2
        self.stats.thunderbird_hp -= 1

        self.thunderbird_ship.center_ship()
        self.score_board.create_health()


    def _phoenix_ship_hit(self):
        """Respond to the Phoenix ship being hit by an alien, bullet or asteroid."""
        if self.phoenix_ship.state.exploding:
            return

        if self.stats.phoenix_hp:
            self._destroy_phoenix()
            self.phoenix_ship.set_immune()
        else:
            # player becomes inactive when loses all hp
            self.phoenix_ship.state.alive = False
            # if the other player is active, remove bullets and continue
            # until both players are dead
            if self.thunderbird_ship.state.alive:
                return
            else:
                # game over if both players are inactive.
                self.stats.game_active = False


    def _destroy_phoenix(self):
        """Destroy the Phoenix ship and center it."""
        self.phoenix_ship.explode()
        self.phoenix_ship.state.shielded = False
        self.settings.phoenix_bullet_count = 1
        if self.settings.phoenix_bullets_allowed > 1:
            self.settings.phoenix_bullets_allowed -= 2
        self.stats.phoenix_hp -= 1

        self.phoenix_ship.center_ship()
        self.score_board.create_health()


    def _check_game_over(self):
        """Check if the game is over and if so, display the game over image"""
        if self.settings.gm.boss_rush and self.stats.level == 16:
            self._display_game_over()
            self.score_board.render_high_score()
        elif not any([self.stats.game_active, self.thunderbird_ship.state.alive,
                     self.phoenix_ship.state.alive]):
            self._display_game_over()


    def _display_game_over(self):
        """Display the game over on screen and save the high score
        for the active game mode"""
        self._set_game_over()
        self.screen.blit(self.settings.game_over, self.game_over_rect)
        self._reset_game_objects()
        self.score_board.update_high_score()

        if not self.ui_options.high_score_saved:
            game_mode_high_score_keys = {
                'boss_rush': 'boss_rush_scores',
                'endless_onslaught': 'endless_scores',
                'meteor_madness': 'meteor_madness_scores',
                'slow_burn': 'slow_burn_scores',
                'last_bullet': 'last_bullet_scores',
                'normal': 'high_scores'
            }
            game_mode = self.settings.gm.game_mode or 'normal'
            high_score_key = game_mode_high_score_keys.get(game_mode, 'high_scores')
            self.score_board.save_high_score(high_score_key)
            self.ui_options.high_score_saved = True


    def _set_game_over(self):
        """Set the location of the game over image on the screen"""
        game_over_rect = self.settings.game_over.get_rect()
        game_over_x = (self.settings.screen_width - game_over_rect.width) / 2
        game_over_y = (self.settings.screen_height - game_over_rect.height) / 2 - 200
        self.game_over_rect = pygame.Rect(game_over_x, game_over_y,
                                        game_over_rect.width, game_over_rect.height)


    def _prepare_next_level(self):
        """Level progression handler"""
        self.thunderbird_bullets.empty()
        self.phoenix_bullets.empty()
        self.alien_bullet.empty()
        self.power_ups.empty()
        self.asteroids.empty()


        self.settings.increase_speed()
        self.stats.increase_level()
        self.score_board.prep_level()
        self._handle_alien_creation()
        self._handle_boss_stats()


    def _prepare_last_bullet_level(self):
        """Level progression handler for the Last Bullet game mode"""
        self.thunderbird_bullets.empty()
        self.phoenix_bullets.empty()
        self.alien_bullet.empty()
        self.power_ups.empty()
        self.asteroids.empty()

        self.settings.increase_speed()
        self.stats.increase_level()
        self.score_board.prep_level()
        self._handle_alien_creation()
        self._prepare_last_bullet_bullets()


    def _prepare_asteroids_level(self):
        """Level progression handler for the Meteor Madness game mode."""
        self.asteroids.empty()

        if self.settings.asteroid_speed < GAME_CONSTANTS['MAX_AS_SPEED']:
            self.settings.asteroid_speed += 0.3
        if self.settings.asteroid_freq > GAME_CONSTANTS['MAX_AS_FREQ']:
            self.settings.asteroid_freq -= 100
        self.settings.thunderbird_ship_speed = max(2.0,
                                                    self.settings.thunderbird_ship_speed - 0.2)
        self.settings.phoenix_ship_speed = max(2.0, self.settings.phoenix_ship_speed - 0.2)
        self.stats.thunderbird_score += 2000
        self.score_board.update_high_score()

        self.stats.increase_level()
        self.score_board.prep_level()
        self.score_board.render_high_score()


    def _reset_game_objects(self):
        """Clear the screen of game objects."""
        self.thunderbird_bullets.empty()
        self.phoenix_bullets.empty()
        self.alien_bullet.empty()
        self.power_ups.empty()
        self.aliens.empty()
        self.asteroids.empty()


    def _reset_ships(self):
        """Reset the ships by playing the warp animation and centering them."""
        self.thunderbird_ship.start_warp()
        self.phoenix_ship.start_warp()
        self.thunderbird_ship.center_ship()
        self.phoenix_ship.center_ship()


    def _display_pause(self):
        """Display the Pause image on screen."""
        pause_rect = self.settings.pause.get_rect()
        pause_rect.centerx = self.screen.get_rect().centerx
        pause_rect.centery = self.screen.get_rect().centery
        self.screen.blit(self.settings.pause, pause_rect)


    def _display_high_scores_on_screen(self):
        """Display the high scores for the current game mode active"""
        game_mode_high_score_keys = {
                'boss_rush': 'boss_rush_scores',
                'endless_onslaught': 'endless_scores',
                'meteor_madness': 'meteor_madness_scores',
                'slow_burn': 'slow_burn_scores',
                'last_bullet': 'last_bullet_scores',
                'normal': 'high_scores',
            }
        game_mode = self.settings.gm.game_mode or 'normal'
        high_score_key = game_mode_high_score_keys[game_mode]
        display_high_scores(self.screen, high_score_key)


    def _reset_game(self):
        # Reset the game statistics.
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.settings.dynamic_settings()
        self.stats.game_active = True
        self.ui_options.high_score_saved = False

        # Prepare the scoreboard and health.
        self.score_board.render_scores()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.create_health()

        # Clear the screen of remaining aliens, bullets, asteroids and power-ups.
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


    def _prepare_last_bullet_bullets(self):
        """Prepare the number of bullets in the Last Bullet game mode
        based on the level"""
        available_bullets = AVAILABLE_BULLETS_MAP.get(self.stats.level, 50)

        for ship in self.ships:
            ship.remaining_bullets = available_bullets

        self.score_board.render_bullets_num()


    def _draw_game_objects(self):
        """Draw game objects and the score on screen."""
        self.thunderbird_ship.blitme()
        self.phoenix_ship.blitme()

        for bullet in self.thunderbird_bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.phoenix_bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.alien_bullet.sprites():
            bullet.draw_bullet()

        for power_up in self.power_ups.sprites():
            power_up.draw_powerup()

        for asteroid in self.asteroids.sprites():
            asteroid.draw_asteroid()

        self.aliens.draw(self.screen)
        self.score_board.show_score()


    def _draw_buttons(self):
        """Draw buttons on screen"""
        self.buttons.play.draw_button()
        self.buttons.quit.draw_button()
        self.buttons.menu.draw_button()
        self.buttons.difficulty.draw_button()
        self.buttons.high_scores.draw_button()
        self.buttons.game_modes.draw_button()


    def _draw_difficulty_buttons(self):
        """Draw difficulty buttons on screen."""
        self.buttons.easy.draw_button()
        self.buttons.medium.draw_button()
        self.buttons.hard.draw_button()


    def _draw_game_mode_buttons(self):
        """Draw game mode buttons on screen."""
        self.buttons.endless.draw_button()
        self.buttons.normal.draw_button()
        self.buttons.slow_burn.draw_button()
        self.buttons.meteor_madness.draw_button()
        self.buttons.boss_rush.draw_button()
        self.buttons.last_bullet.draw_button()


    def _update_screen(self):
        """Update images on the screen"""
        # Draw game objects if game is active
        if self.stats.game_active:
            self._draw_game_objects()

            if self.ui_options.paused:
                self._display_pause()

        else:
            # Draw buttons if game is not active
            self._draw_buttons()

            if self.ui_options.show_difficulty:
                self._draw_difficulty_buttons()

            if self.ui_options.show_high_scores:
                self._display_high_scores_on_screen()

            if self.ui_options.show_game_modes:
                self._draw_game_mode_buttons()

        pygame.display.flip()




class SingleplayerAlienOnslaught(AlienOnslaught):
    """A class that manages the Singleplayer version of the game"""
    def __init__(self):
        super().__init__()
        self.score_board = SecondScoreBoard(self)
        self.clock = pygame.time.Clock()
        self.thunderbird_ship = Thunderbird(self, singleplayer=True)
        self.thunderbird_ship.state.single_player = True
        self.ships = [self.thunderbird_ship]
        self.player_input = PlayerInput(self, self.ui_options)
        self.collision_handler = CollisionManager(self)
        self.manage_screen = ScreenManager(self.settings, self.score_board,
                                        self.buttons, self.screen)


    def _handle_game_logic(self):
        """Handle game logic"""
        self.start_game_mode()
        self._handle_normal_game()
        self._handle_level_progression()

        self.power_ups_manager.create_power_ups()
        self.power_ups_manager.update_power_ups()
        self.collision_handler.check_power_ups_collisions(
                                self._power_up_player, self._health_power_up)

        self.alien_bullets_manager.update_alien_bullets()
        self.collision_handler.check_alien_bullets_collisions(
                                self._thunderbird_ship_hit, self._phoenix_ship_hit)

        self._update_bullets()

        self.collision_handler.check_bullet_alien_collisions(singleplayer=True)
        self.aliens_manager.update_aliens(self._thunderbird_ship_hit, self._phoenix_ship_hit)

        self.thunderbird_ship.update_state()
        self.collision_handler.shield_collisions(self.ships, self.aliens,
                                 self.alien_bullet, self.asteroids)


    def check_events(self):
        """Respond to keypresses, mouse and videoresize events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.stats.game_active:
                    self.player_input.check_keydown_events(
                            event, self._fire_bullet,
                            self._reset_game, self.run_menu, singleplayer=True)
            elif event.type == pygame.KEYUP:
                if self.stats.game_active:
                    self.player_input.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)
                self.manage_screen.update_buttons()


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.thunderbird_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.thunderbird_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.thunderbird_bullets.remove(bullet)


    def _prepare_next_level(self):
        """Handle level progression"""
        self.power_ups.empty()
        self.alien_bullet.empty()
        self.asteroids.empty()
        self.thunderbird_bullets.empty()

        self.settings.increase_speed()
        # Increase level.
        self.stats.increase_level()
        self.score_board.prep_level()
        self._handle_alien_creation()
        self._handle_boss_stats()


    def _thunderbird_ship_hit(self):
<<<<<<< HEAD
        """Respond to the Thunderbird ship being hit"""
=======
        """Respond to the Thunderbird ship being hit by an alien."""
>>>>>>> 3034d0c87f65fb882db55122af241e8ee7958458
        if self.thunderbird_ship.state.exploding:
            return

        if self.stats.thunderbird_hp:
            self._destroy_thunderbird()
            self.thunderbird_ship.set_immune()
        else:
            self.thunderbird_ship.state.alive = False
            self.stats.game_active = False


    def _prepare_last_bullet_bullets(self):
        available_bullets = AVAILABLE_BULLETS_MAP_SINGLE.get(self.stats.level, 50)

        for ship in self.ships:
            ship.remaining_bullets = available_bullets

        self.score_board.render_bullets_num()


    def _reset_game(self):
        # Reset the game statistics.
        self.stats.reset_stats(self.phoenix_ship, self.thunderbird_ship)
        self.phoenix_ship.state.alive = False
        self.settings.dynamic_settings()
        self.stats.game_active = True
        self.ui_options.high_score_saved = False

        self.score_board.render_scores()
        self.score_board.render_high_score()
        self.score_board.prep_level()
        self.score_board.render_bullets_num()
        self.score_board.create_health()

        # Clear the screen of remaining aliens, bullets, asteroids and power ups
        self.thunderbird_bullets.empty()
        self.alien_bullet.empty()
        self.power_ups.empty()
        self.aliens.empty()
        self.asteroids.empty()

        # Create a new fleet and center the ship.
        self.thunderbird_ship.start_warp()
        self.thunderbird_ship.center_ship()
        self.player_input.reset_ship_movement_flags()

        self._handle_alien_creation()
        self._prepare_last_bullet_bullets()

        self._handle_boss_stats()

        # This resets self.last_level_time when a new game starts.
        self.last_level_time = pygame.time.get_ticks()


    def _draw_game_objects(self):
        """Draw game objects on screen"""
        self.thunderbird_ship.blitme()

        for bullet in self.thunderbird_bullets.sprites():
            bullet.draw_bullet()

        for power_up in self.power_ups.sprites():
            power_up.draw_powerup()

        for bullet in self.alien_bullet.sprites():
            bullet.draw_bullet()

        for asteroid in self.asteroids.sprites():
            asteroid.draw_asteroid()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.score_board.show_score()


    def _update_screen(self):
        """Update images on the screen"""
        # Draw game objects if game is active
        if self.stats.game_active:
            self._draw_game_objects()

            if self.ui_options.paused:
                self._display_pause()

        else:
            # Draw buttons if game is not active
            self._draw_buttons()

            if self.ui_options.show_difficulty:
                self._draw_difficulty_buttons()

            if self.ui_options.show_high_scores:
                self._display_high_scores_on_screen()

            if self.ui_options.show_game_modes:
                self._draw_game_mode_buttons()

        pygame.display.flip()


if __name__ =='__main__':
    start = AlienOnslaught()
    start.run_menu()
