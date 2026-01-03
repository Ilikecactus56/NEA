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
            self.rendering.highlight_selection()
            p.display.flip()
            self.rendering.clock.tick(60)
            mouse_x, mouse_y = p.mouse.get_pos()

            col = mouse_x // SQSIZE
            row = mouse_y // SQSIZE
            pos = (row, col)

            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN and not self.game.pending_promotion:
                    self.game.handle_click(pos)
                elif event.type == p.KEYDOWN and self.game.pending_promotion:
                    if event.key == p.K_q:
                        self.game.promote_pawn(self.game.pending_promotion, "Queen")
                    elif event.key == p.K_r:
                        self.game.promote_pawn(self.game.pending_promotion, "Rook")
                    elif event.key == p.K_b:
                        self.game.promote_pawn(self.game.pending_promotion, "Bishop")
                    elif event.key == p.K_n:
                        self.game.promote_pawn(self.game.pending_promotion, "Knight")

                    self.game.pending_promotion = None

        p.quit()


if __name__ == "__main__":
    Main().mainloop()

