"""The route table: the single source of truth consumed by every adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .handlers import handle_assess, handle_health, handle_index, handle_processors
from .http import Request, Response


@dataclass(frozen=True)
class Route:
    path: str
    methods: frozenset[str]
    handler: Callable[[Request], Response]


ROUTES: tuple[Route, ...] = (
    Route("/", frozenset({"GET"}), handle_index),
    Route("/api/health", frozenset({"GET"}), handle_health),
    Route("/api/processors", frozenset({"GET"}), handle_processors),
    Route("/api/assess", frozenset({"POST"}), handle_assess),
)
