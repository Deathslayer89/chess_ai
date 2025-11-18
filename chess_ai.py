"""
Chess AI with Minimax, Alpha-Beta Pruning, and Advanced Evaluation
"""

import chess
import random
from typing import Tuple, Optional, List
import config


class ChessAI:
    """Chess AI engine with minimax and evaluation"""

    def __init__(self, depth: int = 3):
        self.depth = depth
        self.nodes_searched = 0
        self.best_move_line = []
        self.evaluation_history = []

    def set_difficulty(self, difficulty: str):
        """Set AI difficulty level"""
        self.depth = config.AI_DEPTHS.get(difficulty, 3)

    def find_best_move(self, board: chess.Board) -> Tuple[Optional[chess.Move], float, List[str]]:
        """
        Find the best move using minimax with alpha-beta pruning
        Returns: (best_move, evaluation, commentary)
        """
        self.nodes_searched = 0
        self.best_move_line = []

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None, 0, ["No legal moves available"]

        # Randomize move order for variety at same evaluation
        random.shuffle(legal_moves)

        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Store top candidate moves for commentary
        move_evaluations = []

        for move in legal_moves:
            board.push(move)
            value = -self._minimax(board, self.depth - 1, -beta, -alpha, False)
            board.pop()

            move_evaluations.append((move, value))

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

        # Generate commentary
        commentary = self._generate_commentary(board, best_move, best_value, move_evaluations)

        return best_move, best_value, commentary

    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float,
                 maximizing: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning
        """
        self.nodes_searched += 1

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)

        legal_moves = list(board.legal_moves)

        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def evaluate_position(self, board: chess.Board) -> float:
        """
        Comprehensive position evaluation
        Considers: material, piece positioning, mobility, king safety, pawn structure
        """
        if board.is_checkmate():
            return -config.CHECKMATE_SCORE if board.turn == chess.WHITE else config.CHECKMATE_SCORE

        if board.is_stalemate() or board.is_insufficient_material():
            return config.STALEMATE_SCORE

        score = 0

        # Material and piece-square tables
        score += self._evaluate_material_and_position(board)

        # Mobility (number of legal moves)
        score += self._evaluate_mobility(board)

        # King safety
        score += self._evaluate_king_safety(board)

        # Pawn structure
        score += self._evaluate_pawn_structure(board)

        # Center control
        score += self._evaluate_center_control(board)

        return score

    def _evaluate_material_and_position(self, board: chess.Board) -> float:
        """Evaluate material balance and piece positioning"""
        score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            piece_value = config.PIECE_VALUES[piece.symbol().upper()]

            # Get piece-square table value
            if piece.symbol().upper() in config.PIECE_SQUARE_TABLES:
                table = config.PIECE_SQUARE_TABLES[piece.symbol().upper()]
                square_index = square if piece.color == chess.WHITE else (63 - square)
                position_value = table[square_index]
            else:
                position_value = 0

            total_value = piece_value + position_value

            if piece.color == chess.WHITE:
                score += total_value
            else:
                score -= total_value

        return score

    def _evaluate_mobility(self, board: chess.Board) -> float:
        """Evaluate piece mobility"""
        white_mobility = board.legal_moves.count() if board.turn == chess.WHITE else 0
        board.turn = not board.turn
        black_mobility = board.legal_moves.count()
        board.turn = not board.turn

        if board.turn == chess.BLACK:
            white_mobility, black_mobility = black_mobility, white_mobility

        return (white_mobility - black_mobility) * 10

    def _evaluate_king_safety(self, board: chess.Board) -> float:
        """Evaluate king safety based on pawn shield and nearby pieces"""
        score = 0

        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)

        if white_king_square is not None:
            score += self._king_safety_score(board, white_king_square, chess.WHITE)

        if black_king_square is not None:
            score -= self._king_safety_score(board, black_king_square, chess.BLACK)

        return score

    def _king_safety_score(self, board: chess.Board, king_square: int, color: chess.Color) -> float:
        """Calculate king safety score for one side"""
        score = 0
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        # Penalize king in center during opening/middlegame
        if len(board.piece_map()) > 10:  # Not endgame
            if 2 <= king_file <= 5:
                score -= 20

        # Reward castling
        if color == chess.WHITE:
            if board.has_kingside_castling_rights(color):
                score += 15
            if board.has_queenside_castling_rights(color):
                score += 10
        else:
            if board.has_kingside_castling_rights(color):
                score += 15
            if board.has_queenside_castling_rights(color):
                score += 10

        # Check pawn shield
        pawn_shield_squares = []
        if color == chess.WHITE and king_rank < 7:
            pawn_shield_squares = [
                chess.square(f, king_rank + 1) for f in range(max(0, king_file - 1), min(8, king_file + 2))
            ]
        elif color == chess.BLACK and king_rank > 0:
            pawn_shield_squares = [
                chess.square(f, king_rank - 1) for f in range(max(0, king_file - 1), min(8, king_file + 2))
            ]

        for sq in pawn_shield_squares:
            piece = board.piece_at(sq)
            if piece and piece.piece_type == chess.PAWN and piece.color == color:
                score += 10

        return score

    def _evaluate_pawn_structure(self, board: chess.Board) -> float:
        """Evaluate pawn structure (doubled, isolated, passed pawns)"""
        score = 0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        # Penalize doubled pawns
        for file in range(8):
            white_pawns_on_file = len([sq for sq in white_pawns if chess.square_file(sq) == file])
            black_pawns_on_file = len([sq for sq in black_pawns if chess.square_file(sq) == file])

            if white_pawns_on_file > 1:
                score -= 10 * (white_pawns_on_file - 1)
            if black_pawns_on_file > 1:
                score += 10 * (black_pawns_on_file - 1)

        # Reward passed pawns
        for square in white_pawns:
            if self._is_passed_pawn(board, square, chess.WHITE):
                score += 30

        for square in black_pawns:
            if self._is_passed_pawn(board, square, chess.BLACK):
                score -= 30

        return score

    def _is_passed_pawn(self, board: chess.Board, square: int, color: chess.Color) -> bool:
        """Check if pawn is a passed pawn"""
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        enemy_color = not color
        enemy_pawns = board.pieces(chess.PAWN, enemy_color)

        for enemy_square in enemy_pawns:
            enemy_file = chess.square_file(enemy_square)
            enemy_rank = chess.square_rank(enemy_square)

            # Check if enemy pawn is in front or on adjacent files
            if abs(enemy_file - file) <= 1:
                if color == chess.WHITE and enemy_rank > rank:
                    return False
                elif color == chess.BLACK and enemy_rank < rank:
                    return False

        return True

    def _evaluate_center_control(self, board: chess.Board) -> float:
        """Evaluate control of center squares"""
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        score = 0

        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += 20
                else:
                    score -= 20

            # Check if square is attacked
            if board.is_attacked_by(chess.WHITE, square):
                score += 5
            if board.is_attacked_by(chess.BLACK, square):
                score -= 5

        return score

    def _generate_commentary(self, board: chess.Board, best_move: chess.Move,
                            evaluation: float, move_evaluations: List[Tuple]) -> List[str]:
        """Generate human-readable commentary about the move"""
        commentary = []

        # Sort moves by evaluation
        sorted_moves = sorted(move_evaluations, key=lambda x: x[1], reverse=True)

        # Main move description
        if best_move:
            move_san = board.san(best_move)
            commentary.append(f"Best move: {move_san}")
            commentary.append(f"Evaluation: {evaluation / 100:.2f} pawns")

        # Position assessment
        if evaluation > 300:
            commentary.append("Position: White has a winning advantage")
        elif evaluation > 150:
            commentary.append("Position: White is better")
        elif evaluation > 50:
            commentary.append("Position: White has a slight edge")
        elif evaluation < -300:
            commentary.append("Position: Black has a winning advantage")
        elif evaluation < -150:
            commentary.append("Position: Black is better")
        elif evaluation < -50:
            commentary.append("Position: Black has a slight edge")
        else:
            commentary.append("Position: Roughly equal")

        # Top alternatives
        if len(sorted_moves) > 1:
            commentary.append(f"\nTop alternatives:")
            for i, (move, eval_score) in enumerate(sorted_moves[1:4]):
                move_san = board.san(move)
                commentary.append(f"  {i+2}. {move_san} ({eval_score / 100:.2f})")

        # Tactical information
        board.push(best_move)
        if board.is_check():
            commentary.append("This move gives check!")
        board.pop()

        commentary.append(f"\nNodes searched: {self.nodes_searched}")

        return commentary

    def detect_blunder(self, prev_eval: float, current_eval: float) -> Optional[str]:
        """Detect if a move was a blunder, mistake, or good move"""
        eval_change = prev_eval - current_eval  # From player's perspective

        if eval_change > config.BLUNDER_THRESHOLD:
            return "Blunder! You lost significant material or position."
        elif eval_change > config.MISTAKE_THRESHOLD:
            return "Mistake. This move weakened your position."
        elif eval_change < -config.GOOD_MOVE_THRESHOLD:
            return "Good move! Your position improved."

        return None

    def get_hint(self, board: chess.Board) -> Tuple[Optional[chess.Move], List[str]]:
        """Get a hint for the current position"""
        best_move, evaluation, commentary = self.find_best_move(board)

        hint_text = ["Hint:"]
        if best_move:
            hint_text.append(f"Consider playing {board.san(best_move)}")
            hint_text.extend(commentary)

        return best_move, hint_text
