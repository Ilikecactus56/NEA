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
        colors = [	(152, 107, 65), (23,71,48)]  # Light, dark
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

    # Highlight selected piece and optionally its legal moves
    '''def highlight_selection(self):
        selected = self.game.get_selected_piece()
        if selected:
            r, c = selected.position
            highlight_color = (255, 255, 0, 100)  # Yellow
            s = p.Surface((SQSIZE, SQSIZE), p.SRCALPHA)  # Transparent surface
            s.fill(highlight_color)
            self.screen.blit(s, (c*SQSIZE, r*SQSIZE))

            # Highlight legal moves
            for move in selected.get_moves(self.game.board):
                mr, mc = move
                move_color = (0, 0, 255, 100)  # Blue for legal moves
                s.fill(move_color)
                self.screen.blit(s, (mc*SQSIZE, mr*SQSIZE))
'''
    # Main draw method
    def draw(self):
        self.draw_board()
        self.draw_pieces()
        p.display.update()

'''class Rendering:

    def __init__(self, game):
        p.init()
        self.screen	= p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption("Chess")
        self.game = Game()
        self.clock = p.time.Clock()
        self.piece_images = {}   # <-- initialize here
        self.load_images()

    def draw(self):
        self.show_background(self.screen)
        # Additional rendering code will go here later
        self.draw_pieces(self.screen)

    def handle_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                return False

            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                board_pos = self.pixel_to_board(pos)
            self.game.select_square(board_pos)

        return True

    def pixel_to_board(self, pixel_pos):
        x, y = pixel_pos
        col = x // SQSIZE
        row = y // SQSIZE
        return (row, col)
    
    def load_images(self):
        folder = "images"  # Make sure your images are here
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                key = filename.replace(".png", "")  # e.g., "white_pawn"
                path = os.path.join(folder, filename)
                image = p.image.load(path)
                # Resize image to fit square
                image = p.transform.scale(image, (SQSIZE, SQSIZE))
                self.piece_images[key] = image

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.board.get_piece((row, col))  # Get each piece on the board
                if piece:
                    key = f"{piece.colour}_{piece.__class__.__name__.lower()}"  # e.g., "white_pawn"
                    image = self.piece_images.get(key)
                    if image:
                        surface.blit(image, (col * SQSIZE, row * SQSIZE))

    def show_background(self,surface ):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                p.draw.rect(surface,color,rect)'''