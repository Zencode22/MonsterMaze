"""
Menu system for Monster Maze.
"""

from game.config import GameConfig
from game.grid import Maze, Pos
from game.pathfinding import PathFinder
from game.entities import Player, Monster
from game.renderer import Renderer
from ui.display import DisplayManager


class MainMenu:
    """Main menu system for the game."""
    
    def __init__(self):
        """Initialize menu system."""
        self.display = DisplayManager()
        self.game = None
    
    def run(self):
        """Run the main menu loop."""
        while True:
            self.display.clear_screen()
            self.display.print_banner()
            
            self._show_main_menu()
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                self._start_game()
            elif choice == '2':
                self._show_instructions()
            elif choice == '3':
                self.display.clear_screen()
                print("\nThanks for playing Monster Maze!")
                print(f"Star us on GitHub: {GameConfig.REPO_URL}")
                break
            else:
                print("Invalid choice. Please select 1-3.")
                input("Press Enter to continue...")
    
    def _show_main_menu(self):
        """Display the main menu options."""
        print("\nMAIN MENU")
        self.display.print_separator()
        print("1. Play Monster Maze")
        print("2. How to Play")
        print("3. Exit")
        self.display.print_separator()
    
    def _start_game(self):
        """Initialize and start a new game."""
        self.display.clear_screen()
        self.display.print_banner()
        
        print("\n" + "=" * 60)
        print("ESCAPE THE MONSTER MAZE!")
        print("=" * 60)
        
        # Initialize maze and game components
        maze = Maze(GameConfig.MAZE_MAP)
        pathfinder = PathFinder(maze)
        renderer = Renderer(maze)
        
        # Set up positions
        player_start = maze.find_player_start()
        exit_pos = maze.find_exit_position()
        monster_start = maze.find_monster_start(exit_pos)
        
        print(f"\nYou start at: {player_start}")
        print(f"Exit is at: {exit_pos}")
        print(f"Monster starts at: {monster_start}")
        
        # Choose difficulty
        monster_type = self._choose_difficulty()
        
        # Create entities
        player = Player(player_start)
        monster = Monster(monster_start, monster_type)
        
        # Show game info
        self._show_game_intro(monster)
        
        # Start game loop
        self.game = GameLoop(maze, pathfinder, renderer, player, monster, exit_pos)
        self.game.run()
    
    def _choose_difficulty(self) -> str:
        """Let player choose monster AI difficulty."""
        print("\nChoose your pursuer:")
        print("  [1] Draugr (D) - Undead warrior from Norse mythology")
        print("      Wanders the maze with relentless but meandering determination")
        print("      EASY MODE")
        print("  [2] Baba Yaga (B) - Cunning witch from Slavic folklore")
        print("      Flies through the maze, always knowing the shortest path to her prey")
        print("      HARD MODE")
        
        while True:
            choice = input("\nYour choice (1/2): ").strip()
            if choice == '1':
                return "DFS"
            elif choice == '2':
                return "BFS"
            else:
                print("Please choose 1 or 2!")
    
    def _show_game_intro(self, monster: Monster):
        """Show game introduction and controls."""
        print("\n" + "=" * 60)
        print(f"Your Pursuer: {monster.name} ({monster.char})")
        print(f"Origin: {monster.origin}")
        print(f"Difficulty: {monster.difficulty}")
        self.display.print_controls()
        self.display.print_legend(monster.ai_type)
        print("\nTIP: Use walls to your advantage!")
        print("=" * 60)
        input("\nPress Enter to start the game...")
    
    def _show_instructions(self):
        """Display game instructions."""
        self.display.clear_screen()
        self.display.print_banner()
        
        print("\nHOW TO PLAY MONSTER MAZE")
        self.display.print_separator()
        print("\nOBJECTIVE:")
        print("  Navigate through the maze from the top-left corner")
        print("  to the bottom-right exit without being caught!")
        print("\nTHE PURSUERS:")
        print("  Choose which creature hunts you through the maze:")
        print("\n  Draugr (D) - The Wandering Dead")
        print("  * Origin: Norse mythology")
        print("  * An undead warrior who guards burial mounds")
        print("  * Wanders relentlessly, exploring every passage")
        print("  * Can be outsmarted with clever movement")
        print("  * EASY MODE")
        print("\n  Baba Yaga (B) - The Witch of the Woods")
        print("  * Origin: Slavic folklore")
        print("  * A fearsome witch who flies in a magical mortar")
        print("  * Always knows the shortest path to her prey")
        print("  * Cunning and efficient in her hunt")
        print("  * HARD MODE")
        print("\nCONTROLS:")
        print("  W - Move Up")
        print("  A - Move Left")
        print("  S - Move Down")
        print("  D - Move Right")
        print("  Q - Quit game")
        print("\nLEGEND:")
        print("  P - Player")
        print("  D - Draugr (DFS Wandering Monster)")
        print("  B - Baba Yaga (BFS Hunting Monster)")
        print("  E - Exit")
        print("  # - Wall")
        print("  . - Floor")
        print("\nTIPS:")
        print("  * Use walls to block the monster's path")
        print("  * Baba Yaga always takes the shortest route - stay on the move!")
        print("  * Draugr can be tricked into dead ends and long corridors")
        print("  * Plan your route before you start moving")
        
        input("\nPress Enter to return to main menu...")


