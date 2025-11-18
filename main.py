"""
Chess AI - Main Entry Point
A complete chess game with AI opponent

Features:
- Play against AI with adjustable difficulty
- Modern CustomTkinter UI
- Move highlighting and hints
- AI commentary and analysis
- Save/load games (PGN)
- Undo/redo moves
- Blunder detection
- Optional Stockfish integration

Author: Chess AI Project
Version: 1.0
"""

import sys
from chess_ui import ChessUI


def main():
    """Main entry point"""
    print("="*60)
    print("Chess AI - Professional Edition")
    print("="*60)
    print("\nFeatures:")
    print("  ✓ Play vs AI with 4 difficulty levels")
    print("  ✓ Modern dark theme UI")
    print("  ✓ Move hints and AI commentary")
    print("  ✓ Save/load games (PGN format)")
    print("  ✓ Undo moves")
    print("  ✓ Blunder detection")
    print("  ✓ Two-player mode")
    print("\nStarting game...")
    print("="*60)

    # Create and run UI
    app = ChessUI()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
