"""The 'game_utils' module contains various utility functions."""

import os
import sys
import json
import pygame

from .constants import (
    P1_CONTROLS,
    P2_CONTROLS,
    BOSS_RUSH,
    ALIEN_BULLETS_IMG,
    BOSS_BULLETS_IMG,
    SINGLE_PLAYER_FILE,
    MULTI_PLAYER_FILE,
    DEFAULT_HIGH_SCORES,
    RANK_POSITIONS,
)

if hasattr(sys, "_MEIPASS"):
    # Running as a PyInstaller bundle
    BASE_PATH = os.path.join(sys._MEIPASS, "game_assets", "images") # type: ignore
else:
    # Running as a regular script
    BASE_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "game_assets", "images")
    )

if hasattr(sys, "_MEIPASS"):
    # Running as a PyInstaller bundle
    SOUND_PATH = os.path.join(sys._MEIPASS, "game_assets", "sounds") # type: ignore
else:
    # Running as a regular script
    SOUND_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "game_assets", "sounds")
    )


def load_single_image(relative_path):
    """Loads an image based on the BASED_PATH."""
    base_path = BASE_PATH
    image_path = os.path.join(base_path, relative_path)
    return pygame.image.load(image_path)


def get_colliding_sprites(ship, bullets_or_missiles):
    """Returns the sprites that collide with the given ship."""
    return pygame.sprite.spritecollide(ship, bullets_or_missiles, False)


def load_images(image_dict):
    """A function that loads multiple images from a dict of the form:
    key: image name
    value: path to image location"""
    return {
        key: pygame.image.load(os.path.join(BASE_PATH, value))
        for key, value in image_dict.items()
    }


def load_sound_files(sounds_dict):
    """A function that loads multiple sounds from a dict of the form:
    key: sound name:
    value: path to sound location."""
    pygame.mixer.init()
    return {
        key: pygame.mixer.Sound(os.path.join(SOUND_PATH, value))
        for key, value in sounds_dict.items()
    }


def set_sounds_volume(sounds, volume):
    """Set the volume for all sounds in the passed sounds dict."""
    for sound in sounds.values():
        sound.set_volume(volume)


def get_available_channels():
    """Returns a list of available sound channels."""
    num_channels = pygame.mixer.get_num_channels()
    available_channels = []
    for channel_num in range(num_channels):
        channel = pygame.mixer.Channel(channel_num)
        if not channel.get_busy():
            available_channels.append(channel)
    return available_channels


def play_sound(sounds_list, sound_name, loop=False):
    """Plays a certain sound located in the 'sounds_list' on an available sound channel."""
    if sound_name == "bullet":
        channel = pygame.mixer.Channel(7)
    elif sound_name == "alien_exploding":
        channel = pygame.mixer.Channel(6)
    elif available_channels := get_available_channels():
        channel = available_channels[0]
    else:
        channel = pygame.mixer.Channel(1)

    channel.play(sounds_list[sound_name], -1 if loop else 0)


def load_frames(filename_pattern, num_frames, start=0):
    """Loads a sequence of image frames into a list"""
    frame_list = []
    for i in range(start, start + num_frames):
        filename = filename_pattern.format(i)
        path = os.path.join(BASE_PATH, filename)
        image = pygame.image.load(path)
        frame_list.append(image)
    return frame_list


def load_alien_images(alien_prefix):
    """Load the images for the given alien prefix."""
    frames = []
    for i in range(6):
        filename = os.path.join(BASE_PATH, f"aliens/{alien_prefix}_{i}.png")
        frame = pygame.image.load(filename)
        frames.append(frame)

    return frames


def resize_image(image, screen_size=None):
    """Resizes an image to match the current screen size."""
    if screen_size is None:
        screen_size = pygame.display.get_surface().get_size()
    return pygame.transform.smoothscale(image, screen_size)


def load_button_imgs(button_names):
    """Load button images."""
    button_images = {}
    for name in button_names:
        filename = os.path.join(BASE_PATH, "buttons", f"{name}.png")
        button_images[name] = filename
    return button_images


def load_controls_image(image_surface, position):
    """Loads images for controls displayed on menu screen."""
    image = image_surface
    rect = image.get_rect(**position)
    return image, rect


def load_boss_images():
    """Loads and returns a dict of boss images."""
    return {
        alien_name: pygame.image.load(os.path.join(BASE_PATH, alien_image_path))
        for alien_name, alien_image_path in BOSS_RUSH.items()
    }


