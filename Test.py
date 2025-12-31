
from ChessAI import ChessAI

# Create a board


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

if __name__ == "__main__":
    test_ai_returns_legal_move()