"""
This module tests the AlienOnslaught main class that uses every module
necessary to run the game.
"""

import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, call

import pygame

from src.alien_onslaught import AlienOnslaught

from src.game_logic.game_settings import Settings
from src.game_logic.game_stats import GameStats
from src.game_logic.collision_detection import CollisionManager
from src.game_logic.input_handling import PlayerInput
from src.game_logic.gameplay_handler import GameplayHandler

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
from src.managers.player_managers.ships_manager import ShipsManager
from src.managers.save_load_manager import SaveLoadSystem

from src.entities.player_entities.player_ships import Thunderbird, Phoenix


class AlienOnslaughtTestCase(unittest.TestCase):
    """Test cases for the AlienOnslaught class."""

    def setUp(self):
        """Set up test environment."""
        # pygame.init()
        with patch("src.alien_onslaught.pygame.display.set_mode") as mock_display:
            mock_display.return_value = pygame.Surface((1280, 700))
            self.game = AlienOnslaught(singleplayer=False)
        self.game.sound_manager = MagicMock()
        self.game.screen_manager = MagicMock()
        self.game.ships_manager = MagicMock()
        self.game.weapons_manager = MagicMock()
        self.game.asteroids_manager = MagicMock()
        self.game.player_input = MagicMock()
        self.game.score_board = MagicMock()
        self.game.buttons_manager = MagicMock()
        self.game.game_over_manager = MagicMock()
        self.game.stats = MagicMock()
        self.game.gameplay_manager = MagicMock()
        self.game.powers_manager = MagicMock()
        self.game.collision_handler = MagicMock()
        self.game.alien_bullets_manager = MagicMock()
        self.game.aliens_manager = MagicMock()
        self.game.ship_selection = MagicMock()
        self.game.save_load_manager = MagicMock()
        self.game.high_score_manager = MagicMock()

    def tearDown(self):
        pygame.quit()

    @patch("src.alien_onslaught.pygame.display.set_icon")
    @patch("src.alien_onslaught.pygame.display.set_mode")
    def test_init_multiplayer(self, mock_display, mock_set_icon):
        """Test the initialization of AlienOnslaught in multiplayer mode."""
        mock_display.return_value = pygame.Surface((1280, 700))
        game = AlienOnslaught(singleplayer=False)

        # Assertions
        self.assertFalse(game.singleplayer)
        self.assertIsInstance(game.settings, Settings)
        self.assertIsNotNone(game.clock, pygame.time.Clock)
        self.assertIsNotNone(game.screen, pygame.Surface)
        self.assertIsNotNone(game.bg_img, pygame.Surface)
        self.assertIsNotNone(game.bg_img_rect, pygame.Rect)
        self.assertIsNotNone(game.reset_bg, pygame.Surface)
        self.assertIsNotNone(game.second_bg, pygame.Surface)
        self.assertIsNotNone(game.third_bg, pygame.Surface)
        self.assertIsNotNone(game.fourth_bg, pygame.Surface)
        self.assertEqual(game.ui_options, game.settings.ui_options)
        self.assertEqual(game.ships, [game.thunderbird_ship, game.phoenix_ship])
        self.assertEqual(game.pause_time, 0)
        self.assertEqual(game.game_loaded, False)
        self.assertEqual(pygame.display.get_caption()[0], "Alien Onslaught")
        mock_set_icon.assert_called_once_with(game.settings.game_icon)

    @patch("src.alien_onslaught.pygame.display.set_mode")
    def test_init_singleplayer(self, mock_display):
        """Test the initialization of AlienOnslaught in singleplayer mode."""
        mock_display.return_value = pygame.Surface((1280, 700))
        game = AlienOnslaught(singleplayer=True)

        # Assertions
        self.assertTrue(game.singleplayer)

    def test_initialize_game_objects(self):
        """Test the initialization of game objects."""
        self.game._initialize_game_objects()

        # Assert that the necessary game objects are correctly initialized
        self.assertIsInstance(self.game.ships_manager, ShipsManager)
        self.assertIsInstance(self.game.thunderbird_ship, Thunderbird)
        self.assertIsInstance(self.game.phoenix_ship, Phoenix)
        self.assertEqual(
            self.game.ships, [self.game.thunderbird_ship, self.game.phoenix_ship]
        )
        self.assertIsInstance(self.game.stats, GameStats)
        self.assertIsInstance(self.game.score_board, ScoreBoard)
        self.assertIsInstance(self.game.loading_screen, LoadingScreen)

    def test_singleplayer_getter(self):
        """Test the getter for singleplayer attribute."""
        self.assertFalse(self.game.singleplayer)

    def test_singleplayer_setter(self):
        """Test the setter for singleplayer attribute."""
        # Set singleplayer to True
        self.game.singleplayer = True

        # Assert that the singleplayer attribute is updated correctly
        self.assertTrue(self.game.singleplayer)

        # Assert that the singleplayer attributes of ships_manager
        # and screen_manager are also updated
        self.assertTrue(self.game.ships_manager.singleplayer)
        self.assertTrue(self.game.screen_manager.singleplayer)

    def test_initialize_sprite_groups(self):
        """Test the _initialize_sprite_groups method."""
        self.game._initialize_sprite_groups()

        # sprite groups assertions
        self.assertIsInstance(self.game.thunderbird_bullets, pygame.sprite.Group)
        self.assertIsInstance(self.game.phoenix_bullets, pygame.sprite.Group)
        self.assertIsInstance(self.game.thunderbird_missiles, pygame.sprite.Group)
        self.assertIsInstance(self.game.phoenix_missiles, pygame.sprite.Group)
        self.assertIsInstance(self.game.thunderbird_laser, pygame.sprite.Group)
        self.assertIsInstance(self.game.phoenix_laser, pygame.sprite.Group)
        self.assertIsInstance(self.game.alien_bullet, pygame.sprite.Group)
        self.assertIsInstance(self.game.powers, pygame.sprite.Group)
        self.assertIsInstance(self.game.aliens, pygame.sprite.Group)
        self.assertIsInstance(self.game.asteroids, pygame.sprite.Group)

        # sprite_groups assertions
        self.assertEqual(len(self.game.sprite_groups), 10)
        self.assertIn(self.game.powers, self.game.sprite_groups)
        self.assertIn(self.game.aliens, self.game.sprite_groups)
        self.assertIn(self.game.thunderbird_bullets, self.game.sprite_groups)
        self.assertIn(self.game.thunderbird_missiles, self.game.sprite_groups)
        self.assertIn(self.game.thunderbird_laser, self.game.sprite_groups)
        self.assertIn(self.game.phoenix_bullets, self.game.sprite_groups)
        self.assertIn(self.game.phoenix_missiles, self.game.sprite_groups)
        self.assertIn(self.game.phoenix_laser, self.game.sprite_groups)
        self.assertIn(self.game.asteroids, self.game.sprite_groups)
        self.assertIn(self.game.alien_bullet, self.game.sprite_groups)

        # single_sprite_groups assertions
        self.assertEqual(len(self.game.single_sprite_groups), 7)
        self.assertIn(self.game.powers, self.game.single_sprite_groups)
        self.assertIn(self.game.aliens, self.game.single_sprite_groups)
        self.assertIn(self.game.thunderbird_bullets, self.game.single_sprite_groups)
        self.assertIn(self.game.thunderbird_missiles, self.game.single_sprite_groups)
        self.assertIn(self.game.thunderbird_laser, self.game.single_sprite_groups)
        self.assertIn(self.game.asteroids, self.game.single_sprite_groups)
        self.assertIn(self.game.alien_bullet, self.game.single_sprite_groups)

    def test_initialize_managers(self):
        """Test the initialize_managers method."""
        self.game.initialize_managers()

        # Assertions
        self.assertIsInstance(self.game.sound_manager, SoundManager)
        self.assertIsInstance(self.game.buttons_manager, GameButtonsManager)
        self.assertIsInstance(self.game.screen_manager, ScreenManager)
        self.assertIsInstance(self.game.player_input, PlayerInput)
        self.assertIsInstance(self.game.collision_handler, CollisionManager)
        self.assertIsInstance(self.game.powers_manager, PowerEffectsManager)
        self.assertIsInstance(self.game.asteroids_manager, AsteroidsManager)
        self.assertIsInstance(self.game.alien_bullets_manager, AlienBulletsManager)
        self.assertIsInstance(self.game.weapons_manager, WeaponsManager)
        self.assertIsInstance(self.game.aliens_manager, AliensManager)
        self.assertIsInstance(self.game.gameplay_manager, GameplayHandler)
        self.assertIsInstance(self.game.game_over_manager, EndGameManager)
        self.assertIsInstance(self.game.save_load_manager, SaveLoadSystem)

        self.assertEqual(self.game.screen_manager.singleplayer, self.game.singleplayer)
        self.assertEqual(self.game.aliens_manager.aliens, self.game.aliens)
        self.assertEqual(self.game.game_over_manager.screen, self.game.screen)

    @mock.patch.object(AlienOnslaught, "MENU_RUNNING", new_callable=mock.PropertyMock)
    @patch("src.alien_onslaught.play_music")
    @patch("src.alien_onslaught.pygame.display.flip")
    def test_run_menu(self, mock_flip, mock_play_music, mock_menu_running):
        """Test the run_menu method."""
        mock_menu_running.side_effect = [True, False]
        self.game.handle_menu_events = MagicMock()

        self.game.run_menu()

        # Assertions
        self.game.sound_manager.load_sounds.assert_called_once_with("menu_sounds")
        mock_play_music.assert_called_once_with(
            self.game.sound_manager.menu_music, "menu"
        )
        self.game.handle_menu_events.assert_called_once()
        self.game.screen_manager.update_window_mode.assert_called_once()
        self.game.screen_manager.draw_menu_objects.assert_called_once_with(
            self.game.bg_img, self.game.bg_img_rect
        )
        self.game.screen_manager.draw_cursor.assert_called_once()
        mock_flip.assert_called_once()

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_quit_event(self, mock_get):
        """Test the handling of the quit_event from the
        handle_menu_events method."""
        mock_quit_event = MagicMock()
        mock_quit_event.type = pygame.QUIT
        mock_get.return_value = [mock_quit_event]

        self.game.handle_menu_events()

        self.game.buttons_manager.handle_quit_event.assert_called_once()

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_keydown_event(self, mock_get):
        """Test the handling of the keydown event from the
        handle_menu_events method."""
        mock_keydown_event = MagicMock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.key = pygame.K_f
        mock_get.return_value = [mock_keydown_event]

        self.game.handle_menu_events()

        self.game.screen_manager.toggle_window_mode.assert_called_once()

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_mousebuttondown_event_single(self, mock_get):
        """Test the handling of the mousebuttondown event for
        the single button from the handle_menu_events method.
        """
        mock_mousebuttondown_event_single = MagicMock()
        mock_mousebuttondown_event_single.type = pygame.MOUSEBUTTONDOWN
        mock_mousebuttondown_event_single.button = pygame.BUTTON_LEFT
        mock_get.return_value = [mock_mousebuttondown_event_single]

        self.game.start_single_player_game = MagicMock()

        self.game.handle_menu_events()

        self.game.buttons_manager.handle_single_player_button_click.assert_called_once_with(
            self.game.start_single_player_game
        )

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_mousebuttondown_event_multi(self, mock_get):
        """Test the handling of the mousebuttondown event for
        the multi button from the handle_menu_events method.
        """
        mock_mousebuttondown_event_multi = MagicMock()
        mock_mousebuttondown_event_multi.type = pygame.MOUSEBUTTONDOWN
        mock_mousebuttondown_event_multi.button = pygame.BUTTON_LEFT
        mock_get.return_value = [mock_mousebuttondown_event_multi]

        self.game.buttons_manager.single.rect.collidepoint = MagicMock(
            return_value=False
        )

        self.game.start_multiplayer_game = MagicMock()

        self.game.handle_menu_events()

        self.game.buttons_manager.handle_multiplayer_button_click.assert_called_once_with(
            self.game.start_multiplayer_game
        )

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_mousebuttondown_event_quit(self, mock_get):
        """Test the handling of the mousebuttondown event for
        the quit button from the handle_menu_events method.
        """
        mock_mousebuttondown_event_quit = MagicMock()
        mock_mousebuttondown_event_quit.type = pygame.MOUSEBUTTONDOWN
        mock_mousebuttondown_event_quit.button = pygame.BUTTON_LEFT
        mock_get.return_value = [mock_mousebuttondown_event_quit]

        self.game.buttons_manager.single.rect.collidepoint = MagicMock(
            return_value=False
        )
        self.game.buttons_manager.multi.rect.collidepoint = MagicMock(
            return_value=False
        )

        self.game.handle_menu_events()

        self.game.buttons_manager.handle_quit_button_click.assert_called_once()

    @patch("src.alien_onslaught.pygame.event.get")
    def test_handle_videoresize_event(self, mock_get):
        """Test the handling of the VIDEORESIZE event in the
        handle_menu_events method.
        """
        mock_videoresize_event = MagicMock()
        mock_videoresize_event.type = pygame.VIDEORESIZE
        mock_get.return_value = [mock_videoresize_event]

        self.game.handle_menu_resize_screen_event = MagicMock()

        self.game.handle_menu_events()

        self.game.handle_menu_resize_screen_event.assert_called_once_with(
            mock_videoresize_event.size
        )

    def test_handle_menu_resize_screen_event(self):
        """Test the handle_menu_resize_screen_event method."""
        mock_size = (1260, 800)

        self.game.handle_menu_resize_screen_event(mock_size)

        self.game.screen_manager.resize_screen.assert_called_once_with(mock_size)
        self.game.screen_manager.update_buttons.assert_called_once()
        self.game.screen_manager.create_controls.assert_called_once()

    def test_start_single_player_game(self):
        """Test the start_single_player_game method."""
        self.game.singleplayer = False
        self.game._set_singleplayer_variables = MagicMock()
        self.game._start_game = MagicMock()

        self.game.start_single_player_game()

        self.assertTrue(self.game.singleplayer)
        self.game._set_singleplayer_variables.assert_called_once()
        self.game._start_game.assert_called_once()

    def test_start_multiplayer_game(self):
        """Test the start_multiplayer_game method."""
        self.game.singleplayer = True
        self.game._set_multiplayer_variables = MagicMock()
        self.game._start_game = MagicMock()

        self.game.start_multiplayer_game()

        self.assertFalse(self.game.singleplayer)
        self.game._set_multiplayer_variables.assert_called_once()
        self.game._start_game.assert_called_once()

    def test__set_singleplayer_variables(self):
        """Test the set_singleplayer_variables method."""
        self.game._set_singleplayer_variables()

        self.assertTrue(self.game.thunderbird_ship.state.single_player)
        self.assertEqual(self.game.ships, [self.game.thunderbird_ship])
        self.game.high_score_manager.update_high_score_filename.assert_called_once()
        self.game.gameplay_manager.reset_cosmic_conflict.assert_called_once()

    def test__set_multiplayer_variables(self):
        """Test the set_multiplayer_variables method."""
        self.game._set_multiplayer_variables()

        self.assertFalse(self.game.thunderbird_ship.state.single_player)
        self.assertEqual(
            self.game.ships, [self.game.thunderbird_ship, self.game.phoenix_ship]
        )
        self.game.high_score_manager.update_high_score_filename.assert_called_once()

    def test__start_game(self):
        """Test the start_game method."""
        self.game.run_game = MagicMock()

        self.game._start_game()

        self.game.sound_manager.load_sounds.assert_called_once_with("gameplay_sounds")
        self.assertFalse(self.game.ui_options.paused)
        self.assertIsNone(self.game.sound_manager.current_sound)
        self.game.stats.reset_stats.assert_called_once_with(
            self.game.phoenix_ship, self.game.thunderbird_ship
        )
        self.game.run_game.assert_called_once()

    def test__update_background(self):
        """Test the _update_background method."""
        i = 100
        self.game._handle_background_change = MagicMock()
        self.game.screen = MagicMock()
        self.game.screen.blit = MagicMock()

        updated_i = self.game._update_background(i)

        expected_calls = [
            call(
                self.game.bg_img,
                [0, i],
            ),
            call(
                self.game.bg_img,
                [0, i - self.game.settings.screen_height],
            ),
        ]

        self.assertEqual(self.game.screen.blit.call_args_list, expected_calls)
        self.game._handle_background_change.assert_called_once()
        self.assertEqual(updated_i, i + 1)

    def test__update_background_bigger_i(self):
        """Test the _update_background method when i is bigger
        than the screen height.
        """
        i = 701
        self.game._handle_background_change = MagicMock()
        self.game.screen = MagicMock()
        self.game.screen.blit = MagicMock()

        updated_i = self.game._update_background(i)

        expected_calls = [
            call(
                self.game.bg_img,
                [0, i],
            ),
            call(
                self.game.bg_img,
                [0, i - self.game.settings.screen_height],
            ),
        ]

        self.assertEqual(self.game.screen.blit.call_args_list, expected_calls)
        self.game._handle_background_change.assert_called_once()
        self.assertEqual(updated_i, 1)

    @mock.patch.object(AlienOnslaught, "GAME_RUNNING", new_callable=mock.PropertyMock)
    @patch("src.alien_onslaught.pygame.time.Clock")
    def test_run_game_active(self, _, mock_game_running):
        """Test the run_game method when the game is active."""
        mock_game_running.side_effect = [True, False]
        self.game.stats.game_active = True
        self.game.ui_options.paused = False

        self.game.check_events = MagicMock()
        self.game._update_background = MagicMock()
        self.game._handle_game_logic = MagicMock()
        self.game._update_screen = MagicMock()
        self.game._check_for_pause = MagicMock()

        self.game.run_game()

        # Assert that the methods are called as expected
        self.game.check_events.assert_called_once()
        self.game.game_over_manager.check_game_over.assert_called_once()
        self.game.screen_manager.update_window_mode.assert_called_once()

        self.game._update_background.assert_called()
        self.game._handle_game_logic.assert_called()

        self.game._update_screen.assert_called()
        self.game._check_for_pause.assert_called()

    @mock.patch.object(AlienOnslaught, "GAME_RUNNING", new_callable=mock.PropertyMock)
    @patch("src.alien_onslaught.pygame.time.Clock")
    def test_run_game_inactive(self, _, mock_game_running):
        """Test the run_game method when the game is not active."""
        self.game.screen = MagicMock()
        self.game.screen.blit = MagicMock()

        mock_game_running.side_effect = [True, False]
        self.game.stats.game_active = False
        self.game.ui_options.paused = False

        self.game.check_events = MagicMock()
        self.game._update_background = MagicMock()
        self.game._handle_game_logic = MagicMock()
        self.game._update_screen = MagicMock()
        self.game._check_for_pause = MagicMock()

        self.game.run_game()

        # Assert methods that are called or not called
        self.game.check_events.assert_called_once()
        self.game._update_screen.assert_called_once()
        self.assertEqual(self.game.game_over_manager.check_game_over.call_count, 2)
        self.game.screen_manager.update_window_mode.assert_called_once()
        self.game.screen.blit.assert_called_once_with(self.game.bg_img, [0, 0])

        self.game._update_background.assert_not_called()
        self.game._handle_game_logic.assert_not_called()
        self.game._check_for_pause.assert_not_called()

    def test_handle_game_logic(self):
        """Test the handle_game_logic method."""
        self.game.apply_game_mode_behaviors = MagicMock()

        # Run the method
        self.game._handle_game_logic()

        # Assert that the expected methods are called with the correct arguments
        self.game.apply_game_mode_behaviors.assert_called_once()
        self.game.gameplay_manager.handle_level_progression.assert_called_once()
        self.game.powers_manager.create_powers.assert_called_once()
        self.game.powers_manager.update_powers.assert_called_once()
        self.game.collision_handler.check_powers_collisions.assert_called_once_with(
            self.game.powers_manager.apply_powerup_or_penalty,
            self.game.powers_manager.health_power_up,
            self.game.powers_manager.weapon_power_up,
        )
        self.game.powers_manager.manage_power_downs.assert_called_once()
        self.game.powers_manager.display_powers_effect.assert_called_once()
        self.game.gameplay_manager.create_normal_level_bullets.assert_called_once_with(
            self.game.alien_bullets_manager.create_alien_bullets
        )
        self.game.alien_bullets_manager.update_alien_bullets.assert_called_once()
        self.game.collision_handler.check_alien_bullets_collisions.assert_called_once_with(
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )
        self.game.player_input.handle_ship_firing.assert_called_once_with(
            self.game.weapons_manager.fire_bullet
        )
        self.game.weapons_manager.update_projectiles.assert_called_once()
        self.game.collision_handler.check_bullet_alien_collisions.assert_called_once()
        self.game.collision_handler.check_missile_alien_collisions.assert_called_once()
        self.game.collision_handler.check_laser_alien_collisions.assert_called_once()
        self.game.aliens_manager.update_aliens.assert_called_once()
        self.game.collision_handler.check_alien_ship_collisions.assert_called_once_with(
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )
        self.game.ships_manager.update_ship_state.assert_called_once()
        self.game.weapons_manager.update_laser_status.assert_called_once()
        self.game.weapons_manager.check_laser_availability.assert_called_once()
        self.game.collision_handler.handle_shielded_ship_collisions.assert_called_once_with(
            self.game.ships,
            self.game.aliens,
            self.game.alien_bullet,
            self.game.asteroids,
        )

    def test_check_events_quit(self):
        """Test the quit event in the check_events method."""
        quit_event = pygame.event.Event(pygame.QUIT)
        self.game.stats.game_active = True

        with patch("src.alien_onslaught.pygame.event.get", return_value=[quit_event]):
            self.game.check_events()

        self.game.buttons_manager.handle_quit_event.assert_called_once()

    def test_check_events_keydown(self):
        """Test the keydown event in the check_events method."""
        keydown_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f)
        self.game.stats.game_active = True
        self.game.player_input.check_keydown_events = MagicMock()

        with patch(
            "src.alien_onslaught.pygame.event.get", return_value=[keydown_event]
        ):
            self.game.check_events()

        self.game.player_input.check_keydown_events.assert_called_once_with(
            keydown_event,
            self.game._reset_game,
            self.game.run_menu,
            self.game.game_over_manager.return_to_game_menu,
            self.game.weapons_manager.fire_missile,
            self.game.weapons_manager.fire_laser,
        )

    def test_check_events_keyup(self):
        """Test the keyup events in the check_events method."""
        keyup_event = pygame.event.Event(pygame.KEYUP, key=pygame.K_a)
        self.game.stats.game_active = True

        with patch("src.alien_onslaught.pygame.event.get", return_value=[keyup_event]):
            self.game.check_events()

        self.game.player_input.check_keyup_events.assert_called_once_with(keyup_event)

    def test_check_events_mousebuttondown(self):
        """Test the mousebuttondown events in the check_events method."""
        mousebuttondown_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, pos=(100, 200)
        )
        mousebuttondown_event.button = pygame.BUTTON_LEFT

        self.game.stats.game_active = True
        self.game._check_buttons = MagicMock()

        with patch(
            "src.alien_onslaught.pygame.mouse.get_pos", return_value=(100, 200)
        ), patch(
            "src.alien_onslaught.pygame.event.get", return_value=[mousebuttondown_event]
        ):
            self.game.check_events()

        self.game._check_buttons.assert_called_once_with((100, 200))
        self.game.ship_selection.handle_ship_selection.assert_called_once_with(
            (100, 200)
        )

    def test_check_events_videoresize(self):
        """Test the VIDEORESIZE event in the check_events method."""
        videoresize_event = pygame.event.Event(pygame.VIDEORESIZE, size=(1280, 700))

        with patch("pygame.event.get", return_value=[videoresize_event]):
            self.game.check_events()

        # Assertions
        self.game.screen_manager.resize_screen.assert_called_once_with((1280, 700))
        self.game.screen_manager.update_buttons.assert_called_once()

    @patch("src.alien_onslaught.play_sound")
    @patch("src.alien_onslaught.pygame.time.delay")
    def test_check_buttons_button_clicked(self, mock_delay, mock_play_sound):
        """Test the check_buttons when a button is clicked."""
        mock_button = MagicMock()
        mock_button.rect = MagicMock()
        mock_button.rect.collidepoint.return_value = True
        mock_button.visible = False
        self.game.stats.game_active = False

        self.game.run_menu = MagicMock()
        self.game.buttons_manager.create_button_actions_dict = MagicMock(
            return_value={mock_button: self.game.run_menu}
        )

        mouse_pos = (100, 200)
        self.game._check_buttons(mouse_pos)

        # Assertions
        self.game.buttons_manager.handle_buttons_visibility.assert_called_once()
        self.game.buttons_manager.create_button_actions_dict.assert_called_once_with(
            self.game.run_menu, self.game._reset_game
        )

        mock_button.rect.collidepoint.assert_called_once_with(mouse_pos)
        self.game.run_menu.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "click"
        )
        mock_delay.assert_called_once_with(200)

    @patch("src.alien_onslaught.pygame.time.delay")
    @patch("src.alien_onslaught.play_sound")
    def test_check_buttons_button_not_clicked(self, mock_play_sound, mock_delay):
        """Test the check_buttons when the button is not clicked."""
        mock_button = MagicMock()
        mock_button.rect = MagicMock()
        mock_button.rect.collidepoint.return_value = False
        mock_button.visible = False

        self.game.buttons_manager.create_button_actions_dict = MagicMock(
            return_value={mock_button: self.game.run_menu}
        )
        self.game.run_menu = MagicMock()

        mouse_pos = (100, 200)
        self.game._check_buttons(mouse_pos)

        # Assertions
        self.game.buttons_manager.handle_buttons_visibility.assert_called_once()
        self.game.buttons_manager.create_button_actions_dict.assert_called_once_with(
            self.game.run_menu, self.game._reset_game
        )

        mock_button.rect.collidepoint.assert_called_once_with(mouse_pos)

        self.game.run_menu.assert_not_called()
        mock_play_sound.assert_not_called()
        mock_delay.assert_not_called()

    def test_handle_background_change_reset_bg(self):
        """Test handling of background change for reset_bg image."""
        self.game.stats.level = 1

        self.game._handle_background_change()

        self.assertEqual(self.game.bg_img, self.game.reset_bg)

    def test_handle_background_change_second_bg(self):
        """Test handling of background change for second_bg image."""
        self.game.stats.level = 9

        self.game._handle_background_change()

        self.assertEqual(self.game.bg_img, self.game.second_bg)

    def test_handle_background_change_third_bg(self):
        """Test handling of background change for third_bg image."""
        self.game.stats.level = 17

        self.game._handle_background_change()

        self.assertEqual(self.game.bg_img, self.game.third_bg)

    def test_handle_background_change_fourth_bg(self):
        """Test handling of background change for fourth_bg image."""
        self.game.stats.level = 26

        self.game._handle_background_change()

        self.assertEqual(self.game.bg_img, self.game.fourth_bg)

    def test_handle_background_change_current_level_does_not_exist(self):
        """Test handling of background change when the current level does
        not exist in the bg_images dictionary.
        """
        self.game.stats.level = 12

        self.game.bg_img = self.game.second_bg

        self.game._handle_background_change()

        self.assertEqual(self.game.bg_img, self.game.second_bg)

    def test_apply_game_mode_behaviors(self):
        """Test applying game behaviors for different game modes."""
        game_modes = self.game.settings.game_modes

        # Set the game mode to endless_onslaught
        game_modes.endless_onslaught = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.endless_onslaught.assert_called_once_with(
            self.game.aliens_manager.create_fleet,
            self.game.asteroids_manager.handle_asteroids,
        )

        # Set the game mode to slow_burn
        game_modes.endless_onslaught = False
        game_modes.slow_burn = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.slow_burn.assert_called_once_with(
            self.game.asteroids_manager.handle_asteroids,
        )

        # Set the game mode to boss_rush
        game_modes.slow_burn = False
        game_modes.boss_rush = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.boss_rush.assert_called_once_with(
            self.game.asteroids_manager.handle_asteroids,
            self.game.alien_bullets_manager.create_alien_bullets,
        )

        # Set the game mode to meteor_madness
        game_modes.boss_rush = False
        game_modes.meteor_madness = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.meteor_madness.assert_called_once_with(
            self.game.asteroids_manager.create_asteroids,
            self.game.asteroids_manager.update_asteroids,
            self.game.collision_handler.check_asteroids_collisions,
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )

        # Set the game mode to last_bullet
        game_modes.meteor_madness = False
        game_modes.last_bullet = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.last_bullet.assert_called_once_with(
            self.game.thunderbird_ship,
            self.game.phoenix_ship,
            self.game.asteroids_manager.handle_asteroids,
        )

        # Set the game mode to cosmic_conflict
        game_modes.last_bullet = False
        game_modes.cosmic_conflict = True
        self.game.apply_game_mode_behaviors()
        self.game.gameplay_manager.cosmic_conflict.assert_called_once_with(
            self.game.collision_handler.check_cosmic_conflict_collisions,
            self.game.ships_manager.thunderbird_ship_hit,
            self.game.ships_manager.phoenix_ship_hit,
        )

        # Set the game mode to default
        game_modes.cosmic_conflict = False
        self.game.apply_game_mode_behaviors()
        self.game.asteroids_manager.handle_asteroids.assert_called_once_with(
            create_at_high_levels=True,
        )

    @patch("src.alien_onslaught.play_sound")
    def test_reset_game(self, mock_play_sound):
        """Test the reset_game method."""
        self.game.reset_timed_variables = MagicMock()
        self.game.check_game_loaded = MagicMock()
        self.game.settings = MagicMock()
        self.game.singleplayer = False
        self.game.game_loaded = False

        self.game._reset_game()

        self.game.gameplay_manager.reset_game_objects.assert_called_once()
        self.game.check_game_loaded.assert_called_once()

        self.assertTrue(self.game.stats.game_active)
        self.assertFalse(self.game.ui_options.high_score_saved)
        self.assertFalse(self.game.ui_options.game_over_sound_played)

        self.game.ships_manager.reset_ships.assert_called_once()
        self.game.player_input.reset_ship_flags.assert_called_once()

        self.game.gameplay_manager.handle_boss_stats.assert_called_once()

        self.game.gameplay_manager.prepare_last_bullet_bullets.assert_called_once()
        self.game.gameplay_manager.set_last_bullet_bullets.assert_called_once()

        self.game.reset_timed_variables.assert_called_once()

        self.game.score_board.render_scores.assert_called_once()
        self.game.score_board.render_missiles_num.assert_called_once()
        self.game.score_board.render_high_score.assert_called_once()
        self.game.score_board.prep_level.assert_called_once()
        self.game.score_board.create_health.assert_called_once()

        self.game.sound_manager.prepare_level_music.assert_called_once()
        mock_play_sound.assert_called_once_with(
            self.game.sound_manager.game_sounds, "warp"
        )
        self.assertFalse(self.game.game_loaded)

        self.game.singleplayer = True

        self.game._reset_game()

        self.assertFalse(self.game.phoenix_ship.state.alive)

    def test_check_game_loaded(self):
        """Test the check_game_loaded method when the game is loaded."""
        self.game.settings = MagicMock()
        self.game.game_loaded = True

        self.game.check_game_loaded()

        self.game.save_load_manager.update_alien_states.assert_called_once()
        self.game.save_load_manager.update_player_ship_states.assert_called_once()
        self.game.save_load_manager.update_player_weapon.assert_called_once()

        self.game.stats.reset_stats.assert_not_called()
        self.game.settings.dynamic_settings.assert_not_called()
        self.game.gameplay_manager.handle_alien_creation.assert_not_called()

    def test_check_game_loaded_not_loaded(self):
        """Test the check_game_loaded method when the game is not loaded."""
        self.game.settings = MagicMock()
        self.game.game_loaded = False

        self.game.check_game_loaded()

        self.game.stats.reset_stats.assert_called_once()
        self.game.settings.dynamic_settings.assert_called_once()
        self.game.gameplay_manager.handle_alien_creation.assert_called_once()

        self.game.save_load_manager.update_alien_states.assert_not_called()
        self.game.save_load_manager.update_player_ship_states.assert_not_called()
        self.game.save_load_manager.update_player_weapon.assert_not_called()

    @patch("src.alien_onslaught.pygame.time.get_ticks")
    def test_reset_timed_variables(self, mock_get_ticks):
        """Test the reset_timed_variables method."""
        self.game.powers_manager.last_power_up_time = 10
        self.game.asteroids_manager.last_asteroid_time = 10
        self.game.gameplay_manager.last_level_time = None
        mock_get_ticks.return_value = 10

        self.game.reset_timed_variables()

        self.assertEqual(self.game.powers_manager.last_power_up_time, 0)
        self.assertEqual(self.game.asteroids_manager.last_asteroid_time, 0)
        self.assertEqual(self.game.gameplay_manager.last_level_time, 10)

    def test_draw_game_objects(self):
        """Test the draw_game_objects method."""
        self.game.singleplayer = False
        self.game.phoenix_ship = MagicMock()
        self.game.thunderbird_ship = MagicMock()
        self.game.ships = [self.game.phoenix_ship, self.game.thunderbird_ship]

        self.game._draw_game_objects()

        self.game.ships_manager.update_ship_alive_states.assert_called_once()

        for ship in self.game.ships:
            if ship.state.alive:
                ship.blitme.assert_called_once()

        for group in self.game.single_sprite_groups:
            for sprite in group.sprites():
                sprite.draw.assert_called_once()

        self.game.score_board.show_score.assert_called_once()

    @patch("pygame.display.flip")
    def test_update_screen_game_active_paused(self, mock_display_flip):
        """Test the update_screen method when game active and paused"""
        self.game._draw_game_objects = MagicMock()
        self.game.stats.game_active = True
        self.game.ui_options.paused = True

        self.game._update_screen()

        self.game._draw_game_objects.assert_called_once()
        self.game.screen_manager.display_pause.assert_called_once()
        mock_display_flip.assert_called_once()

    @patch("pygame.display.flip")
    def test_update_screen_game_active_not_paused(self, mock_display_flip):
        """Test the update_screen method when game active and not paused."""
        self.game._draw_game_objects = MagicMock()
        self.game.stats.game_active = True
        self.game.ui_options.paused = False

        self.game._update_screen()

        self.game._draw_game_objects.assert_called_once()
        mock_display_flip.assert_called_once()

        self.game.screen_manager.display_pause.assert_not_called()

    @patch("pygame.display.flip")
    def test_update_screen_game_not_active(self, mock_display_flip):
        """Test the update_screen method when the game is not active."""
        # Test for all ui_options
        self.game._draw_game_objects = MagicMock()
        self.game.stats.game_active = False
        self.game.ui_options.paused = False
        self.game.ui_options.show_difficulty = True
        self.game.ui_options.show_high_scores = True
        self.game.ui_options.show_game_modes = True
        self.game.ui_options.ship_selection = True

        self.game._update_screen()

        self.game.buttons_manager.draw_buttons.assert_called_once()
        self.game.screen_manager.draw_cursor.assert_called_once()
        self.game.ship_selection.draw.assert_called_once()

        self.game.buttons_manager.draw_difficulty_buttons.assert_called_once()
        self.game.screen_manager.display_high_scores_on_screen.assert_called_once()
        self.game.buttons_manager.delete_scores.draw_button.assert_called_once()
        self.game.buttons_manager.draw_game_mode_buttons.assert_called_once()

        mock_display_flip.assert_called_once()

    @mock.patch("src.alien_onslaught.pygame.time.get_ticks")
    def test_check_for_pause(self, mock_get_ticks):
        """Test the check_for_pause method."""
        mock_get_ticks.return_value = 10

        # Mocking self.ui_options.paused and self.check_events()
        with mock.patch.object(
            self.game, "ui_options"
        ) as mock_ui_options, mock.patch.object(
            self.game, "check_events"
        ) as mock_check_events:
            mock_ui_options.paused = True
            mock_check_events.side_effect = lambda: setattr(
                mock_ui_options, "paused", False
            )

            self.game._check_for_pause()

            # Assertions
            mock_check_events.assert_called_once()
            self.assertFalse(mock_ui_options.paused)
            self.assertEqual(mock_get_ticks.call_count, 2)

            # Calculate the expected value of pause_time
            pause_start_time = 10
            pause_end_time = mock_get_ticks.return_value
            expected_pause_time = pause_end_time - pause_start_time

            self.assertEqual(self.game.pause_time, expected_pause_time)


if __name__ == "__main__":
    unittest.main()
