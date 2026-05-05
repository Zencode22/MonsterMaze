"""
Display utilities for terminal output.
"""

import os

from game.config import GameConfig


class DisplayManager:
    """Manages terminal display operations."""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_banner():
        """Print the game banner."""
        print(GameConfig.get_banner())
    
    @staticmethod
    def print_separator(char: str = "=", width: int = 60):
        """Print a separator line."""
        print(char * width)
    
    @staticmethod
    def print_game_header(turns: int, moves: int):
        """Print game status header."""
        print(f"\nTurn {turns + 1} | Moves: {moves}")
        print("-" * 40)
    
    @staticmethod
    def print_game_footer(monster_distance: int, exit_distance: int):
        """Print game status footer."""
        print("-" * 40)
        print(f"Monster: {monster_distance} steps away | Exit: {exit_distance} steps away")
    
    @staticmethod
    def print_controls():
        """Print game controls - WSAD only."""
        print("\nCONTROLS:")
        print("  W - Move Up")
        print("  A - Move Left")
        print("  S - Move Down")
        print("  D - Move Right")
        print("  Q - Quit game")
    
    @staticmethod
    def print_legend(monster_type: str):
        """Print game legend."""
        monster_char = 'B' if monster_type == 'BFS' else 'D'
        print("\nLEGEND:")
        print(f"  P = You (Player)")
        print(f"  {monster_char} = Monster ({monster_type})")
        print("  E = Exit")
        print("  # = Wall")
        print("  . = Floor")
    
    @staticmethod
    def get_rating(moves: int) -> str:
        """Get performance rating based on moves made."""
        if moves <= GameConfig.LEGENDARY_THRESHOLD:
            return "*** LEGENDARY!"
        elif moves <= GameConfig.GREAT_THRESHOLD:
            return "** GREAT!"
        elif moves <= GameConfig.GOOD_THRESHOLD:
            return "* GOOD"
        else:
            return "SURVIVOR"