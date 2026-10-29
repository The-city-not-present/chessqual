"""The Position domain object: a single chess position."""

from __future__ import annotations

from dataclasses import dataclass, field

from .fen import is_valid_fen


@dataclass
class Position:
    """A single chess position, represented canonically by its FEN string.

    ``name`` and ``meta`` carry optional user metadata (label, comment, source
    game, tags, ...); ``meta`` is an extensible free-form dict.
    """

    fen: str
    name: str = ""
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        fen = self.fen.strip()
        if not is_valid_fen(fen):
            raise ValueError(f"invalid FEN: {self.fen!r}")
        self.fen = fen

    @property
    def side_to_move(self) -> str:
        """'w' or 'b' — the side to move, taken from the FEN."""
        return self.fen.split()[1]
