from Game import Game
from ChessAI import ChessAI
from Pieces import Pawn, Rook, Knight, Bishop, Queen, King
import time
from Board import Board

game = Game()
game.board.grid = [[None]*8 for _ in range(8)]

game.board.set_piece((0, 4), King("black", (0, 4)))
game.board.set_piece((7, 4), King("white", (7, 4)))
game.board.set_piece((5, 5), Queen("white", (5, 5)))
game.board.set_piece((4, 4), Pawn("black", (4, 4)))
game.board.set_piece((3, 3), Pawn("black", (3, 3)))

ai = ChessAI("black", depth=4)

move = ai.find_best_move(game.board)
print("Trap avoidance:", move)
