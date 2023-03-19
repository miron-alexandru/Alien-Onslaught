"""Module that stores the constants for the game"""
# Button names dict, used for loading and then creating the buttons in the game.
BUTTON_NAMES = [
                "play_button", "quit_button", "menu_button",
                'difficulty', 'easy', 'medium', 'hard', 'high_scores',
                'game_modes', 'endless', 'normal', 'last_stand',
                "single_player", "multiplayer","player_controls",
                "menu_quit_button"
]


# Player1 controls
P1_CONTROLS = ("Player 1:\n"
                "Movement: Arrow Keys\n"
                "Shoot: Enter\n"
                "Ship skin: Numpad 1, 2, 3\n"
                "Pause: P")


# Player2 controls
P2_CONTROLS = ("Player 2:\n"
                "Movement: W, A, S, D\n"
                "Shoot: Space\n"
                "Ship skin: 1, 2, 3\n"
                "Pause: P")


# Images for different parts of the game.
BACKGROUNDS = {
    'space': 'images/background/space.jpg',
    'space2': 'images/background/space2.png',
    'space4': 'images/background/space4.jpg',
}


OTHER = {
    'gameover': 'images/other/gameover.png',
    'pause': 'images/other/pause.png',
    'heart': 'images/other/heart.png',
}


POWER_UPS = {
    'power_up': 'images/power_ups/power_up.png',
    'health': 'images/power_ups/health.png',
}


ALIENS = {
    'alien_bullet': 'images/alien_bullets/alien_bullet.png',
    'xanathar_bullet': 'images/alien_bullets/xanathar_bullet.png',
    'scorpion_bullet': 'images/alien_bullets/scorpion_bullet.png',
    'mothership_bullet': 'images/alien_bullets/mothership_bullet.png',
    'xanathar': 'images/aliens/xanathar.png',
    'scorpion': 'images/aliens/scorpion.png',
    'mothership': 'images/aliens/mothership.png',
    }


SHIPS = {
    'thunderbolt': 'images/player_bullets/thunder_bullet.png',
    'firebird': 'images/player_bullets/fire_bullet.png',
    'thunderbird': 'images/ships/ship1.png',
    'phoenix': 'images/ships/ship4.png',

    }


# Sounds for the game.
SOUNDS = {
    'bullet': 'sounds/fire.wav',
}

# Dict used to map levels to alien images
LEVEL_PREFIX = {
        0: "Alien1",
        3: "Alien2",
        6: "Alien3",
        9: "Alien4",
        12: "Alien4",
    }


GAME_CONSTANTS = {
    'ENDLESS_MAX_ALIENS': 50,
    'MAX_ALIEN_SPEED': 4.0,
    'MAX_ALIEN_NUM': 35,
    'POWER_UP_SPEED': 1.5,
    'SCORE_SCALE': 4,
}


DIFFICULTIES = {
    'EASY': 0.3,
    'MEDIUM': 0.5,
    'HARD': 0.7
}

# Ships settings
MAX_HP = 5
STARTING_HP = 3

BOSS_LEVELS = [10, 15, 20]
