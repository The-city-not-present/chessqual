import json

from chessqual.web.adapters.webserve_endpoints import build_webserve_endpoints

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class _FakeRequestHandler:
    def __init__(self, command="GET", path="/", body=b""):
        self.command = command
        self.path = path
        self._body = body

    @property
    def request_body(self):
        class _Reader:
            def __init__(self, data):
                self.data = data

            def read(self):
                return self.data

        return _Reader(self._body)


def test_build_endpoints_has_all_paths():
    endpoints = build_webserve_endpoints()
    assert set(endpoints) == {"/", "/api/health", "/api/processors", "/api/assess"}


def test_get_processors():
    endpoints = build_webserve_endpoints()
    resp = endpoints["/api/processors"](_FakeRequestHandler("GET", "/api/processors"))
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert "material" in resp.body


def test_post_assess():
    endpoints = build_webserve_endpoints()
    body = json.dumps({"fens": [START_FEN], "processors": ["material"]}).encode()
    resp = endpoints["/api/assess"](_FakeRequestHandler("POST", "/api/assess", body))
    assert resp.status_code == 200
    assert "material" in resp.body


def test_wrong_method_returns_405():
    endpoints = build_webserve_endpoints()
    resp = endpoints["/api/assess"](_FakeRequestHandler("GET", "/api/assess"))
    assert resp.status_code == 405


def test_head_treated_as_get():
    endpoints = build_webserve_endpoints()
    resp = endpoints["/"](_FakeRequestHandler("HEAD", "/"))
    assert resp.status_code == 200
