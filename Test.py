
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
