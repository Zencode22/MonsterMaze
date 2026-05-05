"""
Game configuration, constants, and map data.
"""

class GameConfig:
    """Central configuration for Monster Maze."""
    
    # Repository info
    REPO_NAME = "MonsterMaze"
    REPO_URL = "https://github.com/Zencode22/MonsterMaze"
    VERSION = "1.0.0"
    
    # ASCII display characters
    WALL_CHAR = '#'
    FLOOR_CHAR = '.'
    PLAYER_CHAR = 'P'
    EXIT_CHAR = 'E'
    BFS_MONSTER_CHAR = 'B'
    DFS_MONSTER_CHAR = 'D'
    
    # Game settings
    DEFAULT_DIFFICULTY = "BFS"
    
    # Scoring thresholds
    LEGENDARY_THRESHOLD = 40
    GREAT_THRESHOLD = 60
    GOOD_THRESHOLD = 80
    
    # Maze map definition
    MAZE_MAP = """
####################
#..................#
#.####.#####.####..#
#.#  #.#   #.#  #..#
#.#  #.#   #.#  #..#
#.#  #.#   #.#  #..#
#.####.#####.####..#
#..................#
#.####.# # #.####..#
#.#  #.# # #.#  #..#
#.#  #.# # #.#  #..#
#.####.# # #.####..#
#..................#
#.######.######....#
#.#    #.#    #....#
#.#    #.#    #....#
#.######.######....#
#..................#
#....#......#......#
####################
""".strip("\n")
    
    @classmethod
    def get_banner(cls) -> str:
        """Return the game banner."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                   MONSTER MAZE                                ║
║              Escape the Labyrinth... If You Can!              ║
║                                                              ║
║   GitHub: {cls.REPO_URL}  ║
║   Version: {cls.VERSION}                                           ║
╚══════════════════════════════════════════════════════════════╝
"""