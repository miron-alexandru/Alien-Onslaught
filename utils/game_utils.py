"""The "utils" module provides various utility functions"""
import os
import json
import pygame

from .constants import P1_CONTROLS, P2_CONTROLS


def load_frames(filename_pattern, num_frames, frame_list, start=0):
    """Loads a sequence of images frames into a list"""
    for i in range(start, start + num_frames):
        filename = filename_pattern.format(i)
        path = os.path.join("images", filename)
        image = pygame.image.load(path)
        frame_list.append(image)

def load_alien_images(alien_prefix):
    """Load the images for the given alien prefix."""
    frames = []
    for i in range(6):
        filename = f'images/aliens/{alien_prefix}_{i}.png'
        frame = pygame.image.load(filename)
        frames.append(frame)

    return frames


def load_button_imgs(button_names):
    """Load button images"""
    button_images = {}
    for name in button_names:
        filename = f"images/buttons/{name}.png"
        button_images[name] = filename
    return button_images


def load_controls_image(image_loc, image_name, position):
    """Loads images for controls displayed on menu screen"""
    image = pygame.image.load(image_loc[image_name])
    rect = image.get_rect(**position)
    return image, rect


def render_text(text, font, color, start_pos, line_spacing, second_color=None):
    """Render text with new_lines and tabs"""
    lines = text.split('\n')

    text_surfaces = []
    text_rects = []

    tab_width = 10  # Number of spaces per tab

    for i, line in enumerate(lines):
        # Replace tabs with spaces
        line = line.replace('\t', ' ' * tab_width)

        if i  == 0 and second_color:
            text_surface = font.render(line, True, second_color, None)
        else:
            text_surface = font.render(line, True, color, None)

        text_rect = text_surface.get_rect(topleft=(start_pos[0],
                                                        start_pos[1] + i * line_spacing))
        text_surfaces.append(text_surface)
        text_rects.append(text_rect)

    return text_surfaces, text_rects


def display_high_scores(screen):
    """Display the high scores on the screen."""
    # Load the high score data from the JSON file,
    # or create a new high score list if there is an error
    filename = 'high_score.json'
    try:
        with open(filename, 'r', encoding='utf-8') as score_file:
            high_scores = json.load(score_file)
    except json.JSONDecodeError:
        high_scores = {'high_scores': [0] * 10}

    # Get the scores from the high score list and create a new list of tuples
    # containing the score and its rank
    scores = high_scores['high_scores']
    ranked_scores = [(i, score) for i, score in enumerate(scores, 1) if score]

    # Create formatted strings for each rank and score
    rank_strings = [
        f"{('1st' if rank == 1 else '2nd' if rank == 2 else '3rd' if rank == 3 else rank)}:" 
        for rank, score in ranked_scores
    ]
    score_strings = [f"{score}" for rank, score in ranked_scores]

    score_text = "\n".join(score_strings)
    rank_text = "\n".join(rank_strings)

    # Calculate the relative position of the text based on the screen size
    screen_width, screen_height = screen.get_size()
    title_x = int(screen_width * 0.065)
    title_y = int(screen_height * 0.35)
    rank_x = int(screen_width * 0.03)
    rank_y = int(screen_height * 0.45)
    score_x = int(screen_width * 0.25)
    score_y = rank_y

    # Render the score text and rank text as surfaces with new lines using different fonts
    font = pygame.font.SysFont('impact', int(screen_height * 0.07))
    text_surfaces, text_rects = render_text(
            "HIGH SCORES",
            font,
            'yellow',
            (title_x, title_y),
            int(screen_height * 0.06))

    font = pygame.font.SysFont('impact', int(screen_height * 0.05))
    rank_surfaces, rank_rects = render_text(
            rank_text,
            font,
            'red',
            (rank_x, rank_y),
            int(screen_height * 0.05))

    font = pygame.font.SysFont('impact', int(screen_height * 0.05))
    scores_surfaces, scores_rects = render_text(
            score_text,
            font,
            'red',
            (score_x, score_y),
            int(screen_height * 0.05))

    # Blit the score text surfaces onto the screen using a loop to avoid repetitive code
    for surfaces, rects in [(text_surfaces, text_rects), (rank_surfaces, rank_rects),
                                    (scores_surfaces, scores_rects)]:
        for surface, rect in zip(surfaces, rects):
            screen.blit(surface, rect)


def display_controls(buttons, settings):
    """Display controls on screen"""
    p1_controls, p1_controls_rect = load_controls_image(
                                            buttons,
                                            'player_controls',
                                            {'topleft': (50, 50)})
    p2_controls, p2_controls_rect = load_controls_image(
                                            buttons,
                                            'player_controls',
                                            {'topright':
                                            (settings.get_width() - 50, 50)})

    font = pygame.font.SysFont('arialbold', 35)
    color = 'white'
    t1_surfaces, t1_rects = render_text(
                                P1_CONTROLS,
                                font, color,
                                (p1_controls_rect.left + 30,
                                p1_controls_rect.top + 30), 25)
    t2_surfaces, t2_rects = render_text(
                                    P2_CONTROLS,
                                    font, color,
                                    (p2_controls_rect.left + 30,
                                    p2_controls_rect.top + 30), 25)

    return (p1_controls, p1_controls_rect,
            p2_controls, p2_controls_rect,
            t1_surfaces, t1_rects,
            t2_surfaces, t2_rects)
