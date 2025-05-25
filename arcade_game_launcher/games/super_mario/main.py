"""
Super Mario game implementation.
"""
import os
import sys
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from arcade_game_launcher.config import BLACK, WHITE, RED, BLUE, GREEN, FPS

# Game constants
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
PLATFORM_SPEED = 3

class Player:
    def __init__(self, x, y):
        """
        Initialize the player.
        
        Args:
            x (int): X-coordinate of the player
            y (int): Y-coordinate of the player
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.facing_right = True
        
    def jump(self):
        """Make the player jump if not already jumping."""
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            
    def move_left(self):
        """Move the player left."""
        self.velocity_x = -PLAYER_SPEED
        self.facing_right = False
        
    def move_right(self):
        """Move the player right."""
        self.velocity_x = PLAYER_SPEED
        self.facing_right = True
        
    def stop(self):
        """Stop the player's horizontal movement."""
        self.velocity_x = 0
        
    def update(self, platforms):
        """
        Update the player's position and check for collisions.
        
        Args:
            platforms (list): List of platform objects to check for collisions
        """
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Update rectangle position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Check for platform collisions
        self.is_jumping = True
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Check if landing on top of platform
                if self.velocity_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.velocity_y = 0
                    self.is_jumping = False
                    
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
        if self.rect.right > 800:  # Assuming screen width is 800
            self.rect.right = 800
            self.x = self.rect.x - self.width
            
    def draw(self, screen):
        """
        Draw the player.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw player body
        pygame.draw.rect(screen, RED, self.rect)
        
        # Draw face details based on direction
        if self.facing_right:
            # Draw eye
            eye_x = self.rect.x + self.rect.width - 15
            eye_y = self.rect.y + 15
            pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 8)
            pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 4)
        else:
            # Draw eye
            eye_x = self.rect.x + 15
            eye_y = self.rect.y + 15
            pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 8)
            pygame.draw.circle(screen, BLACK, (eye_x - 2, eye_y), 4)


class Platform:
    def __init__(self, x, y, width, height, moving=False, move_range=0):
        """
        Initialize a platform.
        
        Args:
            x (int): X-coordinate of the platform
            y (int): Y-coordinate of the platform
            width (int): Width of the platform
            height (int): Height of the platform
            moving (bool): Whether the platform moves
            move_range (int): Range of movement for moving platforms
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.moving = moving
        self.move_range = move_range
        self.start_x = x
        self.direction = 1  # 1 for right, -1 for left
        self.speed = PLATFORM_SPEED
        
    def update(self):
        """Update the platform's position if it's moving."""
        if self.moving:
            self.x += self.speed * self.direction
            
            # Change direction if reached movement range
            if self.x > self.start_x + self.move_range:
                self.direction = -1
            elif self.x < self.start_x:
                self.direction = 1
                
            # Update rectangle position
            self.rect.x = int(self.x)
            
    def draw(self, screen):
        """
        Draw the platform.
        
        Args:
            screen: Pygame surface to draw on
        """
        color = GREEN if self.moving else (139, 69, 19)  # Brown for static platforms
        pygame.draw.rect(screen, color, self.rect)


class Coin:
    def __init__(self, x, y):
        """
        Initialize a coin.
        
        Args:
            x (int): X-coordinate of the coin
            y (int): Y-coordinate of the coin
        """
        self.x = x
        self.y = y
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.collected = False
        
    def draw(self, screen):
        """
        Draw the coin if not collected.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.collected:
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), self.radius)  # Gold color


class SuperMarioGame:
    def __init__(self, screen, width, height):
        """
        Initialize the Super Mario game.
        
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
        
        # Create player
        self.player = Player(100, height - 200)
        
        # Create platforms
        self.platforms = [
            # Ground
            Platform(0, height - 50, width, 50),
            
            # Platforms
            Platform(100, height - 150, 200, 20),
            Platform(400, height - 200, 150, 20),
            Platform(600, height - 300, 200, 20),
            Platform(200, height - 300, 100, 20, moving=True, move_range=200),
            Platform(0, height - 400, 100, 20),
            Platform(700, height - 400, 100, 20)
        ]
        
        # Create coins
        self.coins = [
            Coin(150, height - 180),
            Coin(450, height - 230),
            Coin(650, height - 330),
            Coin(250, height - 330),
            Coin(50, height - 430),
            Coin(750, height - 430)
        ]
        
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()
            
    def update(self):
        """Update game state."""
        if self.game_over_state:
            return
            
        # Update player
        self.player.update(self.platforms)
        
        # Update platforms
        for platform in self.platforms:
            platform.update()
            
        # Check for coin collection
        for coin in self.coins:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 10
                
        # Check if all coins are collected
        if all(coin.collected for coin in self.coins):
            self.victory()
            
        # Check if player fell off the screen
        if self.player.y > self.height:
            self.game_over()
            
    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BLUE)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over or victory text if applicable
        if self.game_over_state:
            game_over_font = pygame.font.SysFont("arial", 48)
            if all(coin.collected for coin in self.coins):
                game_over_text = game_over_font.render("VICTORY!", True, (255, 215, 0))  # Gold color
            else:
                game_over_text = game_over_font.render("GAME OVER", True, RED)
                
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press ESC to return to launcher", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        # Update display
        pygame.display.flip()
        
    def game_over(self):
        """Handle game over state."""
        self.game_over_state = True
        
    def victory(self):
        """Handle victory state."""
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
    Run the Super Mario game.
    
    Args:
        screen: Pygame surface to draw on
        width (int): Screen width
        height (int): Screen height
    """
    game = SuperMarioGame(screen, width, height)
    game.run()


if __name__ == "__main__":
    # For testing the game standalone
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Mario")
    run_game(screen, 800, 600)
    pygame.quit()
