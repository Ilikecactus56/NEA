from ChessAI import ChessAI
from Game import Game
from ChessConstants import *
from Rendering import Rendering
from Pieces import *
from Board import Board
from Analysis import AnalysisWindow

class Main:
    def __init__(self):
        self.game = Game()
        self.rendering = Rendering(self.game)
        self.selectedsquare = []
        self.analysis_window = None




    def mainloop(self):
        import pygame as p

        running = True
        runs = 0
        while running:
            self.rendering.draw()
            self.rendering.highlight_selection()
            if self.game.started and self.game.vs_ai and self.game.ai:
                self.analysis_window.draw()
            p.display.flip()
            self.rendering.clock.tick(60)
            mouse_x, mouse_y = p.mouse.get_pos()

            if mouse_x < BOARD_WIDTH:
                col = mouse_x // SQSIZE
                row = mouse_y // SQSIZE
                pos = (row, col)
            else:
                pos = None



            for event in p.event.get():


                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN and not self.game.pending_promotion and self.game.started:
                    self.game.handle_click(pos)
                elif event.type == p.MOUSEBUTTONDOWN and not self.game.started:
                    result = self.rendering.start_menu_click(p.mouse.get_pos())
                    if result:
                        kind, value = result
                        self.game.handle_start_menu_choice(kind, value)
                        print("Menu choice:", kind, value)
                        print("Player colour:", self.game.player_colour)
                        print("Vs AI:", self.game.vs_ai)

                    # CREATE AI HERE
                        if self.game.vs_ai and self.game.ai is None and self.game.player_colour is not None:
                            ai_colour = "black" if self.game.player_colour == "white" else "white"
                            self.game.ai = ChessAI(ai_colour, depth=2)
                            self.analysis_window = AnalysisWindow(self.game.ai)
                            self.game.started = True

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


            if self.game.started and self.game.vs_ai and self.game.ai:
                if self.game.turn == self.game.ai.colour and not self.game.pending_promotion:

                    move = self.game.ai.find_best_move(self.game.board)
                    if move:
                        from_pos, to_pos = move
                        self.game.board.move_piece(from_pos, to_pos)

                            # Switch turn back to player
                        self.game.turn = self.game.player_colour


        p.quit()


if __name__ == "__main__":
    Main().mainloop()

