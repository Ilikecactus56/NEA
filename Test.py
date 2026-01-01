from Game import Game
from ChessAI import ChessAI
from Pieces import *
from Board import Board

board = Board()
game = Game()
ai = ChessAI("black", depth=2)

# Clear the board
game.board.grid = [[None for _ in range(8)] for _ in range(8)]


# Kings (required for legality)
game.board.set_piece((0, 4), King("black", (0, 4)))
game.board.set_piece((7, 4), King("white", (7, 4)))

# Black pawn that can capture
game.board.set_piece((3, 3), Pawn("black", (3, 3)))

# Free white pawn
game.board.set_piece((4, 4), Pawn("white", (4, 4)))
print("\n")

print(game.board.get_pieces("black"))
print(game.board.get_all_legal_moves("black"))
print(game.board.get_all_legal_moves_ai("black"))
move = ai.find_best_move(game.board)
print("AI move:", move)
