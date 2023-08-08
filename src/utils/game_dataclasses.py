"""
The 'game_dataclasses' module contains the UIOptions, GameModes and
ShipStates data classes taht are used in different parts of the game."""


from dataclasses import dataclass


@dataclass
class UIOptions:
    """Represents options for the user interface of the game."""

    paused: bool = False
    show_difficulty: bool = False
    resizable: bool = False
    high_score_saved: bool = False
    show_high_scores: bool = False
    show_game_modes: bool = False
    game_over_sound_played: bool = False
    ship_selection: bool = False


@dataclass
class GameModes:
    """Represents the available game modes for the game"""

    endless_onslaught: bool = False
    slow_burn: bool = False
    meteor_madness: bool = False
    boss_rush: bool = False
    last_bullet: bool = False
    cosmic_conflict: bool = False
    one_life_reign: bool = False
    game_mode: str = "normal"


@dataclass
class ShipStates:
    """A dataclass to manage ship states."""

    alive: bool = True
    exploding: bool = False
    shielded: bool = False
    warping: bool = False
    single_player: bool = False
    immune: bool = False
    empowered: bool = False
    reverse: bool = False
    disarmed: bool = False
    scaled: bool = False
    scaled_weapon: bool = False
    firing: bool = False
