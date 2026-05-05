"""
Pathfinding algorithms: BFS and DFS implementations.
"""

from collections import deque
from typing import Dict, List, Optional, Set, Tuple, Union
from .grid import Maze, Pos


class PathFinder:
    """Handles pathfinding operations using BFS and DFS algorithms."""
    
    def __init__(self, maze: Maze):
        """
        Initialize pathfinder with a maze.
        
        Args:
            maze: The Maze object to navigate
        """
        self.maze = maze
    
    def reconstruct_path(self, parent: Dict[Pos, Union[Pos, None]], 
                        start: Pos, goal: Pos) -> Optional[List[Pos]]:
        """
        Reconstruct path from start to goal using parent pointers.
        
        Args:
            parent: Dictionary mapping each position to its parent
            start: Starting position
            goal: Goal position
            
        Returns:
            List of positions from start to goal, or None if unreachable
        """
        if goal not in parent and goal != start:
            return None
        
        path = []
        current = goal
        
        while current != start:
            path.append(current)
            if current not in parent:
                return None
            current = parent[current]
            if current is None:
                return None
        
        path.append(start)
        return list(reversed(path))
    
    def bfs_find_path(self, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos], int]:
        """
        Breadth-First Search - finds shortest path.
        
        Uses a queue (collections.deque) for FIFO processing.
        Marks nodes as visited when enqueued, not when popped.
        
        Args:
            start: Starting position
            goal: Target position
            
        Returns:
            Tuple of (path, visited_set, nodes_explored_count)
        """
        if start == goal:
            return [start], {start}, 1
        
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        nodes_explored = 0
        
        while queue:
            current = queue.popleft()
            nodes_explored += 1
            
            if current == goal:
                path = self.reconstruct_path(parent, start, goal)
                return path, visited, nodes_explored
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return None, visited, nodes_explored
    
    def dfs_find_path(self, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos], int]:
        """
        Depth-First Search - iterative implementation.
        
        Uses a stack (Python list) for LIFO processing.
        Marks nodes as visited when pushed, not when popped.
        
        Args:
            start: Starting position
            goal: Target position
            
        Returns:
            Tuple of (path, visited_set, nodes_explored_count)
        """
        if start == goal:
            return [start], {start}, 1
        
        stack = [start]
        visited = {start}
        parent = {start: None}
        nodes_explored = 0
        
        while stack:
            current = stack.pop()
            nodes_explored += 1
            
            if current == goal:
                path = self.reconstruct_path(parent, start, goal)
                return path, visited, nodes_explored
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    stack.append(neighbor)
        
        return None, visited, nodes_explored
    
    def find_path(self, start: Pos, goal: Pos, algorithm: str = "BFS") -> Tuple[Optional[List[Pos]], int]:
        """
        Find path using specified algorithm.
        
        Args:
            start: Starting position
            goal: Target position
            algorithm: "BFS" or "DFS"
            
        Returns:
            Tuple of (path, nodes_explored)
        """
        if algorithm == "BFS":
            path, _, nodes = self.bfs_find_path(start, goal)
        else:  # DFS
            path, _, nodes = self.dfs_find_path(start, goal)
        
        return path, nodes