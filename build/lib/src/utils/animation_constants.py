"""
The 'animation_constants' module contains constants used
for different animations in the game.

The constants include the following:
- 'destroy_frames': a list of frames used for destruction animations.
- 'ship_images': a list of images used for ship sprites.
- 'warp_frames': a list of frames used for warp animations.
- 'shield_frames': a list of frames used for shield animations.
- 'immune_frames': a list of frames used for immune animations.
- 'explosion_frames': a list of frames used for explosion animations.
- 'asteroid_frames': a list of frames used for asteroid sprites.
- 'empower_frames': a list of frames used for empower animations.
"""

from src.utils.game_utils import load_frames

destroy_frames = load_frames("destroyed/destroyed-0{}.png", 15, start=1)

ship_images = load_frames("ships/ship{}.png", 6, start=1)

warp_frames = load_frames("warp/warp_{}.png", 9)

shield_frames = load_frames("shield/shield-0{}.png", 11)

immune_frames = load_frames("immune/immune-0{}.png", 11, start=1)

explosion_frames = load_frames("explosion/explosion1_{:04d}.png", 89, start=2)

asteroid_frames = load_frames("asteroid/Asteroid-A-09-{:03d}.png", 120)

empower_frames = load_frames("empower/empower-0{}.png", 6, start=1)

missile_frames = load_frames("projectiles/missiles/missile-0{}.png", 9, start=1)

missile_ex_frames = load_frames("missile_explosion/missile_ex-0{}.png", 9, start=1)

alien_immune_frames = load_frames("alien_immune/immune-0{}.png", 20, start=1)

laser_frames = load_frames("projectiles/laser/laser-0{}.png", 9, start=1)
