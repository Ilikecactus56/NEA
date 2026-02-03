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
            if self.game.started:
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
                    if result == "white_human":
                            self.game.ai_players["white"] = False

                    elif result == "white_ai":
                        self.game.ai_players["white"] = True

                    elif result == "black_human":
                        self.game.ai_players["black"] = False

                    elif result == "black_ai":
                        self.game.ai_players["black"] = True

                    elif result == "start":
                        # Create AI instances only where needed
                        for colour in ("white", "black"):
                            if self.game.ai_players[colour]:
                                self.game.ai_instances[colour] = ChessAI(colour, depth=2)

                        # Use whichever AI exists for analysis window
                        active_ai = (
                            self.game.ai_instances["white"]
                            or self.game.ai_instances["black"]
                        )

                        self.analysis_window = AnalysisWindow(active_ai, self.game)
                        self.game.started = True

                elif event.type == p.KEYDOWN:
                    if self.game.pending_promotion:
                        if event.key == p.K_q:
                            self.game.promote_pawn(self.game.pending_promotion, "Queen")
                        elif event.key == p.K_r:
                            self.game.promote_pawn(self.game.pending_promotion, "Rook")
                        elif event.key == p.K_b:
                            self.game.promote_pawn(self.game.pending_promotion, "Bishop")
                        elif event.key == p.K_n:
                            self.game.promote_pawn(self.game.pending_promotion, "Knight")
                    elif event.key == p.K_z:
                        self.game.undo_move()
                    elif event.key == p.K_y:
                        self.game.redo_move()
                    elif event.key == p.K_w:
                        self.game.toggle_ai("white")
                    elif event.key == p.K_b:
                        self.game.toggle_ai("black")



            if self.game.started and not self.game.pending_promotion:
                current = self.game.turn

                if self.game.ai_players[current]:
                    ai = self.game.ai_instances[current]

                    move = ai.find_best_move(self.game.board)
                    if move:
                        from_pos, to_pos = move
                        self.game.board.move_piece(from_pos, to_pos)

                        # Update evaluation AFTER move
                        ai.last_evaluation = ai.evaluate_material(self.game.board)

                        if self.game.get_game_state() in ("checkmate", "stalemate"):
                            self.rendering.draw_game_over()

                        # Switch turn
                        self.game.turn = "black" if current == "white" else "white"




        p.quit()


if __name__ == "__main__":
    Main().mainloop()

