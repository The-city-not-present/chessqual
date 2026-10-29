from chessqual.positions import Collection, Position

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_from_position_is_single_element_collection():
    p = Position(START_FEN)
    c = Collection.from_position(p, name="game")
    assert len(c) == 1
    assert c[0] is p
    assert c.name == "game"


def test_from_fens_builds_collection():
    c = Collection.from_fens([START_FEN, START_FEN.replace(" w ", " b ")])
    assert len(c) == 2
    assert [p.side_to_move for p in c] == ["w", "b"]


def test_add_and_iterate():
    c = Collection()
    c.add(Position(START_FEN))
    c.add(Position(START_FEN))
    assert len(c) == 2
    assert [p.fen for p in c] == [START_FEN, START_FEN]


def test_empty_collection():
    c = Collection()
    assert len(c) == 0
    assert list(c) == []
