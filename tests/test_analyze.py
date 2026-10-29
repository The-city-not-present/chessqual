from chessqual import Collection
from chessqual.analyze import assess

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_assess_returns_one_row_per_position():
    c = Collection.from_fens([START_FEN, START_FEN])
    results = assess(c, ["material"])
    assert len(results) == 2
    for position, row in results:
        assert position.fen == START_FEN
        assert set(row) == {"material"}
        assert row["material"].processor == "material"
        assert row["material"].score == 0
