"""
Optional Stockfish engine integration
Requires Stockfish binary to be installed
"""

import chess
import chess.engine
from typing import Optional, Tuple, List


class StockfishAI:
    """Stockfish chess engine wrapper"""

    def __init__(self, stockfish_path: str = "stockfish", skill_level: int = 10):
        """
        Initialize Stockfish engine

        Args:
            stockfish_path: Path to Stockfish binary
            skill_level: Skill level 0-20 (0=weakest, 20=strongest)
        """
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            self.skill_level = skill_level
            self.engine.configure({"Skill Level": skill_level})
            self.available = True
        except Exception as e:
            print(f"Stockfish not available: {e}")
            self.engine = None
            self.available = False

    def find_best_move(self, board: chess.Board, time_limit: float = 1.0) -> Tuple[Optional[chess.Move], float, List[str]]:
        """
        Find best move using Stockfish

        Args:
            board: Current board position
            time_limit: Time limit in seconds

        Returns:
            (best_move, evaluation, commentary)
        """
        if not self.available:
            return None, 0, ["Stockfish not available"]

        try:
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            best_move = result.move

            # Get evaluation
            info = self.engine.analyse(board, chess.engine.Limit(time=time_limit))
            score = info["score"].relative.score(mate_score=10000)

            commentary = [
                f"Stockfish (Level {self.skill_level})",
                f"Best move: {board.san(best_move)}",
                f"Evaluation: {score / 100:.2f} pawns"
            ]

            return best_move, score, commentary

        except Exception as e:
            print(f"Stockfish error: {e}")
            return None, 0, [f"Error: {e}"]

    def set_skill_level(self, level: int):
        """Set Stockfish skill level (0-20)"""
        if self.available and 0 <= level <= 20:
            self.skill_level = level
            self.engine.configure({"Skill Level": level})

    def close(self):
        """Close the engine"""
        if self.engine:
            self.engine.quit()


# Example usage
if __name__ == "__main__":
    board = chess.Board()

    # Try to initialize Stockfish
    stockfish = StockfishAI()

    if stockfish.available:
        print("Stockfish is available!")
        best_move, eval, commentary = stockfish.find_best_move(board)
        print("\n".join(commentary))
        stockfish.close()
    else:
        print("Stockfish not found. Install it to use this feature.")
        print("Download from: https://stockfishchess.org/download/")
