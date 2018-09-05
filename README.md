# Math Blaster
A game with an astronaut, spaceships, and numbers.

## Video of Gameplay
![Gameplay](./readme/math-blaster.gif)

## Contents
  * Game Description
  * Technology Used
  * Challenges and Solutions
  * Future Goals
  * Author
  * Credits

## Game Description
### Controls
Use arrow keys to move the hero.

### Gameplay
Catch the UFO with the correct number to score points.
Catch the wrong UFO, you lose a life.
Score points to win the game.

## Technology Used
  * Python 2
  * Pygame

## Challenges and Solutions
This was my first project using pygame, so familiarizing myself with the library was a primary challenge.

  * Challenge #1: Resizable display

  After seeing several games built with pygame, made with a fixed width and height, I knew I wanted my game to be resizable.  This meant every asset had to have a resize function based on the screen size, and called at the proper time.

  * Challenge #2: Generating decoy answers

  The game generates random basic math facts and calculates correct answers as well as three decoys for each problem.  The fact generation was not an issue, the decoys were.  Because they had to be reasonable answers, I tried to have them be one-off errors.  For multiplication, I programmed them to be a random integer between the lower factor and the actual product.  Problem was, if the lower factor was zero, this caused an infinite loop.  The solution was not difficult, but debugging it was because it was a low frequency error.

  * Challenge #3: Timing and displays

  There were certain displays, like when the character loses a life, or scores points, that needed to be shown for a brief period of time.  I wanted to just pause the program to show them, but this was not possible.  Instead, I set a timer and tracked the amount of time passed to control how long to display the text.

  * Challenge #4: Physics

  The basic physics of the main character were actually not a huge challenge.  I simply set the velocity to a value when up, left, or right were pressed in the corresponding direction.  Gravity just changed velocity at a set rate in the down direction.

## Future Goals
  * Display jet pack and running more accurately.  The animation for the jet pack needs to be triggered when it is used only, and the character should not run in mid-air.

  * Convert to a javascript library.  For more users to play, I want to move the game to be web accessible using something like Phaser.

## Author
  Ian Gornall

## Credits
OpenGameArt.org
UI - Buch
Astronaut - MrGecko
Creatures - Stephen Challener (Redshrike)
Spaceships - dravenx
