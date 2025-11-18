# Chess AI - Quick Start Guide

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run the game
python main.py
```

## Testing Without GUI

If you don't have a display (headless server, SSH session), test the core functionality:

```bash
python test_game.py
```

This will:
- Test the chess engine
- Test the AI functionality
- Play a sample AI vs AI game
- Verify all features work correctly

## Files Overview

| File | Purpose |
|------|---------|
| `main.py` | GUI entry point - run this to play |
| `chess_engine.py` | Chess game logic (uses python-chess) |
| `chess_ai.py` | AI with minimax & evaluation |
| `chess_ui.py` | Modern CustomTkinter interface |
| `config.py` | Settings and constants |
| `stockfish_ai.py` | Optional Stockfish integration |
| `test_game.py` | Test suite (no GUI required) |

## Quick Play Guide

### In-Game Controls

**Mouse:**
- Click a piece to select it
- Click highlighted square to move

**Keyboard:**
- `z` - Undo move (takes back your move + AI move)
- `r` - Reset game

**Buttons:**
- **New Game** - Start fresh
- **Undo** - Take back move
- **Get Hint** - AI suggests best move
- **Save Game** - Export to PGN
- **Load Game** - Import from PGN

### Settings

**Game Mode:**
- Play vs AI (you vs computer)
- Two Players (local multiplayer)

**Difficulty:**
- Easy (depth 2) - ~0.1s per move
- Medium (depth 3) - ~0.5s per move
- Hard (depth 4) - ~2-5s per move
- Expert (depth 5) - ~10-30s per move

**Play As:**
- White (you move first)
- Black (AI moves first)

## Features Checklist

✅ Full chess rules (castling, en passant, promotion)
✅ Minimax AI with alpha-beta pruning
✅ Advanced evaluation (material, position, mobility, king safety)
✅ 4 difficulty levels
✅ Move highlighting
✅ AI commentary
✅ Hint system
✅ Blunder detection
✅ Undo/redo
✅ Save/load PGN
✅ Two-player mode
✅ Modern dark theme UI

## Troubleshooting

**"No module named 'chess'"**
```bash
pip install python-chess
```

**"No module named 'customtkinter'"**
```bash
pip install customtkinter
```

**No GUI/display available**
- Use `test_game.py` to test without GUI
- Install on a machine with display to use the full UI

**AI too slow**
- Reduce difficulty level
- Edit `config.py` to lower depth values

**Game crashes**
```bash
pip install -r requirements.txt --upgrade
python --version  # Should be 3.8+
```

## Advanced Usage

### Custom Evaluation Tuning

Edit `config.py` to adjust:
- Piece values
- Piece-square table values
- Search depths
- Blunder thresholds

### Stockfish Integration

1. Download Stockfish: https://stockfishchess.org/download/
2. Install and note the path
3. Use in code:

```python
from stockfish_ai import StockfishAI

stockfish = StockfishAI(stockfish_path="/path/to/stockfish", skill_level=10)
best_move, eval, commentary = stockfish.find_best_move(board)
```

## Performance Tips

- Lower difficulty for faster play
- Medium (depth 3) is recommended for casual games
- Expert (depth 5) can take 30+ seconds on complex positions
- Use Stockfish for instant analysis at any strength

## Next Steps

1. Play a few games to test the AI
2. Try different difficulty levels
3. Use hints to learn strategy
4. Save interesting games as PGN
5. Customize evaluation in `config.py`
6. Add Stockfish for analysis mode

---

**Need help?** Check the full [README.md](README.md) for detailed documentation.
