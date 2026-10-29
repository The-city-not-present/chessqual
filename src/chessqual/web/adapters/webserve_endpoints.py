"""webserve adapter: build a webserve ``endpoints`` dict from the route table.

No import of webserve here: endpoint handlers return the framework-free
:class:`~chessqual.web.http.Response`, which webserve converts internally via
``WebResponse.from_existing`` (its documented "or compatible, per protocol"
contract). The webserve import happens only in the runner (``__main__.py``).
"""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

from ..http import Request, Response
from ..routes import ROUTES


def _request_from_webserve(net_request_handler, method: str) -> Request:
    parsed = urlparse(net_request_handler.path)
    body = None
    raw_body = None
    if hasattr(net_request_handler, "request_body"):
        raw_body = net_request_handler.request_body.read()
        if raw_body:
            try:
                body = json.loads(raw_body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                body = None
    return Request(
        method=method,
        path=parsed.path,
        query=parse_qs(parsed.query),
        body=body,
        raw_body=raw_body,
    )


def _make_endpoint(route):
    def endpoint(net_request_handler, config=None, added_data=None):
        method = (net_request_handler.command or "GET").upper()
        if method == "HEAD" and "GET" in route.methods:
            method = "GET"
        if method not in route.methods:
            return Response(405, "application/json", json.dumps({"error": "method not allowed"}), [])
        try:
            return route.handler(_request_from_webserve(net_request_handler, method))
        except Exception as exc:  # fail with a readable JSON error
            return Response(500, "application/json", json.dumps({"error": str(exc)}), [])

    return endpoint


def build_webserve_endpoints() -> dict:
    """Return a webserve-compatible ``endpoints`` dict for every route."""
    return {route.path: _make_endpoint(route) for route in ROUTES}
