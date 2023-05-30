"""The 'constants' module stores various constant for the game."""

# Button names dict, used for loading and then creating the buttons in the game.
BUTTON_NAMES = [
    "play_button",
    "quit_button",
    "menu_button",
    "difficulty",
    "easy",
    "medium",
    "hard",
    "high_scores",
    "delete_scores",
    "game_modes",
    "endless",
    "normal",
    "slow_burn",
    "meteor_madness",
    "single_player",
    "multiplayer",
    "player_controls",
    "menu_quit_button",
    "boss_rush",
    "last_bullet",
    "cosmic_conflict",
    "one_life_reign",
]

# PLAYER_CONTROLS

# Player2 controls
P2_CONTROLS = (
    "Phoenix controls:\n"
    "Move: Arrow Keys\n"
    "Fire: Enter\n"
    "Change Ship: Numpad 1, 2, 3\n"
    "Launch Missiles: R-Ctrl\n"
    "Pause: P"
)

# Player1 controls
P1_CONTROLS = (
    "Thunderbird controls:\n"
    "Move: W, A, S, D\n"
    "Fire: Space\n"
    "Change Ship: 1, 2, 3\n"
    "Launch Missiles: Z\n"
    "Pause: P"
)


GAME_MODES_DESCRIPTIONS = (
    # Normal
    "Engage in an intense battle against waves of aliens, asteroids and also\n"
    "boss battles, with a standard set of firepower and speed.\n"
    "As you progress, the enemies will become more challenging but,\n"
    "you'll have the opportunity to power up your weapons and defenses.\n\n"
    # Endless Onslaught
    "Survive against an infinite swarm of aliens and asteroids.\n"
    "As time passes, the speed and numbers of your enemies will increase.\n\n"
    # Slow Burn
    "Take on the alien threat with reduced speed and firepower that gradually\n"
    "decreases over time.\n\n"
    # Meteor Madness
    "Navigate through a relentless barrage of asteroids that become\n"
    "increasingly difficult to avoid as their numbers and speed increase,\n"
    "and your speed is also decreasing over time.\n\n"
    # Boss Rush
    "Face off against a series of challenging bosses with each level presenting\n"
    "a new challenge.\n\n"
    # Last Bullet
    "You must use your limited supply of bullets to fight off waves of aliens.\n"
    "If you run out of bullets, you'll become inactive and the game will be over.\n\n"
    # Cosmic Conflict
    "Prepare for an intense PVP space battle as you go head-to-head\n"
    "in a 1v1 showdown.\n\n"
    # One Life Reign
    "Embrace unstoppable strength, but remember, a single life is all you have.\n"
    "Battle against relentless alien forces, navigate deadly challenges,\n"
    "and face epic bosses."
).split("\n\n")


# Images for different parts of the game.
BACKGROUNDS = {
    "space": "../game_assets/images/background/space.jpg",
    "space2": "../game_assets/images/background/space2.png",
    "space3": "../game_assets/images/background/space3.jpg",
    "space4": "../game_assets/images/background/space4.jpg",
}

# Bullets map dicts, used to map available bullets to each level
# in the Last Bullet game mode both singleplayer and multiplayer.

AVAILABLE_BULLETS_MAP = {
    range(1, 5): 9,
    range(5, 10): 17,
}

AVAILABLE_BULLETS_MAP_SINGLE = {
    range(1, 5): 17,
    range(5, 10): 34,
}


ALIENS_HP_MAP = {
    1: 1,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 3,
}


# Other images used in the game.
OTHER = {
    "gameover": "../game_assets/images/other/gameover.png",
    "victory": "../game_assets/images/other/victory.png",
    "thunder_win": "../game_assets/images/other/thunder_victory.png",
    "phoenix_win": "../game_assets/images/other/phoenix_victory.png",
    "pause": "../game_assets/images/other/pause.png",
    "heart": "../game_assets/images/other/heart.png",
    "game_title": "../game_assets/images/other/alien_onslaught.bmp",
    "cursor": "../game_assets/images/other/cursor.bmp",
}


POWERS = {
    "power": "../game_assets/images/power_ups/power_up.png",
    "health": "../game_assets/images/power_ups/health.png",
}

WEAPON_BOXES = {
    "thunderbolt": "../game_assets/images/weapon_boxes/thunder_box.png",
    "firebird": "../game_assets/images/weapon_boxes/fire_box.png",
    "blaster": "../game_assets/images/weapon_boxes/blaster_box.png",
    "discharger": "../game_assets/images/weapon_boxes/discharger_box.png",
    "distorter": "../game_assets/images/weapon_boxes/distorter_box.png",
    "entangler": "../game_assets/images/weapon_boxes/entangler_box.png",
    "disruptor": "../game_assets/images/weapon_boxes/disruptor_box.png",
}

