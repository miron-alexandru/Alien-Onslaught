import os
from setuptools import setup, find_packages

long_description = """
## Alien-Onslaught
- Alien Onslaught is an action-packed game that will test your shooting skills and reflexes. The game is set in outer space, where you must shoot fleets of aliens to reach higher levels and increase your high score. With each level, the game becomes more challenging as the aliens become stronger and faster, bosses are starting to appear, and more asteroids rain down from above.

- The game offers a range of game modes (e.g.: Boss Rush, Endless Onslaught, Cosmic Conflict (PVP)), including single-player and multiplayer modes, where you can choose to battle it out with friends or take on the aliens alone. In game you can also get a variety of ship power-ups, including increased ship speed, bullet speed, and fire power, as well as shields that protect you from enemy fire. It also includes a high score system where players can compete with others for the top spot on the leaderboard, boss fights, different weapons, different player ship types, and more other features.

### Requirements:
- Python 3.7 or later
- Pygame 2.0 or later

### Game Launch:
* pip install alien-onslaught
* python -m src.alien_onslaught

## Controls:
#### Gameplay:
#### Player 1 (Thunderbird):
* Move: W, A, S, D
* Fire: Space
* Laser: C
* Launch Missiles: X

#### Player 2 (Phoenix):
* Move: Arrow Keys
* Fire: Enter
* Laser: R-Shift
* Launch Missiles: R-Ctrl

#### UI Controls:
* Toggle Fullscreen: F
* Pause: P
* - While Paused:
*  Save Game: S
*  Restart: R
*  Return to Game Menu: ESC
*  Return to Main Menu: M
*  Quit: Q

### Game images can be found [here](https://github.com/KhadaAke/Alien-Onslaught/tree/main/game_assets/images/game_images)
"""

setup(
    name="alien-onslaught",
    version="3.3.2",
    author="Miron Alexandru",
    author_email="khadaake@gmail.com",
    description="Alien Onslaught: An action-packed arcade space shooter game.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "game_assets": ["images/**/*", "sounds/**/*"],
    },
    install_requires=["pygame"],
    project_urls={
    "Source Code": "https://github.com/KhadaAke/Alien-Onslaught",
    },
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent",
    "Topic :: Games/Entertainment",
    "Topic :: Software Development :: Libraries :: pygame",
    ],
)
