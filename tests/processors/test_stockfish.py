import pytest

from chessqual.positions import Position
from chessqual.processors import registry
from chessqual.processors.stockfish.processor import StockfishProcessor

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_stockfish_is_registered():
    assert "stockfish" in registry.names()


def test_stockfish_has_readable_failure_without_engine():
    proc = StockfishProcessor(engine_path="/nonexistent/stockfish")
    with pytest.raises(RuntimeError):
        proc.assess(Position(START_FEN), depth=1)
