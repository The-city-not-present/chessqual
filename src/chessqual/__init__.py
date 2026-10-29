"""chessqual — analyze chess positions with pluggable processors."""

from .positions import Collection, Position
from .processors import Assessment, Processor, Registry, registry

__version__ = "0.1.0"

__all__ = [
    "Collection",
    "Position",
    "Assessment",
    "Processor",
    "Registry",
    "registry",
    "__version__",
]
