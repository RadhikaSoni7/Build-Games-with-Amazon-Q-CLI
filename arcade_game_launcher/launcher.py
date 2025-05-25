"""
Main launcher UI with game selection menu.
"""
import os
import sys
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_game_launcher.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, BLUE, 
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, TITLE_FONT_SIZE, 
    BUTTON_FONT_SIZE, GAME_TITLE
)
from arcade_game_launcher.utils.button import Button
from arcade_game_launcher.utils.game_loader import GameLoader
from arcade_game_launcher.utils.screen_manager import ScreenManager

class LauncherScreen:
    def __init__(self, screen_manager):
        """
        Initialize the launcher screen.
        
        Args:
            screen_manager: Screen manager instance
        """
        self.screen_manager = screen_manager
        self.game_loader = GameLoader()
        self.games = self.game_loader.discover_games()
        self.buttons = []
        self.title_font = None
        self.button_font = None
        self.quit_button = None
        
        # Initialize UI elements
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI elements like fonts and buttons."""
        # Initialize fonts
        pygame.font.init()
        try:
            font_path = os.path.join("assets", "fonts", "arial.ttf")
            if os.path.exists(font_path):
                self.title_font = pygame.font.Font(font_path, TITLE_FONT_SIZE)
                self.button_font = pygame.font.Font(font_path, BUTTON_FONT_SIZE)
            else:
                self.title_font = pygame.font.SysFont("arial", TITLE_FONT_SIZE)
                self.button_font = pygame.font.SysFont("arial", BUTTON_FONT_SIZE)
        except Exception as e:
            print(f"Error loading fonts: {e}")
            self.title_font = pygame.font.SysFont("arial", TITLE_FONT_SIZE)
            self.button_font = pygame.font.SysFont("arial", BUTTON_FONT_SIZE)
            
        # Create game buttons
        self.create_buttons()
        
    def create_buttons(self):
        """Create buttons for each game."""
        self.buttons = []
        
        # Calculate starting position for buttons
        start_y = SCREEN_HEIGHT // 3
        
        # Create a button for each game
        for i, game_name in enumerate(self.games.keys()):
            x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
            y = start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            
            button = Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, game_name)
            button.set_font(self.button_font)
            self.buttons.append(button)
            
        # Add quit button at the bottom
        quit_y = start_y + len(self.games) * (BUTTON_HEIGHT + BUTTON_MARGIN) + BUTTON_MARGIN
        self.quit_button = Button(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
            quit_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Quit"
        )
        self.quit_button.set_font(self.button_font)
        
    def handle_event(self, event):
        """
        Handle events for the launcher screen.
        
        Args:
            event: Pygame event
            
        Returns:
            str or None: Game name to launch, or None to continue
        """
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check game buttons
            for i, button in enumerate(self.buttons):
                if button.handle_event(event):
                    game_name = list(self.games.keys())[i]
                    return game_name
                    
            # Check quit button
            if self.quit_button and self.quit_button.handle_event(event):
                self.screen_manager.quit()
                return None
                
        return None
        
    def update(self):
        """Update the launcher screen."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button states
        for button in self.buttons:
            button.update(mouse_pos)
            
        if self.quit_button:
            self.quit_button.update(mouse_pos)
            
    def draw(self, screen):
        """
        Draw the launcher screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw background
        screen.fill(BLACK)
        
        # Draw title
        if self.title_font:
            title_surface = self.title_font.render(GAME_TITLE, True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
            screen.blit(title_surface, title_rect)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
            
        # Draw quit button
        if self.quit_button:
            self.quit_button.draw(screen)


class GameRunner:
    def __init__(self):
        """Initialize the game runner."""
        # Initialize Pygame
        pygame.init()
        
        # Create screen manager
        self.screen_manager = ScreenManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen_manager.set_caption(GAME_TITLE)
        self.screen_manager.set_fps(FPS)
        
        # Create launcher screen
        self.launcher_screen = LauncherScreen(self.screen_manager)
        
        # Game loader
        self.game_loader = GameLoader()
        self.game_loader.discover_games()
        
    def run(self):
        """Run the game launcher."""
        # Set the initial screen
        self.screen_manager.set_screen(self.launcher_screen)
        
        # Main loop
        running = True
        while running:
            # Run the current screen
            result = self.screen_manager.run()
            
            if result is None:
                # Quit the launcher
                running = False
            else:
                # Launch the selected game
                print(f"Launching game: {result}")
                pygame.display.set_caption(f"{GAME_TITLE} - {result}")
                
                # Run the game
                self.game_loader.run_game(result, self.screen_manager.screen)
                
                # Return to the launcher
                pygame.display.set_caption(GAME_TITLE)
                self.screen_manager.set_screen(self.launcher_screen)
                
        # Clean up
        pygame.quit()


if __name__ == "__main__":
    runner = GameRunner()
    runner.run()
