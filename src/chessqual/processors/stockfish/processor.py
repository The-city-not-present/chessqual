"""Stockfish processor: assess positions by querying a Stockfish engine.

Optional dependencies (see this package's ``requirements.txt``):
  - the ``chess`` package (python-chess) for board/UCI handling;
  - a Stockfish engine binary (via explicit path, ``STOCKFISH_PATH``, or PATH).

Both are resolved lazily at assessment time so that discovery/registration of
the processor never breaks when they are absent.
"""

from __future__ import annotations

import os
import shutil

from ...positions import Position
from ..base import Assessment

try:
    import chess
    import chess.engine
    _IMPORT_ERROR: Exception | None = None
except ImportError as exc:  # pragma: no cover - depends on environment
    chess = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc


class StockfishProcessor:
    """Assess positions with a Stockfish engine over UCI (via python-chess)."""

    name = "stockfish"

    def __init__(self, engine_path: str | None = None) -> None:
        self.engine_path = engine_path

    def _resolve_engine_path(self) -> str | None:
        return (
            self.engine_path
            or os.environ.get("STOCKFISH_PATH")
            or shutil.which("stockfish")
        )

    def assess(
        self,
        position: Position,
        *,
        depth: int = 15,
        movetime: float | None = None,
        **params,
    ) -> Assessment:
        if _IMPORT_ERROR is not None:
            raise RuntimeError(
                "the stockfish processor requires the optional 'chess' package "
                "(pip install -r src/chessqual/processors/stockfish/requirements.txt)"
            ) from _IMPORT_ERROR

        engine_path = self._resolve_engine_path()
        if not engine_path:
            raise RuntimeError(
                "stockfish engine not found: pass engine_path, set STOCKFISH_PATH, "
                "or put 'stockfish' on PATH"
            )

        board = chess.Board(position.fen)
        limit = chess.engine.Limit(depth=depth, time=movetime)
        try:
            with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
                result = engine.analyse(board, limit)
        except FileNotFoundError as exc:
            raise RuntimeError(f"could not start stockfish at {engine_path!r}") from exc

        return _to_assessment(result, board)


def _to_assessment(result, board) -> Assessment:
    score = result["score"].pov(board.turn)
    if score.is_mate():
        mate_in = score.mate()
        cp = None
    else:
        mate_in = None
        cp = score.score()

    pv = result.get("pv", [])
    best_move = pv[0].uci() if pv else None
    san = board.san(pv[0]) if pv else None

    return Assessment(
        processor="stockfish",
        score=cp,
        mate_in=mate_in,
        best_move=best_move,
        depth=result.get("depth"),
        info={"san": san, "nodes": result.get("nodes")},
    )
