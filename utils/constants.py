"""Module that stores the constants for the game"""
# Button names dict, used for loading and then creating the buttons in the game.

BUTTON_NAMES = [
                "play_button", "quit_button", "menu_button",
                'difficulty', 'easy', 'medium', 'hard', 'high_scores',
                'game_modes', 'endless', 'normal', 'slow_burn', 'meteor_madness',
                "single_player", "multiplayer","player_controls",
                "menu_quit_button", 'boss_rush', 'last_bullet',
]


# Player1 controls
P2_CONTROLS = ("Phoenix controls:\n"
                "Movement: Arrow Keys\n"
                "Shoot: Enter\n"
                "Ship skin: Numpad 1, 2, 3\n"
                "Pause: P")


# Player2 controls
P1_CONTROLS = ("Thunderbird controls:\n"
                "Movement: W, A, S, D\n"
                "Shoot: Space\n"
                "Ship skin: 1, 2, 3\n"
                "Pause: P")


# Images for different parts of the game.
BACKGROUNDS = {
    'space': 'images/background/space.jpg',
    'space2': 'images/background/space2.png',
    'space3': 'images/background/space3.jpg',
    'space4': 'images/background/space4.jpg',
}


AVAILABLE_BULLETS_MAP = {
        1: 9,
        2: 9,
        3: 9,
        4: 9,
        5: 17,
        6: 17,
        7: 17,
        8: 17,
        9: 17,
        10: 25,
}

ALIENS_HP_MAP = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 3,
}


AVAILABLE_BULLETS_MAP_SINGLE = {
        1: 17,
        2: 17,
        3: 17,
        4: 17,
        5: 34,
        6: 34,
        7: 34,
        8: 34,
        9: 34,
        10: 50,
}

OTHER = {
    'gameover': 'images/other/gameover.png',
    'pause': 'images/other/pause.png',
    'heart': 'images/other/heart.png',
    'game_title': 'images/other/alien_onslaught.png'
}


POWERS = {
    'power': 'images/power_ups/power_up.png',
    'health': 'images/power_ups/health.png',
}

WEAPON_BOXES = {
    'blaster': 'images/weapon_boxes/box1.png',
    'discharger': 'images/weapon_boxes/box2.png',
    'distorter': 'images/weapon_boxes/box3.png',
    'entangler': 'images/weapon_boxes/box4.png',
    'disruptor': 'images/weapon_boxes/box5.png',
}


ALIEN_BULLETS_IMG = {
    'alien_bullet': 'images/alien_bullets/alien_bullet.png',
    'xanathar_bullet': 'images/alien_bullets/xanathar_bullet.png',
    'scorpion_bullet': 'images/alien_bullets/scorpion_bullet.png',
    'mothership_bullet': 'images/alien_bullets/mothership_bullet.png',
    'xyranth_bullet': 'images/alien_bullets/xyranth_bullet.png',
    'nephilim_bullet': 'images/alien_bullets/nephilim_bullet.png',
    'nebulon_bullet': 'images/alien_bullets/nebulon_bullet.png',
    'astaroth_bullet': 'images/alien_bullets/astaroth_bullet.png',
    'krynnax_bullet': 'images/alien_bullets/krynnax_bullet.png',
    'arcturus_bullet': 'images/alien_bullets/arcturus_bullet.png',
    'xydonix_bullet': 'images/alien_bullets/xydonix_bullet.png',
    'valtor_bullet': 'images/alien_bullets/valtor_bullet.png',
    'xalaxar_bullet': 'images/alien_bullets/xalaxar_bullet.png',
    'zorgoth_bullet': 'images/alien_bullets/zorgoth_bullet.png',
    'typhon_bullet': 'images/alien_bullets/typhon_bullet.png',
    'xixo_bullet': 'images/alien_bullets/xixo_bullet.png',
}


