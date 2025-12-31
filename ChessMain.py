import pygame as p

from Game import Game
from ChessConstants import *
from Rendering import Rendering
from Pieces import *
from Board import Board


class Main:
    def __init__(self):
        self.game = Game()
        self.rendering = Rendering(self.game)
        self.selectedsquare = []

    def mainloop(self):
        running = True
        runs = 0
        while running:
            self.rendering.draw()
            p.display.flip()
            self.rendering.clock.tick(60)

            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = p.mouse.get_pos()

                    col = mouse_x // SQSIZE
                    row = mouse_y // SQSIZE
                    pos = (row, col)

                    self.selectedsquare.append(pos)
                    print("selectedsquare:", self.selectedsquare)
                    print(len(self.selectedsquare))

                    if self.game.select_piece((row, col)):
                        print(f"Selected piece at {pos}")
                        
                    if len(self.selectedsquare) == 2:
                            from_pos = self.selectedsquare[0]
                            to_pos = self.selectedsquare[1]
                            print(f"Attempting to move from {from_pos} to {to_pos}")
                            print(self.game.get_legal_moves_for_selected())
                            '''if self.game.move_selected_piece(to_pos):
                                self.game.move_selected_piece(to_pos)
                                print(f"Moved piece from {from_pos} to {to_pos}")
                            else:
                                print(f"Invalid move from {from_pos} to {to_pos}")
                            self.selectedsquare = []'''

                    if not self.game.board.in_bounds(pos):
                        continue
                    
                    runs+=1
                    print("Frame:", runs)

        p.quit()


'''if __name__ == "__main__":
    Main().mainloop()'''

def test_ai_returns_legal_move():
    from Board import Board
    from ChessAI import ChessAI

    board = Board()
    board.setup_pieces()

    ai = ChessAI("white", depth=2)

    move = ai.choose_move(board)

    assert move is not None, "AI returned no move"

    from_pos, to_pos = move
    legal_moves = board.get_all_legal_moves("white")

    assert (from_pos, to_pos) in legal_moves, "AI returned an illegal move"

    print("✅ test_ai_returns_legal_move passed")
def test_ai_prefers_capture():
    from Board import Board
    from ChessAI import ChessAI
    from Pieces import Pawn, Queen

    board = Board()
    board.clear_board()

    board.grid[6][4] = Pawn("white", (6, 4))
    board.grid[1][4] = Pawn("black", (1, 4))
    board.grid[7][3] = Queen("white", (7, 3))

    ai = ChessAI("white", depth=2)
    move = ai.choose_move(board)

    assert move is not None

    from_pos, to_pos = move

    # Queen should capture pawn
    assert to_pos == (1, 4), "AI did not choose winning capture"

    print("✅ test_ai_prefers_capture passed")

def test_ai_avoids_blunder():
    from Board import Board
    from ChessAI import ChessAI
    from Pieces import Queen, Rook, King

    board = Board()
    board.clear_board()

    board.grid[7][3] = Queen("white", (7, 3))
    board.grid[0][3] = Rook("black", (0, 3))
    board.grid[7][4] = King("white", (7, 4))
    board.grid[0][4] = King("black", (0, 4))

    ai = ChessAI("white", depth=2)
    move = ai.choose_move(board)

    from_pos, to_pos = move

    # Queen should NOT move into rook capture
    assert to_pos != (0, 3), "AI blundered queen"

    print("✅ test_ai_avoids_blunder passed")

if __name__ == "__main__":
    test_ai_returns_legal_move()
    test_ai_prefers_capture()
    test_ai_avoids_blunder()


