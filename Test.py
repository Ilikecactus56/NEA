# test_pawn.py

from Board import Board
from Pieces import Pawn
from Rendering import Rendering
from Game import Game
game = Game()
board = Board()
rendering = Rendering(game) 

# test_force_move.py
from Board import Board
from Pieces import Pawn

def test_force_move():
    board = Board()
    # Place a white pawn at (6,4)
    pawn = Pawn("white", (6,4))
    board.grid[6][4] = pawn

    print("Initial board:")
    for r in board.grid:
        print([type(p).__name__ if p else None for p in r])

    # Move pawn from (6,4) to (4,4)
    board._force_move((6,4), (4,4))

    print("\nBoard after _force_move:")
    for r in board.grid:
        print([type(p).__name__ if p else None for p in r])

if __name__ == "__main__":
    test_force_move()


# test_get_piece.py
from Board import Board
from Pieces import Pawn

def test_get_piece():
    board = Board()
    pawn = Pawn("white", (6,4))
    board.grid[6][4] = pawn

    piece = board.get_piece((6,4))
    if piece:
        print(f"Piece at (6,4): {piece.__class__.__name__}, {piece.colour}")
    else:
        print("No piece at (6,4)")

if __name__ == "__main__":
    test_get_piece()

# test_piece_images.py
from Pieces import Pawn
from Rendering import Rendering
from Board import Board

def test_piece_images():
    board = Board()
    pawn = Pawn("white", (6,4))
    board.grid[6][4] = pawn

    # Assume rendering object has piece_images dict
    from Game import Game
    game = Game()
    game.board = board
    rendering = Rendering(game)

    for row in range(8):
        for col in range(8):
            piece = board.get_piece((row,col))
            if piece:
                key = f"{piece.colour}_{piece.__class__.__name__.lower()}"
                if key not in rendering.piece_images:
                    print(f"Missing image key: {key}")
                else:
                    print(f"Found image key: {key}")

if __name__ == "__main__":
    test_piece_images()

# test_sqsize.py
SQSIZE = 80  # Replace with your actual square size

def test_click_to_square(mouse_x, mouse_y, sqsize):
    col = mouse_x // sqsize
    row = mouse_y // sqsize
    print(f"Mouse ({mouse_x},{mouse_y}) -> Grid ({row},{col})")

if __name__ == "__main__":
    test_click_to_square(130, 270, SQSIZE)
    test_click_to_square(400, 400, SQSIZE)
    test_click_to_square(799, 0, SQSIZE)
# test_rendering.py
import pygame as p
from Board import Board
from Pieces import Pawn
from Game import Game
from Rendering import Rendering

def test_rendering():
    p.init()
    screen = p.display.set_mode((640, 640))
    ROWS, COLS, SQSIZE = 8, 8, 80

    board = Board()
    pawn = Pawn("white", (6,4))
    board.grid[6][4] = pawn

    game = Game()
    game.board = board
    rendering = Rendering(game)
    rendering.screen = screen

    # Main loop for 2 seconds
    clock = p.time.Clock()
    running = True
    start_ticks = p.time.get_ticks()
    while running:
        screen.fill((0,0,0))  # Clear screen
        rendering.draw_pieces()
        p.display.flip()
        clock.tick(60)
        if p.time.get_ticks() - start_ticks > 2000:  # 2 seconds
            running = False

    p.quit()

if __name__ == "__main__":
    test_rendering()
