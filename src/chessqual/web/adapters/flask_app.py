"""Flask adapter: build a Flask app from the route table."""

from __future__ import annotations

import json
from urllib.parse import urlparse

from ..http import Request, Response
from ..routes import ROUTES


def _request_from_flask(flask_request) -> Request:
    body = None
    raw_body = None
    if flask_request.data:
        raw_body = flask_request.data
        if flask_request.is_json:
            body = flask_request.get_json()
    return Request(
        method=flask_request.method.upper(),
        path=urlparse(flask_request.path).path,
        query=dict(flask_request.args.lists()),
        body=body,
        raw_body=raw_body,
    )


def _to_flask_response(response: Response):
    from flask import Response as FlaskResponse  # local import: optional dep

    data = response.body.encode("utf-8") if isinstance(response.body, str) else response.body
    return FlaskResponse(
        data,
        status=response.status_code,
        content_type=response.content_type,
        headers=dict(response.headers),
    )


def create_flask_app():
    """Build and return a Flask app serving every route (requires ``flask``)."""
    from flask import Flask, request as flask_request  # local import: optional dep

    app = Flask(__name__)

    for route in ROUTES:
        def view(route=route):
            try:
                return _to_flask_response(route.handler(_request_from_flask(flask_request)))
            except Exception as exc:  # fail with a readable JSON error
                return _to_flask_response(
                    Response(500, "application/json", json.dumps({"error": str(exc)}), [])
                )

        app.add_url_rule(
            route.path,
            endpoint=(route.path.replace("/", "_") or "root"),
            view_func=view,
            methods=sorted(route.methods),
        )

    return app
