# Arcade Game Launcher

A modular arcade game launcher built with Python and Pygame. This launcher allows you to play multiple games from a single interface and easily add new games.

## Features

- Clean and intuitive game selection menu
- Multiple games included (Snake, Flappy Bird, Super Mario)
- Modular architecture for easy addition of new games
- Shared configuration and utility classes

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Launcher

To start the game launcher, run:

```bash
python launcher.py
```

## Game Controls

### Snake
- Arrow keys to control the snake's direction

### Flappy Bird
- Space or mouse click to make the bird jump
- ESC to return to the launcher

### Super Mario
- Left/Right arrow keys to move
- Space or Up arrow to jump
- ESC to return to the launcher

## Adding New Games

To add a new game to the launcher:

1. Create a new directory in the `games` folder with your game name
2. Implement a `main.py` file with a `run_game(screen, width, height)` function
3. Add any game-specific assets to subdirectories (sprites, sounds, etc.)
4. The game will automatically appear in the launcher menu

## Project Structure

```
arcade_game_launcher/
│
├── launcher.py                # Main launcher UI with game selection menu
├── config.py                  # Shared settings (screen size, colors, FPS)
├── assets/                    # Common assets: fonts, icons, sounds
│   ├── fonts/
│   ├── icons/
│   └── sounds/
│
├── games/                     # Each game is a separate module here
│   ├── super_mario/
│   │   ├── main.py            # Super Mario main game loop
│   │   ├── levels/            # Level data (JSON or text)
│   │   ├── sprites/           # Mario player and enemy sprites
│   │   └── sounds/            # Game-specific sounds
│   │
│   ├── flappy_bird/
│   │   ├── main.py
│   │   ├── sprites/
│   │   └── sounds/
│   │
│   └── snake/
│       ├── main.py
│       ├── sprites/
│       └── sounds/
│
├── utils/
│   ├── button.py              # UI button class
│   ├── game_loader.py         # Dynamic game loading and switching
│   └── screen_manager.py      # Handles screen and state management
│
├── README.md
└── requirements.txt           # Pygame and dependencies
```

## License

This project is open source and available under the MIT License.
