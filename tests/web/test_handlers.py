import json

from chessqual import __version__
from chessqual.web.handlers import (
    handle_assess,
    handle_health,
    handle_index,
    handle_processors,
)
from chessqual.web.http import Request

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_handle_index_serves_html():
    resp = handle_index(Request())
    assert resp.status_code == 200
    assert "text/html" in resp.content_type
    assert "hello" in resp.body.lower()


def test_handle_health():
    resp = handle_health(Request())
    assert resp.status_code == 200
    data = json.loads(resp.body)
    assert data["status"] == "ok"
    assert data["version"] == __version__


def test_handle_processors():
    resp = handle_processors(Request())
    assert resp.status_code == 200
    data = json.loads(resp.body)
    assert set(data["processors"]) >= {"material", "stockfish"}


def test_handle_assess():
    req = Request(method="POST", body={"fens": [START_FEN], "processors": ["material"]})
    resp = handle_assess(req)
    assert resp.status_code == 200
    data = json.loads(resp.body)
    assert data["results"][0]["fen"] == START_FEN
    assert data["results"][0]["assessments"]["material"]["score"] == 0


def test_handle_assess_rejects_missing_fens():
    resp = handle_assess(Request(method="POST", body={}))
    assert resp.status_code == 400


def test_handle_assess_rejects_unknown_processor():
    req = Request(method="POST", body={"fens": [START_FEN], "processors": ["nope"]})
    resp = handle_assess(req)
    assert resp.status_code == 400


def test_handle_assess_rejects_invalid_fen():
    req = Request(method="POST", body={"fens": ["not a fen"], "processors": ["material"]})
    resp = handle_assess(req)
    assert resp.status_code == 400
