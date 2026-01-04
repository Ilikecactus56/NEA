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
        
    # ---------------------------------------------
    # Evaluation function (material-based)
    # ---------------------------------------------
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

            '''if type(piece).__name__ in ("Knight", "Bishop"):
                if piece.colour == self.colour:
                    if (piece.colour == "white" and row < 7) or (piece.colour == "black" and row > 0):
                        score += 0.3
                else:
                    if (piece.colour == "white" and row < 7) or (piece.colour == "black" and row > 0):
                        score -= 0.3

            # Discourage early queen movement
            if type(piece).__name__ == "Queen":
                if piece.colour == self.colour:
                    if (piece.colour == "white" and row < 6) or (piece.colour == "black" and row > 1):
                        score -= 0.5
                else:
                    if (piece.colour == "white" and row < 6) or (piece.colour == "black" and row > 1):
                        score += 0.5'''

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

                if value > best_value:
                    best_value = value
                    best_move = (from_pos, to_pos)

        return best_move