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

        return score

    # ---------------------------------------------
    # Minimax with alpha–beta pruning
    # ---------------------------------------------
    '''def minimax(self, board, depth, alpha, beta, maximizing_player):
        print("ENTERED MINIMAX | depth:", depth)

        # Terminal depth
        if depth == 0:
            return self.evaluate_board(board)
        print("DEPTH NOT ZERO")
        opponent = "black" if self.colour == "white" else "white"
        current_colour = self.colour if maximizing_player else opponent
        print("CURRENT COLOUR:", current_colour)
        # Terminal game states
        if board.is_in_checkmate(current_colour):
            return -float("inf") if maximizing_player else float("inf")
        print("NOT CHECKMATE")
        if board.is_in_stalemate(current_colour):
            return 0
        print("NOT STALEMATE")
        legal_moves = board.get_all_legal_moves(current_colour)
        print("LEGAL MOVES:", legal_moves)
        if maximizing_player:
            max_eval = float("-inf")

            for from_pos, moves in legal_moves.items():
                for to_pos in moves:
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
        print("MINIMIZING")

        for from_pos, moves in legal_moves.items():
            for to_pos in moves:
                new_board = board.copy()
                new_board._force_move(from_pos, to_pos)

                eval_score = self.minimax(
                    new_board, depth - 1, alpha, beta, True
                )

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break

        return min_eval'''
    
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

        all_moves = self.game.get_all_legal_moves(self.colour)

        for from_pos, move_list in all_moves.items():
            for to_pos in move_list:
                new_board = self.game.board.copy()
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

