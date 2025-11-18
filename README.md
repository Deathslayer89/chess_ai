# Chess AI - Professional Edition

A complete chess game with AI opponent, built in Python with modern UI and advanced features.

![Chess AI](screenshot.png)

## Features

### Core Features
- **Play vs AI**: Four difficulty levels (Easy, Medium, Hard, Expert)
- **Two-Player Mode**: Play against a friend locally
- **Modern UI**: Clean, dark-themed interface using CustomTkinter
- **Legal Move Validation**: Powered by python-chess library

### AI Engine
- **Minimax Algorithm**: Classic game tree search
- **Alpha-Beta Pruning**: Efficient tree pruning for faster search
- **Advanced Evaluation**:
  - Material balance
  - Piece positioning (piece-square tables)
  - Mobility analysis
  - King safety
  - Pawn structure evaluation
  - Center control
- **Adjustable Depth**: 2-5 ply depending on difficulty

### Game Features
- **Move Highlighting**: See legal moves for selected piece
- **Last Move Highlight**: Visual feedback for previous move
- **Undo/Redo**: Take back moves (undoes both player and AI move)
- **Save/Load Games**: PGN format support
- **Move History**: Complete game notation display

### AI Features
- **Hint System**: Get AI suggestions for your moves
- **Move Commentary**: AI explains its moves and evaluations
- **Blunder Detection**: Warns when you make a poor move
- **Position Evaluation**: Real-time position scoring

### Optional
- **Stockfish Integration**: Use world-class Stockfish engine for analysis

## Installation

### Requirements
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the game**:
```bash
python main.py
```

### Dependencies
- `python-chess==1.999` - Chess logic and validation
- `customtkinter==5.2.2` - Modern UI framework
- `Pillow==10.3.0` - Image processing (for CustomTkinter)

## How to Play

### Basic Controls
1. **Select a piece**: Click on any piece of your color
2. **See legal moves**: Legal destination squares are highlighted
3. **Make a move**: Click on a highlighted square to move
4. **Wait for AI**: AI will respond after thinking

### Buttons
- **New Game**: Start a fresh game
- **Undo**: Take back the last move (your move + AI move)
- **Get Hint**: Ask AI for the best move suggestion
- **Save Game**: Export game to PGN file
- **Load Game**: Import game from PGN file

### Settings
- **Game Mode**: Choose between "Play vs AI" or "Two Players"
- **AI Difficulty**: Select Easy, Medium, Hard, or Expert
- **Play As**: Choose to play as White or Black

## Architecture

### Project Structure
```
chess_ai/
├── main.py              # Entry point
├── config.py            # Configuration and constants
├── chess_engine.py      # Game logic wrapper (python-chess)
├── chess_ai.py          # AI engine (minimax, evaluation)
├── chess_ui.py          # Modern UI (CustomTkinter)
├── stockfish_ai.py      # Optional Stockfish integration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Key Components

#### chess_engine.py
- Wraps python-chess library
- Handles game state, move validation
- PGN save/load functionality
- Board representation for UI

#### chess_ai.py
- Minimax search with alpha-beta pruning
- Position evaluation function
- Move commentary generation
- Blunder detection system
- Hint system

#### chess_ui.py
- Modern CustomTkinter interface
- Board rendering with Unicode pieces
- Move highlighting and selection
- Commentary and move history panels
- Game controls

#### config.py
- UI settings (colors, sizes)
- AI settings (depths, piece values)
- Piece-square tables
- Evaluation constants

## AI Implementation Details

### Minimax Algorithm
The AI uses the minimax algorithm to search the game tree and find the best move. It evaluates positions several moves ahead (depth) and assumes both players play optimally.

### Alpha-Beta Pruning
Alpha-beta pruning eliminates branches of the game tree that don't need to be searched, significantly improving performance without affecting the result.

### Position Evaluation
The evaluation function considers multiple factors:

1. **Material** (70%): Piece values with positional bonuses
2. **Mobility** (10%): Number of legal moves available
3. **King Safety** (10%): Pawn shield, castling rights
4. **Pawn Structure** (5%): Passed pawns, doubled pawns
5. **Center Control** (5%): Control of central squares

### Difficulty Levels
- **Easy**: Depth 2 (looks 2 moves ahead)
- **Medium**: Depth 3 (looks 3 moves ahead)
- **Hard**: Depth 4 (looks 4 moves ahead)
- **Expert**: Depth 5 (looks 5 moves ahead)

## Advanced Features

### Stockfish Integration
To use the world-class Stockfish engine:

1. Download Stockfish from https://stockfishchess.org/download/
2. Install it and note the path to the binary
3. Modify `stockfish_ai.py` to point to your Stockfish installation
4. Use in your code:
```python
from stockfish_ai import StockfishAI

stockfish = StockfishAI(stockfish_path="/path/to/stockfish")
best_move, eval, commentary = stockfish.find_best_move(board)
```

### PGN Format
Games are saved in standard PGN (Portable Game Notation) format, compatible with:
- Chess.com
- Lichess.org
- ChessBase
- Any PGN-compatible chess software

### Customization
Edit `config.py` to customize:
- UI colors and sizes
- Piece values
- Piece-square tables
- AI difficulty depths
- Blunder/mistake thresholds

## Development Roadmap

### Version 1.0 (Current)
- ✓ Complete chess rules implementation
- ✓ AI with minimax and alpha-beta
- ✓ Modern CustomTkinter UI
- ✓ Move highlighting
- ✓ Undo functionality
- ✓ Hint system
- ✓ AI commentary
- ✓ Blunder detection
- ✓ PGN save/load

### Future Enhancements
- Opening book integration
- Endgame tablebase support
- Move animations
- Sound effects
- Time controls/chess clock
- Move strength indicators
- Analysis mode with multiple lines
- Tournament mode
- Rating system
- Online play

## Troubleshooting

### "No module named 'customtkinter'"
Run: `pip install customtkinter`

### "No module named 'chess'"
Run: `pip install python-chess`

### UI looks wrong
Make sure you have the latest version of CustomTkinter:
```bash
pip install --upgrade customtkinter
```

### AI is too slow
- Lower the difficulty level
- Reduce search depth in `config.py`
- Consider using Stockfish for faster analysis

### Game crashes
- Check Python version (3.8+ required)
- Update all dependencies: `pip install -r requirements.txt --upgrade`
- Report issue with full error message

## Performance

### Typical Performance (on modern CPU)
- **Easy (Depth 2)**: ~0.1 seconds per move
- **Medium (Depth 3)**: ~0.5 seconds per move
- **Hard (Depth 4)**: ~2-5 seconds per move
- **Expert (Depth 5)**: ~10-30 seconds per move

Performance varies based on position complexity and number of legal moves.

## Contributing

This is an educational project. Feel free to:
- Add new evaluation features
- Improve the UI
- Optimize the search algorithm
- Add new game modes
- Fix bugs

## License

This project is open source and available for educational purposes.

## Credits

- **python-chess**: Niklas Fiekas (https://python-chess.readthedocs.io/)
- **CustomTkinter**: Tom Schimansky (https://github.com/TomSchimansky/CustomTkinter)
- **Chess piece Unicode symbols**: Unicode Consortium

## Contact

For questions, suggestions, or bug reports, please open an issue on GitHub.

---

**Enjoy playing chess against your own AI!** 🎮♟️
