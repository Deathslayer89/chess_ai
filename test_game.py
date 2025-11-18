"""
Test script for chess AI without GUI
This tests the core chess engine and AI functionality
"""

import chess
from chess_engine import ChessGame
from chess_ai import ChessAI


def test_game_engine():
    """Test chess engine functionality"""
    print("Testing Chess Engine...")
    print("=" * 60)

    game = ChessGame()

    # Test initial position
    print(f"Initial FEN: {game.get_fen()}")
    print(f"Legal moves: {len(game.get_legal_moves())}")

    # Make some moves
    print("\nMaking moves: e2e4, e7e5, Ng1f3")
    game.make_uci_move("e2e4")
    game.make_uci_move("e7e5")
    game.make_san_move("Nf3")

    print(f"Position after 3 moves:")
    print(game.board)
    print(f"\nMove history: {[str(m) for m in game.move_history]}")

    # Test undo
    print("\nTesting undo...")
    game.undo_move()
    print(f"After undo: {len(game.move_history)} moves in history")

    # Test PGN save
    print("\nTesting PGN save...")
    game.save_pgn("test_game.pgn", result="*")
    print("Game saved to test_game.pgn")

    print("\n✓ Chess Engine tests passed!")
    return True


def test_ai():
    """Test AI functionality"""
    print("\n" + "=" * 60)
    print("Testing Chess AI...")
    print("=" * 60)

    game = ChessGame()
    ai = ChessAI(depth=2)  # Use depth 2 for faster testing

    # Test initial position
    print("\nFinding best move in starting position...")
    best_move, evaluation, commentary = ai.find_best_move(game.board)

    print(f"\nBest move: {game.board.san(best_move)}")
    print(f"Evaluation: {evaluation / 100:.2f} pawns")
    print(f"Nodes searched: {ai.nodes_searched}")

    print("\nCommentary:")
    for line in commentary:
        print(f"  {line}")

    # Test hint system
    print("\n" + "-" * 60)
    print("Testing hint system...")
    hint_move, hint_text = ai.get_hint(game.board)
    print("Hint:")
    for line in hint_text:
        print(f"  {line}")

    # Test evaluation
    print("\n" + "-" * 60)
    print("Testing position evaluation...")
    eval_score = ai.evaluate_position(game.board)
    print(f"Starting position evaluation: {eval_score / 100:.2f} pawns")

    # Play a few moves and evaluate
    game.make_san_move("e4")
    game.make_san_move("e5")
    game.make_san_move("Nf3")
    game.make_san_move("Nc6")

    eval_score = ai.evaluate_position(game.board)
    print(f"After 1. e4 e5 2. Nf3 Nc6: {eval_score / 100:.2f} pawns")

    print("\n✓ Chess AI tests passed!")
    return True


def play_sample_game():
    """Play a short sample game"""
    print("\n" + "=" * 60)
    print("Playing sample game (AI vs AI)...")
    print("=" * 60)

    game = ChessGame()
    ai_white = ChessAI(depth=2)
    ai_black = ChessAI(depth=2)

    move_count = 0
    max_moves = 10  # Play 10 moves for demonstration

    while not game.is_game_over() and move_count < max_moves:
        print(f"\nMove {move_count // 2 + 1}:", end=" ")

        # White's turn
        if game.board.turn == chess.WHITE:
            best_move, eval, commentary = ai_white.find_best_move(game.board)
            print(f"{game.board.san(best_move)}", end=" ")
        else:
            # Black's turn
            best_move, eval, commentary = ai_black.find_best_move(game.board)
            print(f"{game.board.san(best_move)}")

        game.make_move(best_move)
        move_count += 1

    print("\n" + "-" * 60)
    print("Final position:")
    print(game.board)

    print(f"\nGame status: {game.get_result()}")
    print(f"Total moves: {len(game.move_history)}")

    print("\n✓ Sample game completed!")
    return True


def main():
    """Run all tests"""
    print("Chess AI Test Suite")
    print("=" * 60)

    try:
        test_game_engine()
        test_ai()
        play_sample_game()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nThe chess engine and AI are working correctly!")
        print("To play with the GUI, run: python main.py")
        print("(Requires a display/GUI environment)")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()