class GameLoop:
    """Main game loop handler."""
    
    def __init__(self, maze: Maze, pathfinder: PathFinder, renderer: Renderer,
                 player: Player, monster: Monster, exit_pos: Pos):
        """
        Initialize game loop.
        
        Args:
            maze: The game maze
            pathfinder: Pathfinding system
            renderer: Game renderer
            player: Player entity
            monster: Monster entity
            exit_pos: Exit position
        """
        self.maze = maze
        self.pathfinder = pathfinder
        self.renderer = renderer
        self.player = player
        self.monster = monster
        self.exit_pos = exit_pos
        self.display = DisplayManager()
        self.running = True
    
    def run(self):
        """Run the main game loop."""
        while self.running:
            self.display.clear_screen()
            self.display.print_banner()
            
            # Render game state
            game_state = self.renderer.render_game_state(
                self.player.position,
                self.monster.position,
                self.exit_pos,
                self.monster.ai_type
            )
            print(game_state)
            self.display.print_game_footer(
                self.monster.get_distance_to(self.player.position),
                self.player.get_distance_to(self.exit_pos)
            )
            
            # Check win/lose conditions
            if self._check_game_over():
                break
            
            # Player move
            if not self._handle_player_move():
                continue
            
            # Monster move
            self._handle_monster_move()
    
    def _check_game_over(self) -> bool:
        """Check if the game is over (win or lose)."""
        if self.player.position == self.monster.position:
            print(f"\nGAME OVER - {self.monster.name} caught you!")
            input("\nPress Enter to return to main menu...")
            return True
        
        if self.player.position == self.exit_pos:
            print(f"\nYOU WIN - You escaped {self.monster.name}!")
            input("\nPress Enter to return to main menu...")
            return True
        
        return False
    
    def _handle_player_move(self) -> bool:
        """
        Handle player input and movement.
        WSAD only - no arrow keys.
        
        Returns:
            True if move was processed, False if invalid
        """
        move = input("\nYour move (WASD): ").strip().lower()
        
        if move == 'q':
            self.display.clear_screen()
            print("\nGame quit. Thanks for playing Monster Maze!")
            self.running = False
            return False
        
        # Calculate new position - WSAD only
        dr, dc = self.player.position
        if move == 'w':
            dr -= 1
        elif move == 's':
            dr += 1
        elif move == 'a':
            dc -= 1
        elif move == 'd':
            dc += 1
        else:
            print("Invalid move! Use W/A/S/D keys only.")
            input("Press Enter to continue...")
            return False
        
        new_pos = (dr, dc)
        
        # Validate move
        if not self.maze.is_valid_position(new_pos):
            if not (0 <= dr < self.maze.rows and 0 <= dc < self.maze.cols):
                print("Can't move there - out of bounds!")
            else:
                print("Can't move there - wall!")
            input("Press Enter to continue...")
            return False
        
        self.player.move(new_pos)
        return True
    
    def _handle_monster_move(self):
        """Handle monster AI movement."""
        new_pos = self.monster.chase(self.pathfinder, self.player.position)
        
        if new_pos:
            path, _ = self.pathfinder.find_path(
                self.monster.position, 
                self.player.position, 
                self.monster.ai_type
            )
            if path:
                steps = len(path) - 1
                if self.monster.ai_type == "BFS":
                    print(f"{self.monster.name} flies toward you! ({steps} steps away)")
                else:
                    print(f"{self.monster.name} shambles through the maze... ({steps} steps away)")