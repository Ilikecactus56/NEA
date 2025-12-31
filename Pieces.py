# This file is to manage the movement of pieces and not to manage the capture of pieces
# This is the foundation of the code i will write later such as the Game, Board and eventually Main file



from ChessConstants import *
from Board import *


class Piece:

    def __init__(self, colour, position):
        
        self.colour = colour
        self.position = position
        self.has_moved = False

    def __str__(self):
        return f"{self.colour} {self.__class__.__name__}"

    def __repr__(self):
        return self.__str__()
    
    def empty_at(self, board, position):
        piece = board.get_piece(position)
        return piece is None
    
    def enemy_at(self, board, position):
        piece = board.get_piece(position)
        return piece is not None and piece.colour != self.colour
    
    def friendly_at(self, board, position):
        piece = board.get_piece(position)
        return piece is not None and piece.colour == self.colour
    
    
    def get_moves(self, board):
        return[] # Gets overrieded by subclasses

class SlidingPiece(Piece):
    def sliding_moves(self, board, directions):
        moves = []
        row, col = self.position

        for deltar, deltac in directions:
            r, c = row + deltar, col + deltac
            while 0 <= r < 8 and 0 <= c < 8:
                if board.is_empty((r, c)):
                    moves.append((r, c))
                elif self.enemy_at(board, (r, c)): 
                    moves.append((r, c))
                    break
                else:
                    break
                r += deltar
                c += deltac

        return moves

class Pawn(Piece):
    value = 1

    def get_pseudo_moves(self, board):
        moves = []
        row , col = self.position
        direction = -1 if self.colour == "white" else 1
        start_row = 6 if self.colour == "white" else 1
        one_step = (row + direction , col) # For moving one step forward
              
        if board.in_bounds(one_step) and board.is_empty(one_step):
            moves.append(one_step)

        two_step = (row + 2 * direction, col) # For a pawn that hasn't moved yet
        if self.has_moved == False and board.is_empty(two_step) and board.is_empty(one_step):
            moves.append(two_step)
        
        for diagonalcapture in (-1, 1):
            target = (row + direction, col + diagonalcapture)
        
            if board.in_bounds(target) and self.enemy_at(board, target):
                moves.append(target)
        
        return moves

    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves

    

    
class Rook(SlidingPiece):
    value = 5
    directions = [(1,0),(0,1),(-1,0),(0,-1)]

    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves
    
    def get_pseudo_moves(self,board):
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        return self.sliding_moves(board, self.directions)
    
class Bishop(SlidingPiece):
    value = 3
    directions = [(1,1),(-1,-1),(1,-1),(-1,1)]

    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves
    
    def get_pseudo_moves(self,board):
        directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
        return self.sliding_moves(board, self.directions)
    
class Queen(SlidingPiece):
    value = 9
    directions = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]
    
    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves
    
    def get_pseudo_moves(self, board):
        directions = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]
        return self.sliding_moves(board, self.directions)
    
class King(Piece):
    value = 1000
    directions = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]

    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves
    
    def get_pseudo_moves(self, board):
        directions = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]
        moves = []
        row, col = self.position

        for deltar, deltac in self.directions:
            r, c = row + deltar , col + deltac
            while 0 <= r < 8  and 0 <= c < 8:
                if self.empty_at(board, (r, c)):
                    moves.append((r,c))
                elif self.enemy_at(board, (r, c)): 
                    moves.append((r, c))

                
        return moves
    
class Knight(Piece):
    Direction = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    def get_moves(self, board):
        legal_moves = []
        for move in self.get_pseudo_moves(board):
            board_copy = board.copy()
            board_copy._force_move(self.position, move)

            if not board_copy.is_in_check(self.colour):
                legal_moves.append(move)

        return legal_moves

    def get_pseudo_moves(self, board):
        Direction = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        moves = []
        row, col = self.position

        for deltar, deltac in Direction:
            r, c = row + deltar, col + deltac
            if 0 <= r < 8 and 0 <= c < 8:
                if board.is_empty((r, c)) or self.enemy_at(board, (r, c)):
                    moves.append((r, c))

        return moves