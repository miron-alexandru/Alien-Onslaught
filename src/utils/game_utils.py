"""The 'game_utils' module contains various utility functions."""

import os
import sys
import json
import pygame

from src.utils.constants import (
    P1_CONTROLS,
    P2_CONTROLS,
    GAME_CONTROLS,
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
    BASE_PATH = os.path.join(sys._MEIPASS, "game_assets", "images")  # type: ignore
else:
    # Running as a regular script
    BASE_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "game_assets", "images")
    )

if hasattr(sys, "_MEIPASS"):
    # Running as a PyInstaller bundle
    SOUND_PATH = os.path.join(sys._MEIPASS, "game_assets", "sounds")  # type: ignore
else:
    # Running as a regular script
    SOUND_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "game_assets", "sounds")
    )

# IMAGE RELATED FINCTIONS


def scale_image(image, scale_factor):
    """Scales the given image and returns it."""
    return pygame.transform.smoothscale(
        image,
        (
            int(image.get_width() * scale_factor),
            int(image.get_height() * scale_factor),
        ),
    )


def load_single_image(relative_path):
    """Loads an image based on the BASED_PATH."""
    base_path = BASE_PATH
    image_path = os.path.join(base_path, relative_path)
    return pygame.image.load(image_path)


def load_images(image_dict):
    """A function that loads multiple images from a dict of the form:
    key: image name
    value: path to image location"""
    return {
        key: pygame.image.load(os.path.join(BASE_PATH, value))
        for key, value in image_dict.items()
    }


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


def draw_image(screen, image, rect):
    """Draw a image to the screen."""
    screen.blit(image, rect)


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


# SOUND RELATED FUNCTIONS:


def load_sound_files(sounds_dict):
    """A function that loads multiple sounds from a dict of the form:
    key: sound name:
    value: path to sound location."""
    pygame.mixer.init()
    return {
        key: pygame.mixer.Sound(os.path.join(SOUND_PATH, value))
        for key, value in sounds_dict.items()
    }


def load_music_files(music_dict):
    """A function that loads multiple music files from a dict of the form:
    key: music name:
    value: path to music file."""
    pygame.mixer.init()
    return {
        key: value if value is None else os.path.join(SOUND_PATH, value)
        for key, value in music_dict.items()
    }


def play_music(music_files, music_name):
    """A function that plays the specified music using its name."""
    music_path = music_files.get(music_name)
    if music_path is not None:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)


def set_sounds_volume(sounds, volume):
    """Set the volume for all sounds in the passed sounds dict."""
    for sound in sounds.values():
        sound.set_volume(volume)


def set_music_volume(music, volume):
    """Set the volume of all music."""
    for _ in music.values():
        pygame.mixer.music.set_volume(volume)


def get_available_channels():
    """Returns a list of available sound channels."""
    num_channels = pygame.mixer.get_num_channels()
    available_channels = []
    for channel_num in range(num_channels):
        channel = pygame.mixer.Channel(channel_num)
        if not channel.get_busy():
            available_channels.append(channel)
    return available_channels


def play_sound(sounds_list, sound_name):
    """Plays a certain sound located in the 'sounds_list' on an available sound channel."""
    if sound_name == "bullet":
        channel = pygame.mixer.Channel(7)
    elif sound_name == "alien_exploding":
        channel = pygame.mixer.Channel(6)
    elif available_channels := get_available_channels():
        channel = available_channels[0]
    else:
        channel = pygame.mixer.Channel(1)

    channel.play(sounds_list[sound_name])


# MISC FUNCTIONS:


def create_save_dir(save_folder):
    """Create the save directory if it does not exist."""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)


def set_attribute(obj, attribute_chain, value):
    """Set the attribute in the nested object."""
    for attribute in attribute_chain[:-1]:
        obj = obj[attribute] if isinstance(obj, dict) else getattr(obj, attribute)
    if isinstance(obj, dict):
        obj[attribute_chain[-1]] = value
    else:
        setattr(obj, attribute_chain[-1], value)


def get_colliding_sprites(ship, bullets_or_missiles):
    """Returns the sprites that collide with the given ship."""
    return pygame.sprite.spritecollide(ship, bullets_or_missiles, False)


def get_boss_rush_title(level):
    """Set the boss rush title for each level."""
    boss_rush_key = f"boss{level}"
    boss_rush_title = BOSS_RUSH.get(boss_rush_key, f"Level {level}")
    return boss_rush_title.split("/")[-1].split(".png")[0].title()


def display_description(screen, description, text_x, text_y):
    """Render description on screen."""
    _, screen_height = screen.get_size()
    font = pygame.font.SysFont("verdana", 15)
    text_surfaces, text_rects = render_text(
        description, font, "white", (text_x, text_y), int(screen_height * 0.03)
    )

    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, text_rects[i])


def render_bullet_num(bullets, x_pos, y_pos, right_aligned=False):
    """Renders the bullet number and returns the image and rect."""
    font = pygame.font.SysFont("", 25)
    text_color = (238, 75, 43)
    bullets_str = f"Remaining bullets: {bullets}" if bullets else ""
    bullets_num_img = font.render(bullets_str, True, text_color, None)
    bullets_num_rect = bullets_num_img.get_rect()
    bullets_num_rect.top = y_pos

    if right_aligned:
        bullets_num_rect.right = x_pos
    else:
        bullets_num_rect.left = x_pos

    return bullets_num_img, bullets_num_rect


