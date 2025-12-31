from Game import Game
from ChessConstants import *
from Rendering import Rendering
from Pieces import *
from Board import Board

g = Game()
print(type(g))
print(g.__class__.__module__)
print(hasattr(g, "get_selected_piece"))

