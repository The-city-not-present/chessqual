from chessqual.positions import Position
from chessqual.processors.material.processor import MaterialProcessor

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
WHITE_UP_A_QUEEN = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
WHITE_DOWN_A_QUEEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1"


def test_start_position_is_equal():
    a = MaterialProcessor().assess(Position(START_FEN))
    assert a.score == 0


def test_white_up_a_queen_is_positive():
    a = MaterialProcessor().assess(Position(WHITE_UP_A_QUEEN))
    assert a.score == 900


def test_white_down_a_queen_is_negative():
    a = MaterialProcessor().assess(Position(WHITE_DOWN_A_QUEEN))
    assert a.score == -900


def test_score_is_side_to_move_relative():
    # Black to move in a materially equal position still scores 0.
    fen = START_FEN.replace(" w ", " b ")
    a = MaterialProcessor().assess(Position(fen))
    assert a.score == 0