def display_message(screen, message, duration):
    """Display a message on the screen for a specified amount of time."""
    font = pygame.font.SysFont("verdana", 14)
    text = font.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(int(duration * 1000))


def display_custom_message(screen, message, ship, cosmic=False, powers=False):
    """Display a message to the right of the ship."""
    ship_rect = ship.rect
    font = pygame.font.SysFont("verdana", 10)
    if powers:
        text = font.render(message, True, (173, 216, 230))
    else:
        text = font.render(message, True, (255, 0, 0))

    if cosmic:
        text_rect = text.get_rect(top=ship_rect.top - 20, left=ship_rect.left + 5)
    else:
        text_rect = text.get_rect(top=ship_rect.top - 5, left=ship_rect.right)
    screen.blit(text, text_rect)


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


def calculate_control_positions(center, x_offset):
    """Calculate the positions of player 1 and player 2 controls."""
    p1_controls_x = center[0] - x_offset
    p2_controls_x = center[0] + x_offset
    y_pos = 260
    return (p1_controls_x, y_pos), (p2_controls_x, y_pos)


def display_controls(controls_surface, surface):
    """Display controls on screen."""
    center = surface.get_rect().center
    font = pygame.font.SysFont("verdana", 20)
    color = "white"

    p1_controls_img, p1_controls_img_rect = load_controls_image(
        controls_surface, {"topleft": (0, 0)}
    )
    p2_controls_img, p2_controls_img_rect = load_controls_image(
        controls_surface, {"topright": (0, 0)}
    )

    p1_pos, p2_pos = calculate_control_positions(center, 600)
    p1_controls_img_rect.topleft = p1_pos
    p2_controls_img_rect.topright = p2_pos

    game_controls_img, game_controls_img_rect = load_controls_image(
        controls_surface,
        {
            "midbottom": (
                p1_controls_img_rect.centerx,
                p1_controls_img_rect.bottom + 225,
            )
        },
    )

    p1_controls_text, p1_controls_text_rects = render_text(
        P1_CONTROLS,
        font,
        color,
        (p1_controls_img_rect.left + 25, p1_controls_img_rect.top + 15),
        22,
    )

    p2_controls_text, p2_controls_text_rects = render_text(
        P2_CONTROLS,
        font,
        color,
        (p2_controls_img_rect.left + 25, p2_controls_img_rect.top + 15),
        22,
    )

    game_controls_text, game_controls_text_rects = render_text(
        GAME_CONTROLS,
        font,
        color,
        (game_controls_img_rect.left + 25, game_controls_img_rect.top + 15),
        22,
    )

    return (
        p1_controls_img,
        p1_controls_img_rect,
        p2_controls_img,
        p2_controls_img_rect,
        p1_controls_text,
        p1_controls_text_rects,
        p2_controls_text,
        p2_controls_text_rects,
        game_controls_img,
        game_controls_img_rect,
        game_controls_text,
        game_controls_text_rects,
    )


def render_simple_text(text, font, color, x, y):
    """Render a simple text."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    return text_surface, text_rect


def display_simple_message(screen, text, font, color, delay_time):
    """Display a simple message on screen."""
    message_surface, message_rect = render_simple_text(
        text, font, color, screen.get_width() // 2, 600
    )
    screen.blit(message_surface, message_rect)
    pygame.display.flip()
    pygame.time.delay(delay_time)


# HIGH SCORE RELATED FUNCTIONS:


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


def draw_buttons(screen, button_info, font, text_color):
    """Render buttons on screen."""
    for button in button_info:
        pygame.draw.rect(
            screen, (0, 0, 0, 0), button["rect"]
        )  # Set background color to transparent
        text_surface = font.render(button["label"], True, text_color)
        text_x = button["rect"].centerx - text_surface.get_width() // 2
        text_y = button["rect"].centery - 13
        screen.blit(text_surface, (text_x, text_y))


def render_label(screen, text, pos, text_font, text_color):
    """Render label on screen."""
    text_surface = text_font.render(text, True, text_color)
    text_x = pos[0] - text_surface.get_width() // 2
    text_y = pos[1] - 18
    screen.blit(text_surface, (text_x, text_y))


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
        screen.blit(
            font.render(player_name, True, pygame.Color(90, 90, 90)),
            (input_box.x + 5, input_box.y),
        )

        # Draw the high score
        high_score_surface = text_font.render(
            f"High Score: {high_score}", True, text_color
        )
        screen.blit(
            high_score_surface,
            high_score_surface.get_rect(
                center=(screen.get_width() / 2, screen.get_height() / 2 - 100)
            ),
        )

        # Draw label, buttons, and cursor
        render_label(
            screen,
            "High score name:",
            (input_box.centerx - 205, input_box.centery),
            text_font,
            text_color,
        )
        draw_buttons(screen, button_info, font, text_color)
        cursor()

        pygame.display.flip()
