"""
Chess Engine using python-chess library
Handles game state, move validation, and game logic
"""

import chess
import chess.pgn
from datetime import datetime
from typing import Optional, List, Tuple


class ChessGame:
    """Main chess game engine"""

    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        self.position_history = []

    def reset(self):
        """Reset the game to initial position"""
        self.board = chess.Board()
        self.move_history = []
        self.position_history = []

    def make_move(self, move: chess.Move) -> bool:
        """
        Make a move on the board
        Returns True if move was legal and made
        """
        if move in self.board.legal_moves:
            self.position_history.append(self.board.fen())
            self.move_history.append(move)
            self.board.push(move)
            return True
        return False

    def make_uci_move(self, uci: str) -> bool:
        """
        Make a move from UCI notation (e.g., 'e2e4')
        Returns True if move was legal and made
        """
        try:
            move = chess.Move.from_uci(uci)
            return self.make_move(move)
        except:
            return False

    def make_san_move(self, san: str) -> bool:
        """
        Make a move from SAN notation (e.g., 'Nf3')
        Returns True if move was legal and made
        """
        try:
            move = self.board.parse_san(san)
            return self.make_move(move)
        except:
            return False

    def undo_move(self) -> bool:
        """
        Undo the last move
        Returns True if there was a move to undo
        """
        if len(self.move_history) > 0:
            self.board.pop()
            self.move_history.pop()
            if self.position_history:
                self.position_history.pop()
            return True
        return False

    def get_legal_moves(self) -> List[chess.Move]:
        """Get list of all legal moves"""
        return list(self.board.legal_moves)

    def get_legal_moves_from_square(self, square: chess.Square) -> List[chess.Move]:
        """Get legal moves from a specific square"""
        return [move for move in self.board.legal_moves if move.from_square == square]

    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.board.is_game_over()

    def get_result(self) -> str:
        """Get game result"""
        if self.board.is_checkmate():
            return "Black wins by checkmate" if self.board.turn == chess.WHITE else "White wins by checkmate"
        elif self.board.is_stalemate():
            return "Draw by stalemate"
        elif self.board.is_insufficient_material():
            return "Draw by insufficient material"
        elif self.board.is_fifty_moves():
            return "Draw by fifty-move rule"
        elif self.board.is_repetition():
            return "Draw by repetition"
        return "Game in progress"

    def is_check(self) -> bool:
        """Check if current player is in check"""
        return self.board.is_check()

    def get_piece_at(self, square: chess.Square) -> Optional[chess.Piece]:
        """Get piece at a square"""
        return self.board.piece_at(square)

    def get_fen(self) -> str:
        """Get FEN representation of current position"""
        return self.board.fen()

    def set_fen(self, fen: str) -> bool:
        """Set position from FEN string"""
        try:
            self.board = chess.Board(fen)
            self.move_history = []
            self.position_history = []
            return True
        except:
            return False

    def save_pgn(self, filename: str, white_name: str = "Player",
                 black_name: str = "AI", result: str = "*"):
        """Save game to PGN file"""
        game = chess.pgn.Game()
        game.headers["Event"] = "Chess AI Game"
        game.headers["Site"] = "Local"
        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        game.headers["White"] = white_name
        game.headers["Black"] = black_name
        game.headers["Result"] = result

        node = game
        board = chess.Board()
        for move in self.move_history:
            node = node.add_variation(move)

        with open(filename, "w") as f:
            f.write(str(game))

    def load_pgn(self, filename: str) -> bool:
        """Load game from PGN file"""
        try:
            with open(filename, "r") as f:
                game = chess.pgn.read_game(f)

            if game is None:
                return False

            self.board = game.board()
            self.move_history = []
            self.position_history = []

            for move in game.mainline_moves():
                self.make_move(move)

            return True
        except:
            return False

    def get_board_representation(self) -> List[List[str]]:
        """
        Get 8x8 representation of board for UI
        Returns list of lists with piece symbols
        """
        board_rep = []
        for rank in range(7, -1, -1):  # Start from rank 8 down to 1
            row = []
            for file in range(8):  # a to h
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    row.append(piece.symbol())
                else:
                    row.append('')
            board_rep.append(row)
        return board_rep

    def square_name_to_index(self, square_name: str) -> Tuple[int, int]:
        """
        Convert square name (e.g., 'e4') to board indices
        Returns (rank, file) where rank 0 is 8th rank, file 0 is 'a' file
        """
        square = chess.parse_square(square_name)
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        return (7 - rank, file)  # Flip rank for display

    def index_to_square(self, rank: int, file: int) -> chess.Square:
        """
        Convert board indices to chess.Square
        rank: 0-7 (0 is 8th rank)
        file: 0-7 (0 is 'a' file)
        """
        return chess.square(file, 7 - rank)
