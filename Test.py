from Board import Board
from ChessAI import ChessAI
from Pieces import Pawn, Rook, Knight, Bishop, Queen, King
from Game import Game

board = Board()
board.grid = [[None for _ in range(8)] for _ in range(8)]

board.place_piece(King("white", (7, 4)))
board.place_piece(King("black", (0, 4)))

ai = ChessAI("white")

print("Opening detected (endgame):", ai.is_opening(board))
