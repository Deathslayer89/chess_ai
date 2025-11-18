"""
Modern Chess UI using CustomTkinter
Features: drag-and-drop, move highlighting, animations, commentary panel
"""

import tkinter as tk
import customtkinter as ctk
import chess
from datetime import datetime
from typing import Optional, Tuple, List
import config
from chess_engine import ChessGame
from chess_ai import ChessAI


# Unicode chess pieces
PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}


class ChessUI:
    """Modern Chess UI with CustomTkinter"""

    def __init__(self):
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Chess AI - Professional Edition")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")

        # Game components
        self.game = ChessGame()
        self.ai = ChessAI(depth=3)

        # UI state
        self.selected_square = None
        self.legal_moves_highlight = []
        self.last_move = None
        self.player_color = chess.WHITE
        self.ai_thinking = False
        self.hint_move = None
        self.previous_evaluation = 0

        # Create UI components
        self._create_widgets()
        self._draw_board()

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ctk.CTkFrame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        self._create_control_panel(left_panel)

        # Center - Chess board
        self.board_frame = ctk.CTkFrame(main_frame, width=config.BOARD_SIZE,
                                        height=config.BOARD_SIZE)
        self.board_frame.pack(side=tk.LEFT, padx=10)
        self.board_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.board_frame,
                               width=config.BOARD_SIZE,
                               height=config.BOARD_SIZE,
                               bg=config.BG_COLOR,
                               highlightthickness=0)
        self.canvas.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self._on_square_click)

        # Right panel - Game info and commentary
        right_panel = ctk.CTkFrame(main_frame, width=300)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self._create_info_panel(right_panel)

    def _create_control_panel(self, parent):
        """Create control panel with buttons and settings"""
        # Title
        title = ctk.CTkLabel(parent, text="Chess AI", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))

        # Game mode
        mode_label = ctk.CTkLabel(parent, text="Game Mode", font=("Arial", 14))
        mode_label.pack(pady=(20, 5))

        self.mode_var = tk.StringVar(value="vs_ai")

        mode_ai = ctk.CTkRadioButton(parent, text="Play vs AI",
                                     variable=self.mode_var,
                                     value="vs_ai")
        mode_ai.pack(pady=5)

        mode_human = ctk.CTkRadioButton(parent, text="Two Players",
                                        variable=self.mode_var,
                                        value="vs_human")
        mode_human.pack(pady=5)

        # Difficulty
        diff_label = ctk.CTkLabel(parent, text="AI Difficulty", font=("Arial", 14))
        diff_label.pack(pady=(20, 5))

        self.difficulty_var = tk.StringVar(value="Medium")

        for difficulty in ["Easy", "Medium", "Hard", "Expert"]:
            btn = ctk.CTkRadioButton(parent, text=difficulty,
                                    variable=self.difficulty_var,
                                    value=difficulty,
                                    command=self._on_difficulty_change)
            btn.pack(pady=5)

        # Player color
        color_label = ctk.CTkLabel(parent, text="Play as", font=("Arial", 14))
        color_label.pack(pady=(20, 5))

        self.color_var = tk.StringVar(value="white")

        color_white = ctk.CTkRadioButton(parent, text="White",
                                         variable=self.color_var,
                                         value="white",
                                         command=self._on_color_change)
        color_white.pack(pady=5)

        color_black = ctk.CTkRadioButton(parent, text="Black",
                                         variable=self.color_var,
                                         value="black",
                                         command=self._on_color_change)
        color_black.pack(pady=5)

        # Control buttons
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(pady=20, fill=tk.X, padx=10)

        self.new_game_btn = ctk.CTkButton(btn_frame, text="New Game",
                                          command=self._new_game)
        self.new_game_btn.pack(pady=5, fill=tk.X)

        self.undo_btn = ctk.CTkButton(btn_frame, text="Undo",
                                      command=self._undo_move)
        self.undo_btn.pack(pady=5, fill=tk.X)

        self.hint_btn = ctk.CTkButton(btn_frame, text="Get Hint",
                                      command=self._show_hint)
        self.hint_btn.pack(pady=5, fill=tk.X)

        self.save_btn = ctk.CTkButton(btn_frame, text="Save Game",
                                      command=self._save_game)
        self.save_btn.pack(pady=5, fill=tk.X)

        self.load_btn = ctk.CTkButton(btn_frame, text="Load Game",
                                      command=self._load_game)
        self.load_btn.pack(pady=5, fill=tk.X)

    def _create_info_panel(self, parent):
        """Create information and commentary panel"""
        # Game status
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_label = ctk.CTkLabel(status_frame, text="White to move",
                                         font=("Arial", 16, "bold"))
        self.status_label.pack(pady=10)

        # Move history
        history_label = ctk.CTkLabel(parent, text="Move History",
                                     font=("Arial", 14, "bold"))
        history_label.pack(pady=(10, 5))

        self.history_text = ctk.CTkTextbox(parent, height=200)
        self.history_text.pack(fill=tk.X, pady=(0, 10))

        # Commentary
        commentary_label = ctk.CTkLabel(parent, text="AI Commentary",
                                       font=("Arial", 14, "bold"))
        commentary_label.pack(pady=(10, 5))

        self.commentary_text = ctk.CTkTextbox(parent, height=300)
        self.commentary_text.pack(fill=tk.BOTH, expand=True)

    def _draw_board(self):
        """Draw the chess board and pieces"""
        self.canvas.delete("all")

        # Draw squares
        for rank in range(8):
            for file in range(8):
                x1 = file * config.SQUARE_SIZE
                y1 = rank * config.SQUARE_SIZE
                x2 = x1 + config.SQUARE_SIZE
                y2 = y1 + config.SQUARE_SIZE

                # Determine square color
                is_light = (rank + file) % 2 == 0
                color = config.LIGHT_SQUARE if is_light else config.DARK_SQUARE

                # Highlight selected square
                square = self.game.index_to_square(rank, file)
                if self.selected_square == square:
                    color = config.SELECTED_COLOR
                # Highlight last move
                elif self.last_move and (square == self.last_move.from_square or
                                        square == self.last_move.to_square):
                    color = config.LAST_MOVE_COLOR
                # Highlight legal moves
                elif square in [move.to_square for move in self.legal_moves_highlight]:
                    color = config.MOVE_HIGHLIGHT

                # Highlight hint
                if self.hint_move and (square == self.hint_move.from_square or
                                      square == self.hint_move.to_square):
                    # Draw with dashed border
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                 outline="blue", width=3,
                                                 dash=(10, 5))
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                 outline="")

                # Draw coordinates
                if file == 0:
                    self.canvas.create_text(x1 + 5, y1 + 5,
                                          text=str(8 - rank),
                                          font=("Arial", 10),
                                          fill="black" if is_light else "white")
                if rank == 7:
                    self.canvas.create_text(x2 - 5, y2 - 5,
                                          text=chr(ord('a') + file),
                                          font=("Arial", 10),
                                          fill="black" if is_light else "white")

        # Draw pieces
        for rank in range(8):
            for file in range(8):
                square = self.game.index_to_square(rank, file)
                piece = self.game.get_piece_at(square)

                if piece:
                    x = file * config.SQUARE_SIZE + config.SQUARE_SIZE // 2
                    y = rank * config.SQUARE_SIZE + config.SQUARE_SIZE // 2

                    # Get piece symbol
                    symbol = PIECE_SYMBOLS.get(piece.symbol(), piece.symbol())

                    # Draw piece
                    self.canvas.create_text(x, y, text=symbol,
                                          font=("Arial", 60),
                                          fill="white" if piece.color == chess.WHITE else "black")

    def _on_square_click(self, event):
        """Handle square click"""
        if self.ai_thinking or self.game.is_game_over():
            return

        # Get clicked square
        file = event.x // config.SQUARE_SIZE
        rank = event.y // config.SQUARE_SIZE

        if file < 0 or file > 7 or rank < 0 or rank > 7:
            return

        square = self.game.index_to_square(rank, file)

        # If in AI mode and not player's turn, ignore
        if (self.mode_var.get() == "vs_ai" and
            self.game.board.turn != self.player_color):
            return

        # If no square selected, select this square
        if self.selected_square is None:
            piece = self.game.get_piece_at(square)
            if piece and piece.color == self.game.board.turn:
                self.selected_square = square
                self.legal_moves_highlight = self.game.get_legal_moves_from_square(square)
                self.hint_move = None  # Clear hint
                self._draw_board()
        else:
            # Try to make move
            move = chess.Move(self.selected_square, square)

            # Check for promotion
            piece = self.game.get_piece_at(self.selected_square)
            if (piece and piece.piece_type == chess.PAWN and
                (chess.square_rank(square) == 0 or chess.square_rank(square) == 7)):
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)

            if move in self.game.board.legal_moves or \
               chess.Move(self.selected_square, square, promotion=chess.QUEEN) in self.game.board.legal_moves:

                # Store evaluation before move for blunder detection
                prev_eval = self.previous_evaluation

                # Make move
                self.game.make_move(move)
                self.last_move = move
                self.selected_square = None
                self.legal_moves_highlight = []

                # Update display
                self._update_move_history()
                self._draw_board()
                self._update_status()

                # Check for blunder
                if len(self.game.move_history) > 1:
                    current_eval = self.ai.evaluate_position(self.game.board)
                    # Flip evaluation if black just moved
                    if not self.game.board.turn:
                        current_eval = -current_eval

                    blunder_msg = self.ai.detect_blunder(prev_eval, current_eval)
                    if blunder_msg:
                        self._add_commentary(blunder_msg)

                    self.previous_evaluation = current_eval

                # Check game over
                if self.game.is_game_over():
                    self._handle_game_over()
                    return

                # AI move
                if self.mode_var.get() == "vs_ai":
                    self.root.after(500, self._make_ai_move)
            else:
                # Clicked on another piece of same color
                piece = self.game.get_piece_at(square)
                if piece and piece.color == self.game.board.turn:
                    self.selected_square = square
                    self.legal_moves_highlight = self.game.get_legal_moves_from_square(square)
                    self.hint_move = None
                    self._draw_board()
                else:
                    # Invalid move, deselect
                    self.selected_square = None
                    self.legal_moves_highlight = []
                    self.hint_move = None
                    self._draw_board()

    def _make_ai_move(self):
        """Make AI move"""
        if self.game.is_game_over():
            return

        self.ai_thinking = True
        self._update_status("AI is thinking...")

        # Find best move
        best_move, evaluation, commentary = self.ai.find_best_move(self.game.board)

        if best_move:
            self.game.make_move(best_move)
            self.last_move = best_move
            self.previous_evaluation = -evaluation  # Store from player's perspective

            # Update display
            self._draw_board()
            self._update_move_history()

            # Show commentary
            self._add_commentary("\n".join(commentary))

        self.ai_thinking = False
        self._update_status()

        # Check game over
        if self.game.is_game_over():
            self._handle_game_over()

    def _update_status(self, custom_text: Optional[str] = None):
        """Update status label"""
        if custom_text:
            self.status_label.configure(text=custom_text)
        elif self.game.is_game_over():
            self.status_label.configure(text=self.game.get_result())
        elif self.game.is_check():
            turn = "White" if self.game.board.turn == chess.WHITE else "Black"
            self.status_label.configure(text=f"{turn} in check!")
        else:
            turn = "White" if self.game.board.turn == chess.WHITE else "Black"
            self.status_label.configure(text=f"{turn} to move")

    def _update_move_history(self):
        """Update move history display"""
        self.history_text.delete("1.0", tk.END)

        moves = self.game.move_history
        board = chess.Board()

        history = []
        for i, move in enumerate(moves):
            move_san = board.san(move)
            board.push(move)

            if i % 2 == 0:
                history.append(f"{i//2 + 1}. {move_san}")
            else:
                history[-1] += f" {move_san}\n"

        self.history_text.insert("1.0", "".join(history))

    def _add_commentary(self, text: str):
        """Add commentary to commentary panel"""
        self.commentary_text.insert("1.0", f"\n{text}\n" + "="*40 + "\n")

    def _new_game(self):
        """Start a new game"""
        self.game.reset()
        self.selected_square = None
        self.legal_moves_highlight = []
        self.last_move = None
        self.hint_move = None
        self.ai_thinking = False
        self.previous_evaluation = 0

        self.history_text.delete("1.0", tk.END)
        self.commentary_text.delete("1.0", tk.END)

        self._draw_board()
        self._update_status()

        # If AI plays white
        if self.mode_var.get() == "vs_ai" and self.player_color == chess.BLACK:
            self.root.after(500, self._make_ai_move)

    def _undo_move(self):
        """Undo last move(s)"""
        if self.ai_thinking:
            return

        # In AI mode, undo 2 moves (player + AI)
        if self.mode_var.get() == "vs_ai":
            self.game.undo_move()
            self.game.undo_move()
        else:
            self.game.undo_move()

        self.selected_square = None
        self.legal_moves_highlight = []
        self.hint_move = None

        if len(self.game.move_history) > 0:
            self.last_move = self.game.move_history[-1]
        else:
            self.last_move = None

        self._draw_board()
        self._update_move_history()
        self._update_status()

    def _show_hint(self):
        """Show hint for current position"""
        if self.ai_thinking or self.game.is_game_over():
            return

        self.hint_move, hint_text = self.ai.get_hint(self.game.board)
        self._add_commentary("\n".join(hint_text))
        self._draw_board()

    def _save_game(self):
        """Save game to PGN file"""
        filename = f"chess_game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pgn"
        result = self.game.get_result() if self.game.is_game_over() else "*"
        self.game.save_pgn(filename, result=result)
        self._add_commentary(f"Game saved to {filename}")

    def _load_game(self):
        """Load game from PGN file"""
        # In a full implementation, this would open a file dialog
        # For now, just show message
        self._add_commentary("Load game feature - select a PGN file")

    def _on_difficulty_change(self):
        """Handle difficulty change"""
        difficulty = self.difficulty_var.get()
        self.ai.set_difficulty(difficulty)
        self._add_commentary(f"Difficulty changed to {difficulty}")

    def _on_color_change(self):
        """Handle player color change"""
        self.player_color = chess.WHITE if self.color_var.get() == "white" else chess.BLACK
        self._new_game()

    def _handle_game_over(self):
        """Handle game over"""
        result = self.game.get_result()
        self._add_commentary(f"Game Over: {result}")

    def run(self):
        """Start the UI"""
        self.root.mainloop()
