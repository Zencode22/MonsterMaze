"""
Player and Monster entities for Monster Maze.
"""

from typing import Optional
from .grid import Maze, Pos


class Player:
    """Player character that navigates the maze."""
    
    def __init__(self, start_pos: Pos):
        """
        Initialize player at starting position.
        
        Args:
            start_pos: Initial (row, col) position
        """
        self.position = start_pos
        self.start_pos = start_pos
        self.moves_made = 0
        self.alive = True
        self.escaped = False
    
    def move(self, new_pos: Pos) -> bool:
        """
        Move player to new position.
        
        Args:
            new_pos: Target position
            
        Returns:
            True if move was successful
        """
        self.position = new_pos
        self.moves_made += 1
        return True
    
    def get_distance_to(self, target: Pos) -> int:
        """Calculate Manhattan distance to target."""
        return abs(self.position[0] - target[0]) + abs(self.position[1] - target[1])
    
    def reset(self):
        """Reset player to starting position."""
        self.position = self.start_pos
        self.moves_made = 0
        self.alive = True
        self.escaped = False


class Monster:
    """Monster that chases the player using pathfinding algorithms."""
    
    def __init__(self, start_pos: Pos, ai_type: str = "BFS"):
        """
        Initialize monster.
        
        Args:
            start_pos: Initial position
            ai_type: "BFS" for smart monster, "DFS" for wandering monster
        """
        self.position = start_pos
        self.start_pos = start_pos
        self.ai_type = ai_type  # "BFS" or "DFS"
        self.total_nodes_explored = 0
        
        if ai_type == "BFS":
            self.char = 'B'
            self.name = "Baba Yaga"
            self.origin = "Slavic folklore"
            self.description = "A cunning witch who flies through the forest in a mortar, wielding a pestle. She always knows the shortest path to her prey."
            self.difficulty = "HARD"
        else:
            self.char = 'D'
            self.name = "Draugr"
            self.origin = "Norse mythology"
            self.description = "An undead warrior who wanders the burial mounds, seeking intruders with relentless but meandering determination."
            self.difficulty = "EASY"
    
    def chase(self, pathfinder, player_pos: Pos) -> Optional[Pos]:
        """
        Move monster one step toward player using AI pathfinding.
        
        Args:
            pathfinder: PathFinder instance for the maze
            player_pos: Current player position
            
        Returns:
            New monster position, or None if no valid path
        """
        if self.ai_type == "BFS":
            # BFS: Always recalculate shortest path to player
            path, nodes = pathfinder.find_path(self.position, player_pos, self.ai_type)
            self.total_nodes_explored += nodes
            
            if path and len(path) > 1:
                self.position = path[1]  # Move one step along path
                return self.position
        else:
            # DFS: Recalculate path each turn based on player's new position
            path, nodes = pathfinder.find_path(self.position, player_pos, self.ai_type)
            self.total_nodes_explored += nodes
            
            if path and len(path) > 1:
                self.position = path[1]  # Move one step along path
                return self.position
        
        return None
    
    def get_distance_to(self, target: Pos) -> int:
        """Calculate Manhattan distance to target."""
        return abs(self.position[0] - target[0]) + abs(self.position[1] - target[1])
    
    def reset(self):
        """Reset monster to starting position."""
        self.position = self.start_pos
        self.total_nodes_explored = 0
        self.current_path = None