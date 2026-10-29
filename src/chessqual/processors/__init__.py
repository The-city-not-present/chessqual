"""Processors: the extensible assessment layer.

Built-in processors are imported and registered here at import time, so the
global registry (``chessqual.processors.registry.registry``) is always populated.

To add a processor, create a package under ``processors/``, implement an object
with a ``name`` and ``assess(position, **params)`` method, and register it here
(see ``material/`` and ``stockfish/`` for the pattern).
"""

from .base import Assessment, Processor
from .material.processor import MaterialProcessor
from .registry import Registry, registry
from .stockfish.processor import StockfishProcessor

registry.register(MaterialProcessor())
registry.register(StockfishProcessor())

__all__ = [
    "Assessment",
    "Processor",
    "Registry",
    "registry",
    "MaterialProcessor",
    "StockfishProcessor",
]
