"""Optional web layer for chessqual.

Serves a JSON API and a minimal HTML page on localhost. The core
(``chessqual``) never imports this package; this package imports the core.

Handlers are framework-free; the ``adapters/`` subpackage wires them to Flask
or to the self-written ``webserve`` server, so the endpoints are identical
either way.
"""

from .handlers import handle_assess, handle_health, handle_index, handle_processors
from .http import Request, Response, html_response, json_response
from .routes import ROUTES, Route

__all__ = [
    "Request",
    "Response",
    "html_response",
    "json_response",
    "Route",
    "ROUTES",
    "handle_assess",
    "handle_health",
    "handle_index",
    "handle_processors",
]