BOSS_RUSH = {
    'arcturus': 'images/boss_rush/arcturus.png',
    'astaroth': 'images/boss_rush/astaroth.png',
    'krynnax': 'images/boss_rush/krynnax.png',
    'nebulon': 'images/boss_rush/nebulon.png',
    'nephilim': 'images/boss_rush/nephilim.png',
    'xydonix': 'images/boss_rush/xydonis.png',
    'typhon': 'images/boss_rush/typhon.png',
    'valtor': 'images/boss_rush/valtor.png',
    'xalaxar': 'images/boss_rush/xalaxar.png',
    'zorgoth': 'images/boss_rush/zorgoth.png',
    'xanathar': 'images/aliens/xanathar.png',
    'scorpion': 'images/aliens/scorpion.png',
    'mothership': 'images/aliens/mothership.png',
    'xyranth': 'images/aliens/xyranth.png',
    'xixo': 'images/boss_rush/xixo.png',

}

boss_rush_image_map = {
                1: 'nephilim',
                2: 'xanathar',
                3: 'scorpion',
                4: 'nebulon',
                5: 'astaroth',
                6: 'krynnax',
                7: 'xyranth',
                8: 'arcturus',
                9: 'xydonix',
                10: 'mothership',
                11: 'valtor',
                12: 'xalaxar',
                13: 'zorgoth',
                14: 'typhon',
                15: 'xixo',
}

boss_rush_bullet_map = {
                1: 'nephilim_bullet',
                2: 'xanathar_bullet',
                3: 'scorpion_bullet',
                4: 'nebulon_bullet',
                5: 'astaroth_bullet',
                6: 'krynnax_bullet',
                7: 'xyranth_bullet',
                8: 'arcturus_bullet',
                9: 'xydonix_bullet',
                10: 'mothership_bullet',
                11: 'valtor_bullet',
                12: 'xalaxar_bullet',
                13: 'zorgoth_bullet',
                14: 'typhon_bullet',
                15: 'xixo_bullet',
}

normal_bullet_map = {
    15: 'scorpion_bullet',
    20: 'mothership_bullet',
    25: 'xyranth_bullet',
}

boss_rush_points_map = {
            1: 1000,
            2: 1250,
            3: 1700,
            4: 2000,
            5: 2250,
            6: 2650,
            7: 3100,
            8: 3500,
            9: 3900,
            10: 4200,
            11: 4500,
            13: 5500,
            14: 8000,
            15: 10000,
}

boss_rush_hp_map = {
            1: 25,
            2: 50,
            3: 75,
            4: 85,
            5: 99,
            6: 110,
            7: 130,
            8: 150,
            9: 175,
            10: 195,
            11: 220,
            13: 250,
            14: 280,
            15: 300,

}

normal_boss_points = {
    15: 5000,
    20: 7000,
    25: 10000,
}

normal_boss_hp_map = {
    10: 50,
    15: 75,
    20: 95,
    25: 100,
}

normal_image_map = {
    15: 'scorpion',
    20: 'mothership',
    25: 'xyranth',
}



SHIPS = {
    'thunderbolt': 'images/projectiles/bullets/thunder_bullet.png',
    'firebird': 'images/projectiles/bullets/fire_bullet.png',
    'thunderbird': 'images/ships/ship1.png',
    'phoenix': 'images/ships/ship4.png',

    }

WEAPONS = {
    'blaster': 'images/projectiles/bullets/blaster.png',
    'discharger': 'images/projectiles/bullets/discharger.png',
    'distorter': 'images/projectiles/bullets/distorter.png',
    'entangler': 'images/projectiles/bullets/entangler.png',
    'disruptor': 'images/projectiles/bullets/disruptor.png',
}

# Sounds for the game.
SOUNDS = {
    'bullet': 'sounds/fire.wav',
}

# Dict used to map levels to alien images
LEVEL_PREFIX = {
        1: "Alien1",
        2: "Alien1",
        3: "Alien2",
        4: "Alien2",
        5: "Alien3",
        6: "Alien3",
        7: "Alien4",
        8: "Alien4",
    }


GAME_CONSTANTS = {
    'ENDLESS_MAX_ALIENS': 50,
    'MAX_ALIEN_SPEED': 4.0,
    'MAX_ALIEN_NUM': 35,
    'POWER_SPEED': 1.5,
    'SCORE_SCALE': 4,
    'MAX_AS_SPEED': 3.0,
    'MAX_AS_FREQ': 200,
}


DIFFICULTIES = {
    'EASY': 0.3,
    'MEDIUM': 0.5,
    'HARD': 0.7
}

# Ships settings
MAX_HP = 5
STARTING_HP = 3

BOSS_LEVELS = [10, 15, 20, 25]
