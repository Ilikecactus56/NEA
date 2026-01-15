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


        self.ai_button = p.Rect(300, 250, 200, 50)
        self.human_button = p.Rect(300, 310, 200, 50)
        self.white_button = p.Rect(300, 390, 200, 50)
        self.black_button = p.Rect(300, 450, 200, 50)

    
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

    def draw_promotion_menu(self):
        menu_width = SQSIZE * 4
        menu_height = SQSIZE
        menu_x = (WIDTH - menu_width) // 2
        menu_y = (HEIGHT - menu_height) // 2
        menu_rect = p.Rect(menu_x, menu_y, menu_width, menu_height)
        p.draw.rect(self.screen, (200, 200, 200), menu_rect)
        p.draw.rect(self.screen, (0, 0, 0), menu_rect, 2)

        piece_types = ["Queen", "Rook", "Bishop", "Knight"]
        for i, piece_type in enumerate(piece_types):
            key = f"{self.game.board.get_piece(self.game.pending_promotion).colour}_{piece_type.lower()}"
            image = self.piece_images.get(key)
            if image:
                x = menu_x + i * SQSIZE
                y = menu_y
                self.screen.blit(image, (x, y))

    def draw_start_menu(self):
        self.screen.fill((30, 30, 30))

        font = p.font.SysFont(None, 40)  # create font locally

        def draw_button(rect, text):
            p.draw.rect(self.screen, (200, 200, 200), rect)
            p.draw.rect(self.screen, (0, 0, 0), rect, 2)

            label = font.render(text, True, (0, 0, 0))
            self.screen.blit(label, label.get_rect(center=rect.center))

        draw_button(self.ai_button, "Play vs AI")
        draw_button(self.human_button, "2 Players")
        draw_button(self.white_button, "Play as White")
        draw_button(self.black_button, "Play as Black") 


    def start_menu_click(self, mouse_pos):
        if self.ai_button.collidepoint(mouse_pos):
            return ("opponent", "ai")
        if self.human_button.collidepoint(mouse_pos):
            return ("opponent", "human")
        if self.white_button.collidepoint(mouse_pos):
            return ("colour", "white")
        if self.black_button.collidepoint(mouse_pos):
            return ("colour", "black")
        return None

    def draw(self):
        if self.game.started:
            self.draw_board()
            self.draw_pieces()
        p.display.update()
        if self.game.pending_promotion:
            self.draw_promotion_menu()
        if not self.game.started:
            self.draw_start_menu()