"""A self-written material-balance processor (stdlib only)."""

from __future__ import annotations

from ...positions import Position
from ..base import Assessment

# Standard material values (pawns = 1). Kings are not counted.
_PIECE_VALUES = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}


class MaterialProcessor:
    """Assess a position by its material balance.

    Returns a centipawn score from the side-to-move perspective (positive =
    better for the side to move), using the standard 1/3/3/5/9 values.
    ``info`` carries the raw material counts in pawns.
    """

    name = "material"

    def assess(self, position: Position, **params) -> Assessment:
        white = 0
        black = 0
        for ch in position.fen.split()[0]:
            if ch.isupper() and ch in _PIECE_VALUES:
                white += _PIECE_VALUES[ch]
            elif ch.islower() and ch.upper() in _PIECE_VALUES:
                black += _PIECE_VALUES[ch.upper()]

        # Positive = white ahead; flip if it is Black to move. Convert pawns
        # to centipawns to match the Assessment.score convention.
        cp = (white - black) * 100
        if position.side_to_move == "b":
            cp = -cp

        return Assessment(
            processor=self.name,
            score=cp,
            info={"white_material": white, "black_material": black},
        )
