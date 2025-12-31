from Board import Board
from ChessAI import ChessAI

board = Board()
ai = ChessAI("black", depth=2)

move = ai.choose_move(board)
print("AI move:", move)
