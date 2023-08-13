"""
The 'loading_screen' module contains the LoadingScreen class
that manages the loading screen.
"""

import pygame


class LoadingScreen:
    """Manages the loading screen for the game,
    including updating the progress of the loading
    bar and drawing it on the screen.
    """

    def __init__(self, screen):
        self.screen = screen
        self.load_bar_width = 400
        self.load_bar_height = 25
        self.load_percent = 0
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render("Loading...", True, (255, 255, 255))

    def update(self, progress):
        """Update progress of the loading bar."""
        self.load_percent = progress
        self.draw()

    def draw(self):
        """Draw the loading screen on the screen."""
        screen_width, screen_height = self.screen.get_size()
        load_bar_x = (screen_width - self.load_bar_width) // 2
        load_bar_y = (screen_height - self.load_bar_height) // 2
        load_bar_fill = self.load_bar_width * self.load_percent // 100

        self.screen.fill((2, 24, 49, 255))
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                load_bar_x,
                load_bar_y,
                self.load_bar_width,
                self.load_bar_height,
            ),
            2,
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (load_bar_x, load_bar_y, load_bar_fill, self.load_bar_height),
        )

        self.screen.blit(
            self.text,
            (
                (screen_width - self.text.get_width()) // 2,
                (screen_height - self.text.get_height()) // 2 - 40,
            ),
        )
        pygame.display.update()
