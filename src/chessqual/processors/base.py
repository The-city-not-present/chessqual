"""Processor contract and the Assessment result type."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class Assessment:
    """The result of assessing a single position with a single processor.

    ``score`` is in centipawns from the **side to move**'s perspective
    (positive = better for the side to move). ``mate_in`` is set instead when
    the processor reports a forced mate. ``info`` carries processor-specific
    extras so results stay extensible without schema changes.
    """

    processor: str
    score: float | None = None
    mate_in: int | None = None
    best_move: str | None = None
    depth: int | None = None
    info: dict[str, Any] = field(default_factory=dict)


class Processor(Protocol):
    """The contract every processor implements.

    A processor is any object with a ``name`` and an
    ``assess(position, **params) -> Assessment`` method. Concrete processors are
    plain classes; they are not required to inherit from anything.
    """

    name: str

    def assess(self, position: Any, **params: Any) -> Assessment: ...