WEAPONS = {
    "thunderbolt": "../game_assets/images/projectiles/bullets/thunder_bullet.png",
    "firebird": "../game_assets/images/projectiles/bullets/fire_bullet.png",
    "blaster": "../game_assets/images/projectiles/bullets/blaster.png",
    "discharger": "../game_assets/images/projectiles/bullets/discharger.png",
    "distorter": "../game_assets/images/projectiles/bullets/distorter.png",
    "entangler": "../game_assets/images/projectiles/bullets/entangler.png",
    "disruptor": "../game_assets/images/projectiles/bullets/disruptor.png",
}

ALIEN_BULLETS_IMG = {
    "alien_bullet1": "../game_assets/images/alien_bullets/alien_bullet1.png",
    "alien_bullet2": "../game_assets/images/alien_bullets/alien_bullet2.png",
    "alien_bullet3": "../game_assets/images/alien_bullets/alien_bullet3.png",
    "alien_bullet4": "../game_assets/images/alien_bullets/alien_bullet4.png",
    "alien_bullet5": "../game_assets/images/alien_bullets/alien_bullet5.png",
    "alien_bullet6": "../game_assets/images/alien_bullets/alien_bullet6.png",
    "alien_bullet7": "../game_assets/images/alien_bullets/alien_bullet7.png",
}

BOSS_BULLETS_IMG = {
    "boss_bullet1": "../game_assets/images/alien_bullets/nephilim_bullet.png",
    "boss_bullet2": "../game_assets/images/alien_bullets/xanathar_bullet.png",
    "boss_bullet3": "../game_assets/images/alien_bullets/scorpion_bullet.png",
    "boss_bullet4": "../game_assets/images/alien_bullets/nebulon_bullet.png",
    "boss_bullet5": "../game_assets/images/alien_bullets/astaroth_bullet.png",
    "boss_bullet6": "../game_assets/images/alien_bullets/krynnax_bullet.png",
    "boss_bullet7": "../game_assets/images/alien_bullets/xyranth_bullet.png",
    "boss_bullet8": "../game_assets/images/alien_bullets/arcturus_bullet.png",
    "boss_bullet9": "../game_assets/images/alien_bullets/xydonix_bullet.png",
    "boss_bullet10": "../game_assets/images/alien_bullets/mothership_bullet.png",
    "boss_bullet11": "../game_assets/images/alien_bullets/valtor_bullet.png",
    "boss_bullet12": "../game_assets/images/alien_bullets/xalaxar_bullet.png",
    "boss_bullet13": "../game_assets/images/alien_bullets/zorgoth_bullet.png",
    "boss_bullet14": "../game_assets/images/alien_bullets/typhon_bullet.png",
    "boss_bullet15": "../game_assets/images/alien_bullets/xixo_bullet.png",
    "normal_bullet15": "../game_assets/images/alien_bullets/scorpion_bullet.png",
    "normal_bullet20": "../game_assets/images/alien_bullets/mothership_bullet.png",
    "normal_bullet25": "../game_assets/images/alien_bullets/xyranth_bullet.png",
}


BOSS_RUSH = {
    "boss1": "../game_assets/images/boss_rush/nephilim.png",
    "boss2": "../game_assets/images/aliens/xanathar.png",
    "boss3": "../game_assets/images/aliens/scorpion.png",
    "boss4": "../game_assets/images/boss_rush/nebulon.png",
    "boss5": "../game_assets/images/boss_rush/astaroth.png",
    "boss6": "../game_assets/images/boss_rush/krynnax.png",
    "boss7": "../game_assets/images/aliens/xyranth.png",
    "boss8": "../game_assets/images/boss_rush/arcturus.png",
    "boss9": "../game_assets/images/boss_rush/xydonis.png",
    "boss10": "../game_assets/images/aliens/mothership.png",
    "boss11": "../game_assets/images/boss_rush/valtor.png",
    "boss12": "../game_assets/images/boss_rush/xalaxar.png",
    "boss13": "../game_assets/images/boss_rush/zorgoth.png",
    "boss14": "../game_assets/images/boss_rush/typhon.png",
    "boss15": "../game_assets/images/boss_rush/xixo.png",
    "normal15": "../game_assets/images/aliens/scorpion.png",
    "normal20": "../game_assets/images/aliens/mothership.png",
    "normal25": "../game_assets/images/aliens/xyranth.png",
}


