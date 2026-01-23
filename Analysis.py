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
        
        y += 35
        bar_x = self.x + self.width // 2 - 10
        bar_y = y + 40
        bar_height = 300
        bar_width = 20

        # Background
        p.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))

        # Clamp evaluation
        eval_value = max(-1000, min(1000, self.ai.last_evaluation))
        normalized = eval_value / 1000  # -1 to +1

        # Bar fill
        fill_height = int(bar_height * abs(normalized))
        if normalized > 0:
            fill_y = bar_y + (bar_height // 2 - fill_height)
            color = (200, 200, 200)  # White advantage
        else:
            fill_y = bar_y + bar_height // 2
            color = (50, 50, 50)     # Black advantage

        p.draw.rect(screen, color, (bar_x, fill_y, bar_width, fill_height))

        # Center line
        p.draw.line(
            screen,
            (150, 150, 150),
            (bar_x - 5, bar_y + bar_height // 2),
            (bar_x + bar_width + 5, bar_y + bar_height // 2),
            2
        )
        # -----------------------------
        # Move legality explanation
        # -----------------------------
        screen.blit(self.font_text.render("Move Legality:", True, (230,230,230)), (self.x+20, y))
        y += 22
        screen.blit(self.font_small.render(
            self.explain_move_legality(), True, (200,200,200)), (self.x+30, y))
        y += 35

        # -----------------------------
        # Threat indicators
        # -----------------------------
        screen.blit(self.font_text.render("Threats:", True, (230,230,230)), (self.x+20, y))
        y += 22
        screen.blit(self.font_small.render(
            self.threat_info(), True, (255,160,160)), (self.x+30, y))
        y += 35

        # -----------------------------
        # AI top moves
        # -----------------------------
        screen.blit(self.font_text.render("Top AI Moves:", True, (230,230,230)), (self.x+20, y))
        y += 25

        top_moves = getattr(self.ai, "top_moves", [])
        for i, (move, val) in enumerate(top_moves[:3]):
            text = f"{i+1}. {move} ({val:.1f})"
            screen.blit(self.font_small.render(text, True, (200,200,200)), (self.x+30, y))
            y += 20
            
        y += 20

        if hasattr(self.ai, "last_move_type") and self.ai.last_move_type:
            move_type_text = f"Move Type: {self.ai.last_move_type}"
        else:
            move_type_text = "Move Type: --"

        move_type_surface = self.font_text.render(move_type_text, True, (220, 220, 220))
        screen.blit(move_type_surface, (self.x + 20, y))

