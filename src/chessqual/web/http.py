"""Framework-free HTTP types shared by the web adapters."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Request:
    """A normalized HTTP request handed to pure handlers."""

    method: str = "GET"
    path: str = "/"
    query: dict[str, Any] = field(default_factory=dict)
    body: Any = None
    raw_body: bytes | None = None


@dataclass
class Response:
    """A framework-free HTTP response.

    The field names intentionally match ``webserve``'s ``WebResponse`` so the
    webserve adapter can hand it over directly (webserve converts it via
    ``WebResponse.from_existing``).
    """

    status_code: int = 200
    content_type: str = "text/plain"
    body: str | bytes = ""
    headers: list[tuple[str, str]] = field(default_factory=list)
    is_binary: bool = False


def json_response(data: Any, status_code: int = 200) -> Response:
    return Response(
        status_code=status_code,
        content_type="application/json",
        body=json.dumps(data),
        headers=[],
    )


def html_response(html: str, status_code: int = 200) -> Response:
    return Response(
        status_code=status_code,
        content_type="text/html; charset=utf-8",
        body=html,
        headers=[],
    )
