"""
Snake game implementation.
"""
import os
import sys
import random
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from arcade_game_launcher.config import BLACK, WHITE, GREEN, RED, FPS

# Snake game constants
GRID_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30
SNAKE_SPEED = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        """Initialize the snake."""
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
    def change_direction(self, direction):
        """
        Change the snake's direction.
        
        Args:
            direction (tuple): New direction as (x, y)
        """
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            
    def check_collision(self):
        """
        Check if the snake has collided with itself.
        
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.body[0] in self.body[1:]
        
    def grow_snake(self):
        """Make the snake grow on the next move."""
        self.grow = True


class Food:
    def __init__(self, snake_body):
        """
        Initialize food at a random position.
        
        Args:
            snake_body (list): List of snake body positions to avoid
        """
        self.position = self.generate_position(snake_body)
        
    def generate_position(self, snake_body):
        """
        Generate a random position for food that's not on the snake.
        
        Args:
            snake_body (list): List of snake body positions to avoid
            
        Returns:
            tuple: (x, y) position for the food
        """
        while True:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if position not in snake_body:
                return position


class SnakeGame:
    def __init__(self, screen, width, height):
        """
        Initialize the snake game.
        
        Args:
            screen: Pygame surface to draw on
            width (int): Screen width
            height (int): Screen height
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.running = True
        self.score = 0
        
        # Calculate cell size
        self.cell_width = width // GRID_WIDTH
        self.cell_height = height // GRID_HEIGHT
        
        # Create snake and food
        self.snake = Snake()
        self.food = Food(self.snake.body)
        
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        """Update game state."""
        # Move snake
        self.snake.move()
        
        # Check for food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.food = Food(self.snake.body)
            self.score += 10
            
        # Check for self collision
        if self.snake.check_collision():
            self.game_over()
            
    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw snake
        for segment in self.snake.body:
            rect = pygame.Rect(
                segment[0] * self.cell_width,
                segment[1] * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.screen, GREEN, rect)
            
        # Draw food
        food_rect = pygame.Rect(
            self.food.position[0] * self.cell_width,
            self.food.position[1] * self.cell_height,
            self.cell_width,
            self.cell_height
        )
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Update display
        pygame.display.flip()
        
    def game_over(self):
        """Handle game over state."""
        game_over_font = pygame.font.SysFont("arial", 48)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
        
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        
        # Wait for a moment before returning to launcher
        pygame.time.wait(2000)
        self.running = False
        
    def run(self):
        """Run the game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(SNAKE_SPEED)


def run_game(screen, width, height):
    """
    Run the snake game.
    
    Args:
        screen: Pygame surface to draw on
        width (int): Screen width
        height (int): Screen height
    """
    game = SnakeGame(screen, width, height)
    game.run()


if __name__ == "__main__":
    # For testing the game standalone
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    run_game(screen, 800, 600)
    pygame.quit()
