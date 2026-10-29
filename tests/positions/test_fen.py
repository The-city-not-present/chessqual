from chessqual.positions.fen import is_valid_fen

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_valid_start_position():
    assert is_valid_fen(START_FEN)


def test_valid_minimal_castling_and_en_passant():
    assert is_valid_fen("8/8/8/8/8/8/8/K6k w - - 0 1")


def test_invalid_too_few_fields():
    assert not is_valid_fen("8/8/8/8/8/8/8/K6k w - - 0")


def test_invalid_side_to_move():
    assert not is_valid_fen("8/8/8/8/8/8/8/K6k x - - 0 1")


def test_invalid_rank_file_count():
    assert not is_valid_fen("8/8/8/8/8/8/8/K7k w - - 0 1")


def test_invalid_halfmove_and_fullmove():
    assert not is_valid_fen("8/8/8/8/8/8/8/K6k w - - -1 1")
    assert not is_valid_fen("8/8/8/8/8/8/8/K6k w - - 0 0")


def test_non_string_rejected():
    assert not is_valid_fen(123)
