"""A collection of positions: the unit the tool always operates on."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator

from .position import Position


@dataclass
class Collection:
    """An ordered collection of positions.

    Working with a single position is just a collection of length one, so a
    collection — not a bare position — is the single unit the tool operates on.
    """

    name: str = ""
    positions: list[Position] = field(default_factory=list)

    # -- constructors -----------------------------------------------------
    @classmethod
    def from_position(cls, position: Position, name: str = "") -> "Collection":
        return cls(name=name, positions=[position])

    @classmethod
    def from_fens(cls, fens: Iterable[str], name: str = "") -> "Collection":
        return cls(name=name, positions=[Position(fen) for fen in fens])

    # -- mutation ---------------------------------------------------------
    def add(self, position: Position) -> None:
        self.positions.append(position)

    # -- sequence protocol -------------------------------------------------
    def __len__(self) -> int:
        return len(self.positions)

    def __iter__(self) -> Iterator[Position]:
        return iter(self.positions)

    def __getitem__(self, index: int) -> Position:
        return self.positions[index]
