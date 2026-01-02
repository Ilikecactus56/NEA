import pygame as p
from ChessConstants import *
from Game import Game
import os


class Rendering:
    def __init__(self, game):
        p.init()
        self.game = game
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption("Chess")
        self.clock = p.time.Clock()
        
        # Initialize dictionary for images
        self.piece_images = {}
        self.load_images()
    
    # Load all piece images from the 'images' folder
    def load_images(self):
        folder = "images"  # Make sure your piece images are here
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                key = filename.replace(".png", "").lower()  # e.g., "white_pawn"
                path = os.path.join(folder, filename)
                image = p.image.load(path)
                image = p.transform.scale(image, (SQSIZE, SQSIZE))
                self.piece_images[key] = image

    # Draw the board squares
    def draw_board(self):
        colors = [	(238,238,210), (118,150,86)]  # Light, dark
        for row in range(ROWS):
            for col in range(COLS):
                color = colors[(row + col) % 2]
                p.draw.rect(self.screen, color, (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE))

    # Draw all pieces on the board
    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.board.get_piece((row, col))
                if piece:
                    key = f"{piece.colour}_{piece.__class__.__name__.lower()}"
                    image = self.piece_images.get(key)
                    if image:
                        self.screen.blit(image, (col*SQSIZE, row*SQSIZE))
    def highlight_selection(self):
        selected = self.game.get_selected_piece()
        if not selected:
            return

        # Highlight selected square (border only)
        r, c = selected.position
        rect = p.Rect(c * SQSIZE, r * SQSIZE, SQSIZE, SQSIZE)
        p.draw.rect(self.screen, (255, 215, 0), rect, 4)  # gold border

        # Highlight legal moves (small circles)
        for move in self.game.get_legal_moves_for_selected():
            mr, mc = move
            center = (
                mc * SQSIZE + SQSIZE // 2,
                mr * SQSIZE + SQSIZE // 2
            )
            p.draw.circle(self.screen, (50, 50, 50), center, 10)

    # Highlight selected piece and optionally its legal moves
    # Main draw method
    def draw(self):
        self.draw_board()
        self.draw_pieces()
        p.display.update()