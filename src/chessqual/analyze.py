"""Convenience entry points for assessing positions with processors."""

from __future__ import annotations

from typing import Iterable

from .positions import Collection, Position
from .processors import Assessment, registry


def assess(
    collection: Collection,
    processors: Iterable[str] | None = None,
) -> list[tuple[Position, dict[str, Assessment]]]:
    """Assess every position in ``collection`` with the requested processors.

    ``processors`` is an iterable of processor names; when omitted, all
    registered processors are used.

    Returns a list of ``(position, {processor_name: Assessment})`` pairs, one
    per position in the collection.
    """
    names = list(processors) if processors is not None else registry.names()
    results: list[tuple[Position, dict[str, Assessment]]] = []
    for position in collection:
        row = {name: registry.get(name).assess(position) for name in names}
        results.append((position, row))
    return results
