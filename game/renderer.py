"""
Rendering and display for the game state.
"""

from typing import List
from .grid import Maze, Pos
from .config import GameConfig


class Renderer:
    """Handles rendering the game state to the terminal."""
    
    def __init__(self, maze: Maze):
        """
        Initialize renderer with a maze.
        
        Args:
            maze: The Maze object to render
        """
        self.maze = maze
        self.config = GameConfig()
    
    def render_game_state(self, player_pos: Pos, monster_pos: Pos, 
                         exit_pos: Pos, monster_type: str = "BFS") -> str:
        """
        Render the current game state with all entities.
        
        Args:
            player_pos: Player position
            monster_pos: Monster position
            exit_pos: Exit position
            monster_type: "BFS" or "DFS" for monster character selection
            
        Returns:
            String representation of the game state
        """
        rows, cols = self.maze.rows, self.maze.cols
        
        # Create blank canvas
        canvas = [[' ' for _ in range(cols)] for _ in range(rows)]
        
        # First pass: draw the maze structure
        for r in range(rows):
            for c in range(cols):
                cell = self.maze.get_cell((r, c))
                if cell == '#':
                    canvas[r][c] = self.config.WALL_CHAR
                else:
                    canvas[r][c] = self.config.FLOOR_CHAR
        
        # Place entities (later ones appear on top)
        self._place_entity(canvas, exit_pos, self.config.EXIT_CHAR)
        self._place_entity(canvas, monster_pos, self._get_monster_char(monster_type))
        self._place_entity(canvas, player_pos, self.config.PLAYER_CHAR)
        
        # Convert to string
        result = []
        for row in canvas:
            result.append(''.join(row))
        
        return '\n'.join(result)
    
    def _get_monster_char(self, monster_type: str) -> str:
        """Get the appropriate monster character."""
        return self.config.BFS_MONSTER_CHAR if monster_type == "BFS" else self.config.DFS_MONSTER_CHAR
    
    def _place_entity(self, canvas: List[List[str]], pos: Pos, char: str):
        """Place an entity on the canvas."""
        r, c = pos
        if 0 <= r < len(canvas) and 0 <= c < len(canvas[0]):
            canvas[r][c] = char