"""Pure request handlers — no HTTP framework, fully unit-testable."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .. import __version__
from ..analyze import assess
from ..positions import Collection
from ..processors import registry
from .http import Request, Response, html_response, json_response

_STATIC_DIR = Path(__file__).parent / "static"


def handle_index(request: Request) -> Response:
    """Serve the minimal landing page."""
    return html_response((_STATIC_DIR / "index.html").read_text(encoding="utf-8"))


def handle_health(request: Request) -> Response:
    """Return app health and version."""
    return json_response({"status": "ok", "version": __version__})


def handle_processors(request: Request) -> Response:
    """Return the names of all registered processors."""
    return json_response({"processors": registry.names()})


def handle_assess(request: Request) -> Response:
    """Assess a list of FENs with the requested processors."""
    body = request.body if isinstance(request.body, dict) else {}
    fens = body.get("fens")
    if not isinstance(fens, list) or not fens or not all(isinstance(f, str) for f in fens):
        return json_response({"error": "'fens' must be a non-empty list of FEN strings"}, 400)

    processors = body.get("processors")
    if processors is None:
        processors = registry.names()
    elif not isinstance(processors, list) or not all(isinstance(p, str) for p in processors):
        return json_response({"error": "'processors' must be a list of processor names"}, 400)

    unknown = [p for p in processors if p not in registry]
    if unknown:
        return json_response(
            {"error": f"unknown processors: {unknown}; available: {registry.names()}"}, 400
        )

    try:
        collection = Collection.from_fens(fens)
    except ValueError as exc:
        return json_response({"error": str(exc)}, 400)

    results = []
    for position, row in assess(collection, processors):
        results.append(
            {
                "fen": position.fen,
                "assessments": {name: asdict(a) for name, a in row.items()},
            }
        )
    return json_response({"results": results})
