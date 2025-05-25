"""
Flappy Bird game implementation.
"""
import os
import sys
import random
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from arcade_game_launcher.config import BLACK, WHITE, GREEN, BLUE, RED, YELLOW, FPS

# Game constants
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
GROUND_HEIGHT = 100

class Bird:
    def __init__(self, x, y):
        """
        Initialize the bird.
        
        Args:
            x (int): X-coordinate of the bird
            y (int): Y-coordinate of the bird
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.velocity = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def jump(self):
        """Make the bird jump."""
        self.velocity = BIRD_JUMP
        
    def update(self):
        """Update the bird's position."""
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update rectangle position
        self.rect.y = int(self.y)
        
    def draw(self, screen):
        """
        Draw the bird.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, YELLOW, self.rect)
        
        # Draw eye
        eye_x = self.rect.x + self.rect.width - 10
        eye_y = self.rect.y + 10
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 5)


class Pipe:
    def __init__(self, x, height, screen_height, is_top=False):
        """
        Initialize a pipe.
        
        Args:
            x (int): X-coordinate of the pipe
            height (int): Height of the pipe
            screen_height (int): Height of the screen
            is_top (bool): Whether this is a top pipe
        """
        self.width = 60
        self.height = height
        self.x = x
        
        if is_top:
            self.y = 0
        else:
            self.y = screen_height - height - GROUND_HEIGHT
            
        self.rect = pygame.Rect(x, self.y, self.width, self.height)
        self.passed = False
        
    def update(self):
        """Update the pipe's position."""
        self.x -= PIPE_SPEED
        self.rect.x = self.x
        
    def draw(self, screen):
        """
        Draw the pipe.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, GREEN, self.rect)


class FlappyBirdGame:
    def __init__(self, screen, width, height):
        """
        Initialize the Flappy Bird game.
        
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
        self.game_over_state = False
        
        # Create bird
        self.bird = Bird(width // 4, height // 2)
        
        # Create pipes
        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()
        
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over_state:
                        self.bird.jump()
                    else:
                        # Restart game
                        self.__init__(self.screen, self.width, self.height)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
        # Also allow mouse clicks for jumping
        if pygame.mouse.get_pressed()[0] and not self.game_over_state:
            self.bird.jump()
            
    def update(self):
        """Update game state."""
        if self.game_over_state:
            return
            
        # Update bird
        self.bird.update()
        
        # Generate new pipes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_FREQUENCY:
            # Generate random gap position
            gap_y = random.randint(100, self.height - GROUND_HEIGHT - PIPE_GAP - 100)
            
            # Create top pipe
            top_height = gap_y
            top_pipe = Pipe(self.width, top_height, self.height, is_top=True)
            
            # Create bottom pipe
            bottom_height = self.height - gap_y - PIPE_GAP - GROUND_HEIGHT
            bottom_pipe = Pipe(self.width, bottom_height, self.height, is_top=False)
            
            # Add pipes to list
            self.pipes.append(top_pipe)
            self.pipes.append(bottom_pipe)
            
            # Update last pipe time
            self.last_pipe_time = current_time
            
        # Update pipes and check for score
        for pipe in self.pipes:
            pipe.update()
            
            # Check if bird has passed the pipe
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                # Only count score once per pipe pair
                if pipe.y == 0:  # Only count top pipes
                    self.score += 1
                    
        # Remove pipes that are off screen
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]
        
        # Check for collisions
        self.check_collisions()
        
    def check_collisions(self):
        """Check for collisions with pipes and boundaries."""
        # Check for collision with ground
        if self.bird.y + self.bird.height > self.height - GROUND_HEIGHT:
            self.game_over()
            return
            
        # Check for collision with ceiling
        if self.bird.y < 0:
            self.game_over()
            return
            
        # Check for collision with pipes
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over()
                return
                
    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BLUE)
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Draw ground
        ground_rect = pygame.Rect(0, self.height - GROUND_HEIGHT, self.width, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, (139, 69, 19), ground_rect)  # Brown color
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over text if game is over
        if self.game_over_state:
            game_over_font = pygame.font.SysFont("arial", 48)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        # Update display
        pygame.display.flip()
        
    def game_over(self):
        """Handle game over state."""
        self.game_over_state = True
        
    def run(self):
        """Run the game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


def run_game(screen, width, height):
    """
    Run the Flappy Bird game.
    
    Args:
        screen: Pygame surface to draw on
        width (int): Screen width
        height (int): Screen height
    """
    game = FlappyBirdGame(screen, width, height)
    game.run()


if __name__ == "__main__":
    # For testing the game standalone
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Flappy Bird")
    run_game(screen, 800, 600)
    pygame.quit()
