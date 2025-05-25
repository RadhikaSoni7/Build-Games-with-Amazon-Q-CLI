"""
Game loader for dynamically loading and switching between games.
"""
import os
import importlib.util
import pygame
from arcade_game_launcher.config import SCREEN_WIDTH, SCREEN_HEIGHT

class GameLoader:
    def __init__(self, games_dir="games"):
        """
        Initialize the game loader.
        
        Args:
            games_dir (str): Directory containing game modules
        """
        self.games_dir = games_dir
        self.games = {}
        self.current_game = None
        
    def discover_games(self):
        """
        Discover available games in the games directory.
        
        Returns:
            dict: Dictionary of game names and their paths
        """
        games = {}
        
        # Check if the games directory exists
        if not os.path.exists(self.games_dir):
            print(f"Games directory '{self.games_dir}' not found.")
            return games
            
        # Look for game modules (directories with main.py)
        for item in os.listdir(self.games_dir):
            game_dir = os.path.join(self.games_dir, item)
            main_file = os.path.join(game_dir, "main.py")
            
            if os.path.isdir(game_dir) and os.path.exists(main_file):
                # Format the game name for display (replace underscores with spaces and capitalize)
                display_name = " ".join(word.capitalize() for word in item.split("_"))
                games[display_name] = {
                    "name": item,
                    "path": game_dir,
                    "main_file": main_file
                }
                
        self.games = games
        return games
        
    def load_game(self, game_name):
        """
        Load a game module by name.
        
        Args:
            game_name (str): Name of the game to load
            
        Returns:
            module or None: Loaded game module or None if loading failed
        """
        try:
            # Find the game info
            game_info = None
            for display_name, info in self.games.items():
                if display_name == game_name or info["name"] == game_name:
                    game_info = info
                    break
                    
            if not game_info:
                print(f"Game '{game_name}' not found.")
                return None
                
            # Load the module
            module_name = f"arcade_game_launcher.games.{game_info['name']}.main"
            spec = importlib.util.spec_from_file_location(module_name, game_info["main_file"])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            return module
            
        except Exception as e:
            print(f"Error loading game '{game_name}': {e}")
            return None
            
    def run_game(self, game_name, screen):
        """
        Run a game by name.
        
        Args:
            game_name (str): Name of the game to run
            screen: Pygame surface to draw on
            
        Returns:
            bool: True if the game ran successfully, False otherwise
        """
        try:
            # Load the game module
            module = self.load_game(game_name)
            if not module:
                return False
                
            # Run the game
            self.current_game = module
            if hasattr(module, "run_game"):
                module.run_game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                return True
            else:
                print(f"Game '{game_name}' does not have a run_game function.")
                return False
                
        except Exception as e:
            print(f"Error running game '{game_name}': {e}")
            return False