NORMAL_BOSS_POINTS = {
    15: 5000,
    20: 7000,
    25: 10000,
}

NORMAL_BOSS_HP_MAP = {
    10: 50,
    15: 75,
    20: 95,
    25: 100,
}


SHIPS = {
    "thunderbird": "../game_assets/images/ships/ship1.png",
    "phoenix": "../game_assets/images/ships/ship4.png",
}


# Sounds for the game.
MENU_SOUNDS = {
    "menu": "../game_assets/sounds/ui/menu.wav",
    "click_menu": "../game_assets/sounds/ui/click_menu.wav",
    "quit_effect": "../game_assets/sounds/ui/quit_effect.wav",
}

GAME_SOUNDS = {
    "bullet": "../game_assets/sounds/gameplay/fire.wav",
    "explode": "../game_assets/sounds/gameplay/explode.wav",
    "game_over": "../game_assets/sounds/ui/game_over.wav",
    "power_up": "../game_assets/sounds/gameplay/power_up.mp3",
    "penalty": "../game_assets/sounds/gameplay/penalty.wav",
    "health": "../game_assets/sounds/gameplay/health.wav",
    "weapon": "../game_assets/sounds/gameplay/weapon.wav",
    "missile": "../game_assets/sounds/gameplay/missile.wav",
    "missile_launch": "../game_assets/sounds/gameplay/missile_launch.wav",
    "click": "../game_assets/sounds/ui/click_button.wav",
    "quit_effect": "../game_assets/sounds/ui/quit_effect.wav",
    "keypress": "../game_assets/sounds/ui/keypress.wav",
    "warp": "../game_assets/sounds/gameplay/warp_sound.mp3",
    "alien_exploding": "../game_assets/sounds/gameplay/alien_exploding.wav",
    "boss_exploding": "../game_assets/sounds/gameplay/boss_exploding.wav",
}

LEVEL_SOUNDS = {
    range(1, 8): "../game_assets/sounds/level/battle_one.wav",
    range(9, 16): "../game_assets/sounds/level/battle_two.wav",
    range(17, 24): "../game_assets/sounds/level/battle_three.wav",
    range(25, 27): "../game_assets/sounds/level/battle_four.wav",
}

BOSS_RUSH_MUSIC = {
    range(1, 5): "../game_assets/sounds/boss_rush/first_phase.wav",
    range(6, 9): "../game_assets/sounds/boss_rush/second_phase.wav",
    range(10, 16): "../game_assets/sounds/boss_rush/third_phase.wav",
}

ENDLESS_SOUNDTRACK = {range(1, 3): "../game_assets/sounds/endless/endless.mp3"}

# Dict used to map alien images to game level.
LEVEL_PREFIX = {
    1: "Alien1",
    2: "Alien2",
    3: "Alien3",
    4: "Alien4",
    5: "Alien5",
    6: "Alien6",
    7: "Alien7",
}

# Various game constants.
GAME_CONSTANTS = {
    "ENDLESS_MAX_ALIENS": 50,
    "MAX_ALIEN_NUM": 15,
    "POWER_SPEED": 1.5,
    "SCORE_SCALE": 4,
    "MAX_AS_SPEED": 3.0,
    "MAX_AS_FREQ": 200,
}


DIFFICULTIES = {
    "EASY": 0.2,
    "MEDIUM": 0.4,
    "HARD": 0.6,
    "MAX_EASY": 3.4,
    "MAX_MEDIUM": 3.6,
    "MAX_HARD": 3.8,
}
# used to map each key with the game mode, for saving the high scores
GAME_MODE_SCORE_KEYS = {
    "boss_rush": "boss_rush_scores",
    "endless_onslaught": "endless_scores",
    "meteor_madness": "meteor_madness_scores",
    "slow_burn": "slow_burn_scores",
    "last_bullet": "last_bullet_scores",
    "cosmic_conflict": "cosmic_conflict_scores",
    "one_life_reign": "one_life_reign_scores",
    "normal": "high_scores",
}

SINGLE_PLAYER_FILE = "single_high_score.json"
MULTI_PLAYER_FILE = "high_score.json"
DEFAULT_HIGH_SCORES = {"high_scores": [0] * 10}
RANK_POSITIONS = {1: "1st", 2: "2nd", 3: "3rd"}

# Ships settings
MAX_HP = 5
STARTING_HP = 3

BOSS_LEVELS = [10, 15, 20, 25]


POWER_DOWN_ATTRIBUTES = {
            'reverse': 'last_reverse_power_down_time',
            'disarmed': 'last_disarmed_power_down_time',
            'scaled_weapon': 'last_scaled_weapon_power_down_time'
        }
