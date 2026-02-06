import pygame as p
from ChessConstants import *
from Pieces import *

class AnalysisWindow:
    def __init__(self, ai, game):
        self.game = game
        self.ai = ai

        self.font_title = p.font.SysFont(None, 36)
        self.font_text = p.font.SysFont(None, 22)
        self.font_small = p.font.SysFont(None, 20)

        self.x = BOARD_WIDTH
        self.y = 0
        self.width = ANALYSIS_WIDTH
        self.height = HEIGHT

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def count_material(self, colour):
        counts = {"Pawn":0, "Knight":0, "Bishop":0, "Rook":0, "Queen":0}
        for row in self.game.board.grid:
            for piece in row:
                if piece and piece.colour == colour:
                    name = piece.__class__.__name__
                    if name in counts:
                        counts[name] += 1
        return counts

    def format_counts(self, counts):
        return (
            f"P×{counts['Pawn']} "
            f"N×{counts['Knight']} "
            f"B×{counts['Bishop']} "
            f"R×{counts['Rook']} "
            f"Q×{counts['Queen']}"
        )

    def explain_move_legality(self):
        piece = self.game.get_selected_piece()
        if not piece:
            return "No piece selected"

        if piece.colour != self.game.turn:
            return "Not your turn"

        moves = piece.get_moves(self.game.board)
        if not moves:
            return "No legal moves (pinned or blocked)"

        return "Legal moves shown on board"

    def threat_info(self):
        board = self.game.board
        turn = self.game.turn

        if board.is_in_check(turn):
            return "⚠ King is under attack"

        piece = self.game.get_selected_piece()
        if piece:
            if board.is_square_attacked(piece.position, piece.colour):
                return "⚠ Selected piece is attacked"

        return "No immediate threats detected"

    # -------------------------------------------------
    # Draw
    # -------------------------------------------------
    def draw(self):
        screen = p.display.get_surface()

        panel = p.Rect(self.x, 0, self.width, self.height)
        p.draw.rect(screen, (40, 40, 40), panel)

        y = 20
        screen.blit(self.font_title.render("Analysis", True, (230,230,230)), (self.x+20, y))
        y += 50

        # -----------------------------
        # Game state
        # -----------------------------
        screen.blit(self.font_text.render(
            f"Turn: {self.game.turn.capitalize()}", True, (220,220,220)), (self.x+20, y))
        y += 25

        screen.blit(self.font_text.render(
            f"State: {self.game.get_game_state().capitalize()}", True, (220,220,220)), (self.x+20, y))
        y += 35

        # -----------------------------
        # Material breakdown
        # -----------------------------
        white_counts = self.count_material("white")
        black_counts = self.count_material("black")

        screen.blit(self.font_text.render("Material:", True, (230,230,230)), (self.x+20, y))
        y += 25

        screen.blit(self.font_small.render(
            f"White: {self.format_counts(white_counts)}", True, (200,200,200)), (self.x+30, y))
        y += 20

        screen.blit(self.font_small.render(
            f"Black: {self.format_counts(black_counts)}", True, (200,200,200)), (self.x+30, y))
        y += 35

        # -----------------------------
        # Evaluation
        # -----------------------------
        eval_val = getattr(self.ai, "last_evaluation", None)
        eval_text = f"Evaluation: {eval_val:.2f}" if eval_val is not None else "Evaluation: --"
        screen.blit(self.font_text.render(eval_text, True, (220,220,220)), (self.x+20, y))
        
        y += 28

        #-----------------------------
        # AI move time
        #-----------------------------
        ai_time = getattr(self.ai, "last_move_time", None)
        if ai_time is not None:
            time_text = f"AI Move Time: {ai_time:.2f}s"
        else:
            time_text = "AI Move Time: --"

        screen.blit(
            self.font_text.render(time_text, True, (220,220,220)),
            (self.x + 20, y)
        )

        # -----------------------------
        # Move legality explanation
        # -----------------------------
        y += 35
        screen.blit(self.font_text.render("Move Legality:", True, (230,230,230)), (self.x+20, y))
        y += 22
        screen.blit(self.font_small.render(
            self.explain_move_legality(), True, (200,200,200)), (self.x+30, y))
        y += 35

        # -----------------------------
        # Move History
        # -----------------------------
        screen.blit(
            self.font_text.render("Move History:", True, (230,230,230)),
            (self.x + 20, y)
        )
        y += 25

        history = self.game.move_history[-5:]  # last 5 moves only

        for i, move in enumerate(history):
            move_number = len(self.game.move_history) - len(history) + i + 1
            text = f"{move_number}. {move}"
            screen.blit(
                self.font_small.render(text, True, (200,200,200)),
                (self.x + 30, y)
            )
            y += 18
        
        y+=35

        # -----------------------------
        # Threat indicators
        # -----------------------------
        screen.blit(self.font_text.render("Threats:", True, (230,230,230)), (self.x+20, y))
        y += 22
        screen.blit(self.font_small.render(
            self.threat_info(), True, (255,160,160)), (self.x+30, y))
        y += 35

        if hasattr(self.ai, "last_move_type") and self.ai.last_move_type:
            move_type_text = f"Move Type: {self.ai.last_move_type}"
        else:
            move_type_text = "Move Type: --"

        move_type_surface = self.font_text.render(move_type_text, True, (220, 220, 220))
        screen.blit(move_type_surface, (self.x + 20, y))

