"""
Grid/Maze representation and operations.
"""

from typing import List, Tuple, Optional

# Type aliases
Pos = Tuple[int, int]
Grid = List[List[str]]


class Maze:
    """Represents the game maze and provides maze-related operations."""
    
    def __init__(self, map_string: str):
        """
        Initialize maze from string representation.
        
        Args:
            map_string: Multiline string with # for walls, . for floors, spaces for walls
        """
        self.raw_map = map_string
        self.grid = self._parse_map(map_string)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.grid else 0
    
    def _parse_map(self, map_string: str) -> Grid:
        """Parse map string into 2D grid, treating spaces as walls."""
        lines = [line for line in map_string.strip().split('\n') if line.strip()]
        grid = [list(line) for line in lines]
        
        # Normalize - spaces become walls
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == ' ':
                    grid[r][c] = '#'
        
        return grid
    
    def is_wall(self, pos: Pos) -> bool:
        """Check if position is a wall."""
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == '#'
        return True  # Out of bounds is treated as wall
    
    def is_valid_position(self, pos: Pos) -> bool:
        """Check if position is within bounds and not a wall."""
        r, c = pos
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                self.grid[r][c] != '#')
    
    def get_neighbors(self, pos: Pos) -> List[Pos]:
        """Return valid 4-direction neighbors that are not walls."""
        r, c = pos
        candidates = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        return [(nr, nc) for nr, nc in candidates if self.is_valid_position((nr, nc))]
    
    def find_position(self, start_row: int = 0, start_col: int = 0, 
                     reverse: bool = False, char: str = '.') -> Optional[Pos]:
        """
        Find a position in the grid with the given character.
        
        Args:
            start_row: Starting row for search
            start_col: Starting column for search
            reverse: If True, search from bottom-right
            char: Character to find
            
        Returns:
            Position tuple or None if not found
        """
        if reverse:
            row_range = range(self.rows - 1, -1, -1)
            col_range = range(self.cols - 1, -1, -1)
        else:
            row_range = range(self.rows)
            col_range = range(self.cols)
        
        for r in row_range:
            for c in col_range:
                if self.grid[r][c] == char:
                    return (r, c)
        
        return None
    
    def find_player_start(self) -> Pos:
        """Find top-left most open space for player start."""
        pos = self.find_position(reverse=False)
        return pos if pos else (1, 1)
    
    def find_exit_position(self) -> Pos:
        """Find bottom-right most open space for exit."""
        pos = self.find_position(reverse=True)
        return pos if pos else (self.rows - 2, self.cols - 2)
    
    def find_monster_start(self, exit_pos: Pos) -> Pos:
        """Find a position adjacent to the exit for monster start."""
        ex, ey = exit_pos
        
        # Check 4 neighbors of exit first
        for r, c in [(ex+1, ey), (ex-1, ey), (ex, ey+1), (ex, ey-1)]:
            if self.is_valid_position((r, c)):
                return (r, c)
        
        # Fallback: search nearby area
        for r in range(max(0, ex-2), min(self.rows, ex+3)):
            for c in range(max(0, ey-2), min(self.cols, ey+3)):
                if (r, c) != exit_pos and self.is_valid_position((r, c)):
                    return (r, c)
        
        return (ex, ey)
    
    def get_cell(self, pos: Pos) -> str:
        """Get the character at a position."""
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return '#'