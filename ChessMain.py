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
        import pygame as p

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
                            if self.game.move_selected_piece(to_pos):
                                self.game.move_selected_piece(to_pos)
                                print(f"Moved piece from {from_pos} to {to_pos}")
                            else:
                                print(f"Invalid move from {from_pos} to {to_pos}")
                            self.selectedsquare = []

                    if not self.game.board.in_bounds(pos):
                        continue
                    
                    runs+=1
                    print("Frame:", runs)

        p.quit()


if __name__ == "__main__":
    Main().mainloop()

