# Overview

**Project Title**: Target Practice

**Project Description**: The initial goal of this project was to create a Python version of the classic DOOM game through an intensive study of the WAD file format. The emphasis of the project shifted because significant obstacles with WAD file manipulation and a desire to finish a concrete project within a self-imposed deadline required it. Pygame enabled the development of a fully functional Target Practice game which maintains simplicity. Players manipulate a rotating turret to shoot moving targets while music plays in the background to earn a high score.

**Project Goals**:

  * To learn and apply basic game development principles using Pygame.
  * To create a simple, playable game within a reasonable timeframe.
  * To implement core game mechanics: player input for aiming, projectile firing, target movement, collision detection, and score tracking.
  * To gain experience with sound integration in a Python application.

-----

## Instructions for Build and Use

Steps to build and/or run the software:

1.  **Save the code**: Save the provided Python code as a `.py` file (e.g., `target_practice.py`).
2.  **Place the music file**: Download an MP3 music file (e.g., "Evanescence - Bring Me To Life (Official HD Music Video).mp3") and place it in the **same directory** as your Python script.
3.  **Run the game**: Open a terminal or command prompt, navigate to the directory where you saved the file, and run the script using `python target_practice.py`.

Instructions for using the software:

1.  **Aim the turret**: Move your mouse cursor across the screen to rotate the turret. The turret will always point towards your mouse.
2.  **Fire projectiles**:
      * Click the **left mouse button** to fire a projectile.
      * Alternatively, press the **spacebar** to fire a projectile.
3.  **Score points**: Hit the red moving targets with your projectiles to earn points. Your score is displayed in the top-left corner of the screen.
4.  **Enjoy the music**: A background song will play continuously while the game is running.

-----

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

  * **Python**: Version 3.x (tested with Python 3.8+)
  * **Pygame**: Version 2.0.0 or higher. You can install it via pip: `pip install pygame`

-----

## Useful Websites to Learn More

I found these websites useful in developing this software:

  * [Pygame Documentation](https://www.pygame.org/docs/): The official documentation for Pygame, invaluable for learning about its modules and functions.
  * [Youtube Tutorials](https://youtu.be/AY9MnQ4x3zk?si=UlcXt-nOc0iwDDPV): A great YouTube video with comprehensive Pygame tutorial for beginners.
  

-----

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

  * [ ] **Difficulty scaling**: Implement a system where target speed or spawn rate increases over time to make the game more challenging.
  * [ ] **Sound effects**: Add sound effects for projectile firing, target hits, and potentially a game over sound.
  * [ ] **Game states**: Introduce a start screen, game over screen, and pause functionality.
  * [ ] **Different target types**: Create various types of targets with different sizes, speeds, or point values.
  * [ ] **High score system**: Save the highest score achieved locally.
  * [ ] **Visual enhancements**: Add particle effects for hits, a more detailed turret sprite, or background elements.
  * [ ] **Power-ups**: Implement temporary power-ups for the player (e.g., faster projectiles, multi-shot).