def load_alien_bullets():
    """Loads and returns a dict of alien bullet images."""
    return {
        bullet_name: pygame.image.load(os.path.join(BASE_PATH, bullet_image_path))
        for bullet_name, bullet_image_path in ALIEN_BULLETS_IMG.items()
    }


def load_boss_bullets():
    """Loads and returns a dict of boss bullet images."""
    return {
        bullet_name: pygame.image.load(os.path.join(BASE_PATH, bullet_image_path))
        for bullet_name, bullet_image_path in BOSS_BULLETS_IMG.items()
    }


def render_text(text, font, color, start_pos, line_spacing, second_color=None):
    """Render text with new_lines and tabs."""
    lines = text.split("\n")

    text_surfaces = []
    text_rects = []

    tab_width = 10  # Number of spaces per tab

    for i, line in enumerate(lines):
        # Replace tabs with spaces
        line = line.replace("\t", " " * tab_width)

        if i == 0 and second_color:
            text_surface = font.render(line, True, second_color, None)
        else:
            text_surface = font.render(line, True, color, None)

        text_rect = text_surface.get_rect(
            topleft=(start_pos[0], start_pos[1] + i * line_spacing)
        )
        text_surfaces.append(text_surface)
        text_rects.append(text_rect)

    return text_surfaces, text_rects


def load_high_scores(game):
    """Load the high score data from the JSON file or create a new high score list."""
    filename = SINGLE_PLAYER_FILE if game.singleplayer else MULTI_PLAYER_FILE
    try:
        with open(filename, "r", encoding="utf-8") as score_file:
            high_scores = json.load(score_file)
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = DEFAULT_HIGH_SCORES
    return high_scores


def display_high_scores(game, screen, score_key):
    """Display the high scores on the screen."""
    high_scores = load_high_scores(game)

    try:
        scores = high_scores[score_key]
    except KeyError:
        scores = []

    ranked_entries = [
        (i + 1, entry["name"], entry["score"])
        for i, entry in enumerate(scores)
        if isinstance(entry, dict)
    ]

    rank_strings = [
        f"{RANK_POSITIONS.get(rank, str(rank))} {name}"
        for rank, name, score in ranked_entries
    ]
    score_strings = [f"{score}" for _, _, score in ranked_entries]

    score_text = "\n".join(score_strings)
    rank_text = "\n".join(rank_strings)

    screen_width, screen_height = screen.get_size()
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    title_x = int(center_x - 520)
    title_y = int(center_y - 150)
    rank_x = int(center_x - 550)
    rank_y = int(center_y - 50)
    score_x = int(center_x - 270)
    score_y = rank_y

    title_font = pygame.font.SysFont("impact", int(screen_height * 0.07))
    scores_font = pygame.font.SysFont("impact", int(screen_height * 0.05))

    text_surfaces, text_rects = render_text(
        "HIGH SCORES",
        title_font,
        (255, 215, 0),
        (title_x, title_y),
        int(screen_height * 0.06),
    )

    rank_surfaces, rank_rects = render_text(
        rank_text, scores_font, "red", (rank_x, rank_y), int(screen_height * 0.05)
    )

    scores_surfaces, scores_rects = render_text(
        score_text, scores_font, "red", (score_x, score_y), int(screen_height * 0.05)
    )

    for surfaces, rects in [
        (text_surfaces, text_rects),
        (rank_surfaces, rank_rects),
        (scores_surfaces, scores_rects),
    ]:
        for surface, rect in zip(surfaces, rects):
            screen.blit(surface, rect)


def display_game_modes_description(screen, description):
    """Render game modes description on screen."""
    screen_width, screen_height = screen.get_size()
    font = pygame.font.SysFont("verdana", int(screen_height * 0.021))
    text_x = int(screen_width * 0.56)
    text_y = 470
    text_surfaces, text_rects = render_text(
        description, font, "white", (text_x, text_y), int(screen_height * 0.03)
    )

    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, text_rects[i])


def calculate_control_positions(center, x_offset):
    """Calculate the positions of player 1 and player 2 controls."""
    p1_controls_x = center[0] - x_offset
    p2_controls_x = center[0] + x_offset
    y_pos = 250
    return (p1_controls_x, y_pos), (p2_controls_x, y_pos)


