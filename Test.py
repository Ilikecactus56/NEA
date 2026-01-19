from Board import Board
from Pieces import Pawn, Rook, Knight, Bishop, Queen, King

board = Board()
board.grid = [[None]*8 for _ in range(8)]

king = King("white", (4, 4))
rook = Rook("black", (4, 7))

board.set_piece((4, 4), king)
board.set_piece((4, 7), rook)

print(king.get_moves(board))
