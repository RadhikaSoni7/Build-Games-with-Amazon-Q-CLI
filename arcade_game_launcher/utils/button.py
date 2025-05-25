"""
Button class for UI elements in the game launcher.
"""
import pygame
from arcade_game_launcher.config import WHITE, BLACK, LIGHT_GRAY, DARK_GRAY

class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        """
        Initialize a button with position, size, and text.
        
        Args:
            x (int): X-coordinate of the button's top-left corner
            y (int): Y-coordinate of the button's top-left corner
            width (int): Width of the button
            height (int): Height of the button
            text (str): Text to display on the button
            font_size (int): Font size for the button text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font = None
        self.is_hovered = False
        self.is_clicked = False
        
        # Colors
        self.bg_color = LIGHT_GRAY
        self.hover_color = WHITE
        self.text_color = BLACK
        self.border_color = DARK_GRAY
        
    def set_font(self, font):
        """Set the font for the button text."""
        self.font = font
        
    def draw(self, screen):
        """
        Draw the button on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw button background
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # Draw text if font is available
        if self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
            
    def update(self, mouse_pos):
        """
        Update button state based on mouse position.
        
        Args:
            mouse_pos (tuple): Current mouse position (x, y)
            
        Returns:
            bool: True if button is hovered, False otherwise
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def handle_event(self, event):
        """
        Handle mouse events for the button.
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_clicked = True
                return True
        return False
