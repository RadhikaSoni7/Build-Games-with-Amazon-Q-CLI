"""
Screen manager for handling different screens and states in the game launcher.
"""
import pygame
from arcade_game_launcher.config import BLACK

class ScreenManager:
    def __init__(self, width, height):
        """
        Initialize the screen manager.
        
        Args:
            width (int): Screen width
            height (int): Screen height
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.running = True
        self.fps = 60
        
    def set_caption(self, caption):
        """Set the window caption."""
        pygame.display.set_caption(caption)
        
    def set_fps(self, fps):
        """Set the frames per second."""
        self.fps = fps
        
    def set_screen(self, screen):
        """
        Set the current screen to display.
        
        Args:
            screen: Screen object to display
        """
        self.current_screen = screen
        
    def clear_screen(self, color=BLACK):
        """
        Clear the screen with the specified color.
        
        Args:
            color (tuple): RGB color tuple
        """
        self.screen.fill(color)
        
    def update(self):
        """Update the display."""
        pygame.display.flip()
        self.clock.tick(self.fps)
        
    def quit(self):
        """Quit the screen manager."""
        self.running = False
        
    def run(self):
        """
        Main loop for the screen manager.
        
        Returns:
            str or None: The next screen to switch to, or None to quit
        """
        if not self.current_screen:
            return None
            
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                    
                # Let the current screen handle the event
                result = self.current_screen.handle_event(event)
                if result:
                    return result
            
            # Update and draw the current screen
            self.current_screen.update()
            self.clear_screen()
            self.current_screen.draw(self.screen)
            self.update()
            
        return None
