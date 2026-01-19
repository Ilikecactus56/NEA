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
        self.pending_promotion = None
        self.vs_ai = None          # True or False
        self.player_colour = None # "white" or "black"
        self.started = False
        self.ai = None  # Placeholder for AI player

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
            self.turn = "black" if self.turn == "white" else "white"

            if isinstance(self.board.get_piece(to_pos), Pawn):
                row, col = to_pos
                if (self.board.get_piece(to_pos).colour == "white" and row == 0) or (self.board.get_piece(to_pos).colour == "black" and row == 7):
                    self.pending_promotion = to_pos
                    self.selected_piece = None
                    pass

        self.selected_piece = None
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
        if self.board.is_in_checkmate(self.turn):
            return "checkmate"
        if self.board.is_in_stalemate(self.turn):
            return "stalemate"
        if self.board.is_in_check(self.turn):
            return "check"
        return "playing"

    def get_game_result(self):
        if self.board.is_in_checkmate(self.turn):
            winner = "Black" if self.turn == "white" else "White"
            return f"{winner} wins by checkmate"
        if self.board.is_in_stalemate(self.turn):
            return "Draw by stalemate"
        return None

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

    def promote_pawn(self, position, new_piece_type):
        pawn = self.board.get_piece(position)
        if not pawn or pawn.__class__.__name__ != "Pawn":
            return False
        
        row, col = position
        if (pawn.colour == "white" and row != 0) or (pawn.colour == "black" and row != 7):
            return False
        
        if new_piece_type == "Queen":
            new_piece = Queen(pawn.colour, position)
        elif new_piece_type == "Rook":
            new_piece = Rook(pawn.colour, position)
        elif new_piece_type == "Bishop":
            new_piece = Bishop(pawn.colour, position)
        elif new_piece_type == "Knight":
            new_piece = Knight(pawn.colour, position)
        else:
            return False
        
        self.board.set_piece(position, new_piece)
        self.pending_promotion = None
        return True
    
    def make_ai_move(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        self.selected_piece = piece
        self.move_selected_piece(to_pos)


    def handle_start_menu_choice(self, choice_type, value):
        if choice_type == "opponent":
            self.vs_ai = (value == "ai")
            if value == "human":
                self.ai = None

        elif choice_type == "colour":
            self.player_colour = value
            self.turn = "white"  # white always starts

        if self.player_colour is not None:
            self.started = True
