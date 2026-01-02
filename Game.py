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
        

        # Click same piece again → deselect
        if self.selected_piece and self.selected_piece.position == position:
            self.selected_piece = None
            self.legal_moves = []
            return False

        # Select own piece
        if piece and piece.colour == self.turn:
            self.selected_piece = piece
            self.legal_moves = piece.get_moves(self.board)
            return True
        
        if piece and piece.colour != self.turn:
            self.selected_piece = None
            self.legal_moves = []
            return False

        return False
    
    def handle_click(self, position):
        """
        Handles all mouse click logic:
        - selecting a piece
        - deselecting a piece
        - moving a selected piece
        """

        # Click outside the board
        if not self.board.in_bounds(position):
            self.selected_piece = None
            return

        clicked_piece = self.board.get_piece(position)

        # CASE 1: No piece selected yet → try to select
        if self.selected_piece is None:
            if clicked_piece and clicked_piece.colour == self.turn:
                self.selected_piece = clicked_piece
            return

        # CASE 2: Clicked the same piece again → deselect
        if clicked_piece == self.selected_piece:
            self.selected_piece = None
            return

        # CASE 3: Try to move selected piece
        if self.move_selected_piece(position):
            # Successful move
            self.selected_piece = None
            return

        # CASE 4: Click another own piece → switch selection
        if clicked_piece and clicked_piece.colour == self.turn:
            self.selected_piece = clicked_piece
            return

        # CASE 5: Invalid click → clear selection
        self.selected_piece = None
    
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
    
    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"
    
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

    '''def queue_pre_move(self, to_pos):
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
