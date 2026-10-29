import pytest

from chessqual.positions import Position

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_position_holds_fen_and_side_to_move():
    p = Position(START_FEN)
    assert p.fen == START_FEN
    assert p.side_to_move == "w"


def test_position_strips_whitespace():
    p = Position("  " + START_FEN + "  ")
    assert p.fen == START_FEN


def test_position_black_to_move():
    fen = START_FEN.replace(" w ", " b ")
    assert Position(fen).side_to_move == "b"


def test_position_rejects_invalid_fen():
    with pytest.raises(ValueError):
        Position("not a fen")


def test_position_defaults_name_and_meta():
    p = Position(START_FEN)
    assert p.name == ""
    assert p.meta == {}
