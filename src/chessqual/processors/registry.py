"""Global processor registry (app-level, extensible)."""

from __future__ import annotations

from .base import Processor


class Registry:
    """A simple name → processor registry.

    The single app-level instance is ``registry`` (lowercase) at the bottom of
    this module; built-in processors are registered in
    ``chessqual.processors.__init__``.
    """

    def __init__(self) -> None:
        self._processors: dict[str, Processor] = {}

    def register(self, processor: Processor) -> Processor:
        name = processor.name
        if not name:
            raise ValueError("processor must have a non-empty name")
        if name in self._processors:
            raise ValueError(f"processor already registered: {name!r}")
        self._processors[name] = processor
        return processor

    def get(self, name: str) -> Processor:
        try:
            return self._processors[name]
        except KeyError:
            available = ", ".join(sorted(self._processors)) or "(none)"
            raise KeyError(f"unknown processor {name!r}; available: {available}") from None

    def names(self) -> list[str]:
        return sorted(self._processors)

    def __contains__(self, name: str) -> bool:
        return name in self._processors

    def __len__(self) -> int:
        return len(self._processors)


registry = Registry()
