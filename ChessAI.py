from Game import Game
from Board import Board
from ChessConstants import *
from Pieces import *

class ChessAI:
    def __init__(self, colour, depth=3):
        self.colour = colour
        self.depth = depth
        self.game = Game()
        self.board = Board()
        self.last_evaluation = 0
        self.last_move_type = None
        self.transposition_table = {}
        self.top_moves = []
        self.node_count = 0
        self.node_limit = 8000   # SAFE for pygame
        self.position_history = {}


        
    # ---------------------------------------------
    # Evaluation function (material-based)
    # ---------------------------------------------
    def is_opening(self, board):
        piece_count = 0
        for row in board.grid:
            for piece in row:
                if piece:
                    piece_count += 1
        return piece_count > 24  # opening ≈ before many captures

    def classify_move(self, board_before, from_pos, to_pos):
        piece = board_before.get_piece(from_pos)
        target = board_before.get_piece(to_pos)

        # Capture
        if target is not None:
            return "Capture"

        # Check
        board_copy = board_before.copy()
        board_copy._force_move(from_pos, to_pos)
        opponent = "black" if self.colour == "white" else "white"
        if board_copy.is_in_check(opponent):
            return "Check"

        # Development (minor pieces leaving back rank)
        if piece.__class__.__name__ in ("Knight", "Bishop"):
            start_rank = 7 if self.colour == "white" else 0
            if from_pos[0] == start_rank:
                return "Development"

        # Defensive (move blocks attack or removes threat)
        if board_before.is_square_attacked(from_pos, self.colour):
            return "Defensive"

        return "Neutral"
    
    def evaluate_material(self, board):
        """
        Material-only evaluation (for analysis display).
        Positive = advantage for AI colour
        """
        piece_values = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9
        }

        score = 0

        for row in board.grid:
            for piece in row:
                if piece:
                    value = piece_values.get(type(piece), 0)
                    if piece.colour == self.colour:
                        score += value
                    else:
                        score -= value

        return score
    
        piece = board_before.get_piece(from_pos)
        target = board_before.get_piece(to_pos)

        # Capture
        if target is not None:
            return "Capture"

        # Check
        board_copy = board_before.copy()
        board_copy._force_move(from_pos, to_pos)
        opponent = "black" if self.colour == "white" else "white"
        if board_copy.is_in_check(opponent):
            return "Check"

        # Development (minor pieces leaving back rank)
        if piece.__class__.__name__ in ("Knight", "Bishop"):
            start_rank = 7 if self.colour == "white" else 0
            if from_pos[0] == start_rank:
                return "Development"

        # Defensive (move blocks attack or removes threat)
        if board_before.is_square_attacked(from_pos, self.colour):
            return "Defensive"

        return "Neutral"
    def analyse_position(self, board):
        """
        Updates evaluation + top moves WITHOUT making a move
        """
        self.top_moves = []
        self.last_evaluation = 0

        best_value = float("-inf")

        all_moves = board.get_all_legal_moves_ai(self.colour)

        for from_pos, move_list in all_moves.items():
            for to_pos in move_list:
                new_board = board.copy()
                new_board._force_move(from_pos, to_pos)

                value = self.minimax(
                    new_board,
                    self.depth - 1,
                    float("-inf"),
                    float("inf"),
                    False
                )

                self.top_moves.append(((from_pos, to_pos), value))

                if value > best_value:
                    best_value = value

        self.top_moves.sort(key=lambda x: x[1], reverse=True)
        self.top_moves = self.top_moves[:5]
        self.last_evaluation = best_value



    def evaluate_board(self, board):
        piece_values = {
            Pawn: 100,
            Knight: 320,
            Bishop: 330,
            Rook: 500,
            Queen: 900,
            King: 20000
        }

        score = 0

        for row in board.grid:
            for piece in row:
                if piece:
                    value = piece_values[type(piece)]
                    if piece.colour == self.colour:
                        score += value
                    else:
                        score -= value
        # Opening central pawn bonus
        if self.is_opening(board):
            for r in range(8):
                for c in range(8):
                    piece = board.grid[r][c]
                    if isinstance(piece, Pawn) and piece.colour == self.colour:
                        if (r, c) in CENTER_SQUARES:
                            score += 40  # small but meaningful bonus



        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):

        # Terminal condition
        if depth == 0:
            return self.evaluate_board(board)

        opponent = "black" if self.colour == "white" else "white"
        # Checkmate & stalemate
        if board.is_in_checkmate(self.colour):
            return -float("inf")

        elif board.is_in_checkmate(opponent):
            return float("inf")
        elif board.is_in_stalemate(self.colour) or board.is_in_stalemate(opponent):
            return 0

        if maximizing_player == True:
            max_eval = float("-inf")

            for from_pos, to_pos in board.get_all_legal_moves(self.colour):
                new_board = board.copy()
                new_board._force_move(from_pos, to_pos)

                eval_score = self.minimax(
                    new_board, depth - 1, alpha, beta, False
                )

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = float("inf")

            for from_pos, to_pos in board.get_all_legal_moves(opponent):
                new_board = board.copy()
                new_board._force_move(from_pos, to_pos)

                eval_score = self.minimax(
                    new_board, depth - 1, alpha, beta, True
                )

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break

            return min_eval


    # ---------------------------------------------
    # Public method used by Game
    # ---------------------------------------------
    def find_best_move(self, board):
        best_move = None
        best_value = float("-inf")

        all_moves = board.get_all_legal_moves_ai(self.colour)

        for from_pos, move_list in all_moves.items():
            for to_pos in move_list:
                new_board = board.copy()
                new_board._force_move(from_pos, to_pos)

                value = self.minimax(
                    new_board,
                    self.depth - 1,
                    float("-inf"),
                    float("inf"),
                    False
                )
                board_before = board.copy()
                if value > best_value:
                    best_value = value
                    best_move = (from_pos, to_pos)
                    self.last_move_type = self.classify_move(board_before, from_pos, to_pos)

        return best_move