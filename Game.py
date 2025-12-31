from turtle import pos
from ChessConstants import *
from Board import Board
from Pieces import *
from ChessConstants import *


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white" 
        self.selected_piece = None
        self.move_history = []

    def select_piece(self, position):
        piece = self.board.get_piece(position)
        if piece and piece.colour == self.turn:
            self.selected_piece = piece
            return True
        return False
    
    def move_selected_piece(self, to_pos):
        if self.selected_piece is None:
            return False
        
        from_pos = self.selected_piece.position
        if to_pos not in self.selected_piece.get_moves(self.board):
            return False
        
        if self.board.move_piece(from_pos, to_pos):
            self.move_history.append((from_pos, to_pos))
            self.selected_piece.has_moved = True
            self.selected_piece = None
            self.turn = "black" if self.turn == "white" else "white"


        return True
    
    def reset_selection(self):
        self.selected_piece = None

    def get_turn(self):
        return self.turn
    
    def get_selected_piece(self):
        if self.selected_piece:
            return self.board.get_piece(self.selected_piece.position)
        return None

    def get_legal_moves_for_selected(self):
        piece = self.get_selected_piece()
        if piece:
            return piece.get_moves(self.board)
        return []

    def get_game_state(self):
        if self.board.is_checkmate(self.turn):
            return "checkmate"
        if self.board.is_stalemate(self.turn):
            return "stalemate"
        if self.board.is_in_check(self.turn):
            return "check"
        return "playing"

    def get_game_result(self):
        if self.board.is_checkmate(self.turn):
            winner = "Black" if self.turn == "white" else "White"
            return f"{winner} wins by checkmate"
        if self.board.is_stalemate(self.turn):
            return "Draw by stalemate"
        return None

    def undo_move(self):
        if not self.move_history:
            return False
        self.board = self.move_history.pop()
        self.turn = "black" if self.turn == "white" else "white"
        self.selected_piece = None
        return True

    def get_all_legal_moves(self, colour):
        moves = {}
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.colour == colour:
                    legal_moves = piece.get_moves(self.board)
                    if legal_moves:
                      moves[(row, col)] = legal_moves
        return moves
    
    def get_all_pieces(self, colour):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.colour == colour:
                    pieces.append(piece)
        return pieces
    
    def print_board(self):
        for row in self.board.grid:
            print([str(piece) if piece else "." for piece in row])

    def handle_click(self, pos):  # pos is the raw mouse (x,y)
    # Convert pixel coordinates to grid
        row = pos[1] // SQSIZE
        col = pos[0] // SQSIZE
        pos = (row, col)

        clicked_piece = self.board.get_piece(pos)

        # CASE 1: No piece selected
        if self.selected_piece is None:
            if clicked_piece and clicked_piece.colour == self.get_turn():
                self.selected_piece = clicked_piece
                self.legal_moves = clicked_piece.get_moves(self.board)
            return
    # CASE 2: Clicked a legal move
        if pos in self.legal_moves:
            if pos != self.selected_piece.position:  # Prevent moving to same square
                self.board.move_piece(self.selected_piece.position, pos)
            self.selected_piece = None
            self.legal_moves = []
            return

    # CASE 3: Clicked another own piece → switch selection
        if clicked_piece and clicked_piece.colour == self.get_turn():
            self.selected_piece = clicked_piece
            self.legal_moves = clicked_piece.get_moves(self.board)
            return

    # CASE 4: Clicked invalid square → deselect
        self.selected_piece = None
        self.legal_moves = []


    '''def handle_click(self, pos):
        clicked_piece = self.board.get_piece(pos)
        row = pos[1] // SQSIZE
        col = pos[0] // SQSIZE
        pos = (row, col)
        if self.selected_piece is None:
            if clicked_piece and clicked_piece.colour == self.get_turn():
                self.selected_piece = clicked_piece
                self.legal_moves = clicked_piece.get_moves(self.board)
            return

        if pos in self.legal_moves:
            self.board.move_piece(self.selected_piece.position, pos)
            self.selected_piece = None
            self.legal_moves = []
            return

        if clicked_piece and clicked_piece.colour == self.get_turn():
            self.selected_piece = clicked_piece
            self.legal_moves = clicked_piece.get_moves(self.board)
            return

    # --------------------------------------------------
    # CASE 3: Clicked another own piece → switch selection
    # --------------------------------------------------
        if clicked_piece and clicked_piece.colour == self.get_turn():
            self.selected_piece = clicked_piece
            self.legal_moves = clicked_piece.get_moves(self.board)
            return

    # --------------------------------------------------
    # CASE 4: Clicked invalid square → deselect
    # --------------------------------------------------
        self.selected_piece = None
        self.legal_moves = []


    def queue_pre_move(self, to_pos):
        pre_moves=[]

        selected_piece = self.get_selected_piece()  # Get the piece currently selected

        if selected_piece and selected_piece.colour == self.turn:
            from_pos = selected_piece.position   # Where the piece currently is
            self.pre_moves.append((from_pos, to_pos))  # Add to queue
            self.reset_selection()  # Clear selection after queuing
            return pre_moves

        return pre_moves
    

    def execute_pre_move(self):
        if self.queue_pre_move is None:
            return False  # No pre-moves queued
        
        pre_move = self.queue_pre_move

        from_pos, to_pos = pre_move[0]
        piece = self.board.get_piece(from_pos)  # Get the piece at from_pos

        if self.board.is_in_check(self.turn):
            self.queue_pre_move.clear()
            return False

        # Only execute if piece exists and belongs to current player
        if piece and piece.colour == self.turn:
            if self.board.move_piece(from_pos, to_pos):  # Move the piece
                self.pre_moves.pop(0)  # Remove the executed move
                self.turn = "black" if self.turn == "white" else "white"
                return True
        return False'''
