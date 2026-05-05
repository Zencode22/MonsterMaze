#!/usr/bin/env python3
"""
Monster Maze - Escape the Labyrinth
GitHub Repository: https://github.com/Zencode22/MonsterMaze

Main entry point for the game.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game.config import GameConfig
from ui.menu import MainMenu


def main() -> None:
    """Main entry point for Monster Maze."""
    try:
        menu = MainMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for playing Monster Maze!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue on GitHub:")
        print(f"{GameConfig.REPO_URL}/issues")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()