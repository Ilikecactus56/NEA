from Game import Game
from ChessAI import ChessAI
from Pieces import Pawn, Rook, Knight, Bishop, Queen, King
import time

game = Game()
ai = ChessAI("black")

start = time.time()
ai.find_best_move(game.board)
end = time.time()

print("Time:", end - start)
