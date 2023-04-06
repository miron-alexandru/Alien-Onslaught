## Alien-Onslaught description:
- Alien-Onslaught is an action-packed game that will test your shooting skills and reflexes. The game is set in outer space, where you must shoot fleets of aliens to reach higher levels and increase your high score. With each level, the game becomes more challenging as the aliens become stronger and faster, and more asteroids rain down from above.

- The game offers a range of game modes, including single-player and multiplayer modes, where you can choose to battle it out with friends or take on the aliens alone. In game you can also get a variety of ship power-ups, including increased speed, bullet speed, and bullets allowed, as well as shields that protect you from enemy fire. It also includes a high score system where players can compete with others for the top spot on the leaderboard, Boss Fights, and more other features.


## Alien-Onslaught Changelog

### Version 1.7:
* Added the option to choose Singleplayer or Multiplayer mode from the Start Menu.
* Implemented new backgrounds that change as the game progresses.
* Made the game window resizable.

### Version 1.8:
* Increased the strength of aliens as the player progresses to higher levels.
* Added ship power-ups, including increased ship speed, bullet speed, and bullets allowed.

### Version 1.9:
* Added random alien shooting and a new power-up, the shield.

### Version 2.0:
* Added animated asteroids dropping from the top of the screen as the game progresses.
* Implemented new ship skins and the ability to switch between them.
* Introduced new animated aliens.

### Version 2.1:
* Added new animations for ship hitting an alien, asteroid, or alien bullet.
* Added a new power-up that increases the number of bullets the player can shoot.
* Added new background images.

### Version 2.2:
* Improved the Start Menu with button images instead of text for Singleplayer, Multiplayer, Play, and Quit buttons.
* Displayed controls for both players on the screen.
* Added Game Over screen when the game ends.

### Version 2.2.1:
* Added new buttons: "Menu" and "Difficulty".
* Players can now adjust the game's difficulty.
* Fixed a bug in ship movement by using Python's "match case" instead of "if-elif-else".
* Added the ability to pause the game.

### Version 2.3:
* Improved the game's user interface.
* Fixed a bug that occurred when the game window was resized.
* Added a ship warp animation when the game starts.
* Implemented boss fights: different bosses with different types of bullets.
* Improved code readability and added more documentation, comments, and docstrings.

### Version 2.4:
* Changed the alien movement so that they randomly move in different directions.
* Improved the code to make it more concise, refactored, and easier to read, and added more documentation.
* Implemented high scores; when the game ends, the high score is saved, and players can view the top 10 high scores by clicking the "HIGH SCORES" button.
* Changed fleet creation so that aliens drop in rows from the top of the screen, and the number of aliens in each row increases with each level.
* Added minimum and maximum window sizes: 1260x700 and 1920x1080.

### Version 2.5:
* Implemented Game Modes:
* The Endless game mode features fleets of aliens and asteroids that continuously appear, with the speed of the aliens and their bullets increasing over time.
* Last Stand: In the Last Stand game mode, the ship and bullet speeds decrease over time, making the game more difficult.
* Refactored code by grouping related functions and classes into new modules for improved organization.
* Created new modules: "game_utils" for common utility functions, "screen_manager" for managing screen resizing behavior, "game_buttons" for creating the game buttons, "animations" for animating elements on the screen, and "constants" for storing constants.

### Version 2.6:
* Refactored code into new classes and modules
* Improvements to the code organization by grouping related modules and classes into new packages.
* New packages created:
* "animations": This package contains modules for handling animations in the game.
* "entities": This package includes modules for defining and managing game entities such as ships, asteroids, aliens, and power-ups.
* "game logic": This package contains modules that handle the core game logic, such as collision detection, game settings, and scoring.
* "ui": This package includes modules for managing the user interface (UI) of the game. It contains classes and functions for creating game buttons, scoreboards, and other UI elements.
* "utils": This package contains modules for various utilities and helper functions used throughout the game and constants.
* Implemented a new game mode, Meteor Madness:  Players must navigate a barrage of asteroids as each level progresses, the number of asteroids coming towards the player will increase, and their speed will become more relentless. Additionally,
the player's speed will decrease, adding an extra layer of challenge to the game.
* New feature to enhance gameplay: player immunity after being hit! Now, when a player is hit, they will be granted a brief period of immunity to prevent them from taking another hit right away. This will give players a chance to recover and avoid getting hit again immediately after respawning. An animation will play during the immunity period, letting the players know they are invulnerable.
* Implemented new animation for entities getting destroyed, and a new module 'frames' which contains constants for animations or images used in the game.
* Implemented a new Boss fight and a new animation for power-ups being picked up.

### Version 2.7:
* Created a new module, 'image_loader' which has functions to load images for aliens.
* Implemented a new game mode, Boss Rush: Players must fight different bosses at every level, each with their own unique designs and bullet patterns. With each level, the bosses become stronger and faster, making them more challenging.
* Improved the high score system, now there are separate high scores for every game mode.
* Improved UI, moved some buttons and added the game title in the Menu screen.
* Refactored code in multiple modules and created two new @dataclasses to hold values for different parts of the game.
* Created a new module 'game_modes' that manages the different game modes available in the game.
* Implemented new power_ups, alien speed and alien bullet speed decreased.
* New power up that is available only in the Last Bullet game mode, remaining bullets increased.
* Implemented a new feature to the game which introduces a new weapon for players. Each player now starts with three missiles that can cause damage to multiple aliens when they explode. Additionally, a power-up has been included which increases the number of missiles available to the player.
* Moved all projectiles into a new module called 'projectiles' and refactored the code in the 'collision_detection' module.
* Now when a player picks up a power, there is a chance for that power to be a penalty. Introduced two penalties: Reversed movement and disarm. The penalties are active for a short period of time.
* New background after level 25.
* Solved a bug that prevented the ships from playing their destroy animation when losing their last health.

### Version 2.8:
* Implemented a new feature: Gift boxes now drop from the top of the screen, each containing different weapon for players to use.
* Implemented two new powers, bonus points and invincibility.
* Code refactored
* Improved UI by adding a description for every game mode available in the game
