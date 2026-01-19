import pygame as p
from ChessConstants import *

class AnalysisWindow:
    def __init__(self, ai):
        """
        The analysis window does NOT create a new pygame window.
        It draws onto the right-hand side of the existing window.
        """
        self.ai = ai

        self.font_title = p.font.SysFont(None, 36)
        self.font_text = p.font.SysFont(None, 24)

        # Analysis panel position
        self.x = BOARD_WIDTH
        self.y = 0
        self.width = ANALYSIS_WIDTH
        self.height = HEIGHT

    def draw(self):
        """
        Draws the analysis panel:
        - background
        - evaluation
        - best move
        """
        screen = p.display.get_surface()

        # -----------------------------
        # Background panel
        # -----------------------------
        panel_rect = p.Rect(self.x, self.y, self.width, self.height)
        p.draw.rect(screen, (40, 40, 40), panel_rect)

        # -----------------------------
        # Title
        # -----------------------------
        title = self.font_title.render("Analysis", True, (220, 220, 220))
        screen.blit(title, (self.x + 20, 20))

        y_offset = 70

        # -----------------------------
        # Evaluation
        # -----------------------------
        if hasattr(self.ai, "last_evaluation"):
            eval_value = self.ai.last_evaluation
            eval_text = f"Evaluation: {eval_value:.2f}"
        else:
            eval_text = "Evaluation: --"

        eval_surface = self.font_text.render(eval_text, True, (220, 220, 220))
        screen.blit(eval_surface, (self.x + 20, y_offset))
        y_offset += 40