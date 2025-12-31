from ChessConstants import *
import copy

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def copy(self):
        return copy.deepcopy(self)  

    def get_piece(self, position):
        row , col = position
        return self.grid[row][col]
    
    def get_pieces(self, colour):
        pieces = []
        for row in self.grid:
            for piece in row:
                if piece and piece.colour == colour:
                    pieces.append(piece)
        return pieces
    
    def in_bounds(self, position):
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_empty(self, position):
        row, col = position
        if self.grid[row][col] == None:
            return True
        else:
            return False
    
    def set_piece(self, position, piece): # This is used throughout the game
        row, col = position
        self.grid[row][col] = piece

    def place_piece(self, piece): # This is only used at startup
        row, col = piece.position
        self.grid[row][col] = piece 

    def setup_pieces(self):
        from Pieces import Pawn, Rook, Knight, Bishop, Queen, King

        for col in range(8):
            self.place_piece(Pawn("white", (6, col)))
            self.place_piece(Pawn("black", (1, col)))

        self.place_piece(Rook("white", (7, 0)))
        self.place_piece(Rook("white", (7, 7)))
        self.place_piece(Rook("black", (0, 0)))
        self.place_piece(Rook("black", (0, 7)))

        self.place_piece(Knight("white", (7, 1)))
        self.place_piece(Knight("white", (7, 6)))
        self.place_piece(Knight("black", (0, 1)))
        self.place_piece(Knight("black", (0, 6)))

        self.place_piece(Bishop("white", (7, 2)))
        self.place_piece(Bishop("white", (7, 5)))
        self.place_piece(Bishop("black", (0, 2)))
        self.place_piece(Bishop("black", (0, 5)))

        self.place_piece(Queen("white", (7, 3)))
        self.place_piece(Queen("black", (0, 3)))

        self.place_piece(King("white", (7, 4)))
        self.place_piece(King("black", (0, 4)))

    def move_piece(self, from_pos, to_pos):
        print("Attempting move:", from_pos, "->", to_pos)

        piece = self.get_piece(from_pos)
        print("Piece:", piece)
        if piece is None:
            print("FAIL: no piece")
            return False

        pseudo = piece.get_pseudo_moves(self)
        print("Pseudo moves:", pseudo)

        if to_pos not in pseudo:
            print("FAIL: not in pseudo")
            return False

        board_copy = self.copy()
        board_copy._force_move(from_pos, to_pos)

        print("Checking check...")
        if board_copy.is_in_check(piece.colour):
            print("FAIL: king in check")
            return False

        print("FORCE MOVE")
        self._force_move(from_pos, to_pos)
        piece.has_moved = True
        return True

        

    def _force_move(self,from_pos, to_pos):
        piece = self.get_piece(from_pos)
        if piece == None:
            return False
    
        self.set_piece(to_pos, piece)
        self.set_piece(from_pos, None)
        piece.position = to_pos


    def is_square_attacked(self, position, colour):
        board_copy = self.copy()
        for row in self.grid:
            for piece in row:
                if piece and piece.colour != colour:
                    if position in piece.get_pseudo_moves(board_copy):
                        return True
        return False
    
    def get_all_legal_moves(self, colour):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.colour == colour:
                    from_pos = (row, col)
                    print("FROM_POS:", from_pos)
                    print("Piece Moves:", piece.get_moves(self))

                    for to_pos in piece.get_moves(self):
                        print("TO_POS:", to_pos)
                        # OPTIONAL SAFETY CHECK:
                        # Ensure move does not leave king in check
                        test_board = self.copy()
                        test_board._force_move(from_pos, to_pos)

                        if not test_board.is_in_check(colour):
                            moves.append((from_pos, to_pos))

        return moves

    
    def find_king(self, colour):
        for row in self.grid:
            for piece in row:
                if piece and piece.colour == colour and piece.__class__.__name__ == "King":
                    return piece.position
    
    def is_in_check(self, colour):
        king_pos = self.find_king(colour)
        return self.is_square_attacked(king_pos, colour)

    def is_in_stalemate(self, colour):
        if self.is_in_check(colour):
            return False
        
        for piece in self.get_pieces(colour):
            if piece.get_moves(self):
                return False
        return True
    
    def is_in_checkmate(self, colour):
        if not self.is_in_check(colour):
            return False
        
        for piece in self.get_pieces(colour):
            if piece.get_moves(self):
                return False
        return True
    
    '''piece = self.get_piece(from_pos)
        print(piece)
        if piece is None:
            print("No piece at that square")
            return False
        pseudo_moves = piece.get_pseudo_moves(self)


        # Check pseudo-legal move
        if to_pos not in pseudo_moves:
            print("Not in that pieces moves")
            return False

        # Simulate move to check legality
        board_copy = self.copy()
        board_copy._force_move(from_pos, to_pos)

        if board_copy.is_in_check(piece.colour):
            print("Would be check")
            return False  # illegal, king would be in check

        # Perform move for real
        self._force_move(from_pos, to_pos)
        piece.has_moved = True
        return True'''