def display_controls(controls_frame, settings):
    """Display controls on screen."""
    surface_width, _ = settings.get_size()
    center = settings.get_rect().center

    # Constants for positions
    top_left = (50, 220)
    p2_top_right = (surface_width - 50, 220)
    x_offset = 600

    # Load player 1 and player 2 controls
    p1_controls, p1_controls_rect = load_controls_image(
        controls_frame, {"topleft": top_left}
    )
    p2_controls, p2_controls_rect = load_controls_image(
        controls_frame, {"topright": p2_top_right}
    )

    # Calculate the positions of player 1 and player 2 controls
    p1_pos, p2_pos = calculate_control_positions(center, x_offset)
    p1_controls_rect.topleft = p1_pos
    p2_controls_rect.topright = p2_pos

    font = pygame.font.SysFont("arialbold", 35)
    color = "white"

    t1_surfaces, t1_rects = render_text(
        P1_CONTROLS,
        font,
        color,
        (p1_controls_rect.left + 30, p1_controls_rect.top + 30),
        25,
    )
    t2_surfaces, t2_rects = render_text(
        P2_CONTROLS,
        font,
        color,
        (p2_controls_rect.left + 30, p2_controls_rect.top + 30),
        25,
    )

    return (
        p1_controls,
        p1_controls_rect,
        p2_controls,
        p2_controls_rect,
        t1_surfaces,
        t1_rects,
        t2_surfaces,
        t2_rects,
    )


def display_message(screen, message, duration):
    """Display a message on the screen for a specified amount of time."""
    font = pygame.font.SysFont("verdana", 14)
    text = font.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(int(duration * 1000))


def get_player_name(
    screen, background_image, cursor, high_score, game_end_img=None, game_end_rect=None
):
    """Get the player name for the high score."""

    # Set up fonts and colors
    font = pygame.font.SysFont("verdana", 19)
    text_font = pygame.font.SysFont("verdana", 23)
    text_color = pygame.Color("silver")

    # Set up input box and initial player name
    input_box = pygame.Rect(0, 0, 200, 26)
    input_box.center = (screen.get_width() / 2 + 100, screen.get_height() / 2)
    player_name = "Player"

    # Set up buttons
    button_info = [
        {
            "label": "Close",
            "rect": pygame.Rect(
                (input_box.centerx + 20, input_box.centery + 20), (65, 24)
            ),
        },
        {
            "label": "Save",
            "rect": pygame.Rect(
                (input_box.centerx - 75, input_box.centery + 20), (50, 24)
            ),
        },
    ]

    # Draw buttons function
    def draw_buttons():
        for button in button_info:
            pygame.draw.rect(
                screen, (0, 0, 0, 0), button["rect"]
            )  # Set background color to transparent
            text_surface = font.render(button["label"], True, text_color)
            text_x = button["rect"].centerx - text_surface.get_width() / 2
            text_y = button["rect"].centery - 13
            screen.blit(text_surface, (text_x, text_y))

    # Draw text label fuction
    def draw_label(text, pos):
        text_surface = text_font.render(text, True, text_color)
        text_x = pos[0] - text_surface.get_width() / 2
        text_y = pos[1] - 18
        screen.blit(text_surface, (text_x, text_y))

    # Loop until player name is confirmed or canceled
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return player_name  # Exit loop and return player name
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isalnum() and len(player_name) < 10:
                    player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in button_info:
                    if button["rect"].collidepoint(event.pos):
                        if button["label"] == "Close":
                            return None  # Exit loop without saving the name
                        if button["label"] == "Save":
                            return player_name  # Exit loop and return player name

        screen.blit(background_image, (0, 0))
        if game_end_img is not None and game_end_rect is not None:
            screen.blit(game_end_img, game_end_rect)

        # Draw the input box and player name
        pygame.draw.rect(screen, text_color, input_box, 1)
        text_surface = font.render(player_name, True, pygame.Color(90, 90, 90))
        screen.blit(text_surface, (input_box.x + 5, input_box.y))

        # Draw the high score
        high_score_text = f"High Score: {high_score}"
        high_score_surface = text_font.render(high_score_text, True, text_color)
        high_score_rect = high_score_surface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 - 100)
        )
        screen.blit(high_score_surface, high_score_rect)

        # Draw label, buttons and cursor
        draw_label("High score name:", (input_box.centerx - 205, input_box.centery))
        draw_buttons()
        cursor()

        pygame.display.flip()
