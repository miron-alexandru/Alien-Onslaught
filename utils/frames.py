"""This module contains constants used in the game, such as images and animations.

The constants include the following:
- `destroy_frames`: a list of frames used for destruction animations.
- `ship_images`: a list of images used for ship sprites.
- `warp_frames`: a list of frames used for warp animations.
- `shield_frames`: a list of frames used for shield animations.
- `immune_frames`: a list of frames used for immune animations.
- `explosion_frames`: a list of frames used for explosion animations.
- `frames`: a list of frames used for asteroid sprites.
- `empower_frames`: a list of frames used for empower animations.

All frames are loaded using the `load_frames` function from the `game_utils` module.
"""


from .game_utils import load_frames

destroy_frames = []
load_frames('destroyed/destroyed-0{}.png', 15, destroy_frames, start=1)

ship_images = []
load_frames('ships/ship{}.png', 6, ship_images, start=1)

warp_frames = []
load_frames('warp/warp_{}.png', 9, warp_frames)

shield_frames = []
load_frames('shield/shield-0{}.png', 11, shield_frames)

immune_frames = []
load_frames('immune/immune-0{}.png', 11, immune_frames, start=1)

explosion_frames = []
load_frames('explosionn/explosion1_{:04d}.png', 89, explosion_frames, start=2)

frames = [] # asteroid frames
load_frames('asteroid/Asteroid-A-09-{:03d}.png', 120, frames)

empower_frames = []
load_frames('empower/empower-0{}.png', 6, empower_frames, start=1)

missile_frames = []
load_frames('projectiles/missiles/missile-0{}.png', 9, missile_frames, start=1)

missile_ex_frames = []
load_frames('missile_explosion/missile_ex-0{}.png', 9, missile_ex_frames, start=1)

alien_immune_frames = []
load_frames('alien_immune/immune-0{}.png', 20, alien_immune_frames, start=1)

